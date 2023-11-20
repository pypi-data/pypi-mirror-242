"""Internal processing classes and functions."""

import logging
import os
from enum import Enum
from typing import Callable, Iterator, Optional

from shapely.geometry import base, mapping

from mapchete.enums import Concurrency
from mapchete.executor import Executor, ExecutorBase
from mapchete.processing.types import TaskResult
from mapchete.types import Bounds, MPathLike

FUTURE_TIMEOUT = float(os.environ.get("MP_FUTURE_TIMEOUT", 10))


logger = logging.getLogger(__name__)


class Status(Enum):
    pending = "pending"
    running = "running"
    finished = "finished"
    cancelled = "cancelled"


class Job:
    """
    Wraps the output of a processing function into a generator with known length.

    This class also exposes the internal Executor.cancel() function in order to cancel all remaining
    tasks/futures.

    Will move into the mapchete core package.
    """

    func: Callable[..., Iterator[TaskResult]]
    fargs: tuple
    fkwargs: dict
    status: Status
    executor: ExecutorBase
    executor_concurrency: Concurrency
    executor_kwargs: dict
    tiles_tasks: int
    bounds: Optional[Bounds]
    stac_item_path: Optional[MPathLike]

    def __init__(
        self,
        func: Callable[..., Iterator[TaskResult]],
        fargs: tuple = None,
        fkwargs: dict = None,
        as_iterator: bool = False,
        tiles_tasks: int = None,
        preprocessing_tasks: int = None,
        executor_concurrency: Concurrency = Concurrency.processes,
        executor_kwargs: dict = None,
        process_area: Optional[base.BaseGeometry] = None,
        stac_item_path: Optional[MPathLike] = None,
    ):
        self.func = func
        self.fargs = fargs or ()
        self.fkwargs = fkwargs or {}
        self.status = Status.pending
        self.executor_concurrency = executor_concurrency
        self.executor_kwargs = executor_kwargs or {}
        self.tiles_tasks = tiles_tasks or 0
        self.preprocessing_tasks = preprocessing_tasks or 0
        self._total = self.preprocessing_tasks + self.tiles_tasks
        self._as_iterator = as_iterator
        self._process_area = process_area
        self.bounds = Bounds(*process_area.bounds) if process_area is not None else None
        self.stac_item_path = stac_item_path
        if not as_iterator:
            self._results: Iterator[TaskResult] = list(self._run())

    @property
    def __geo_interface__(self) -> dict:  # pragma: no cover
        if self._process_area is not None:
            return mapping(self._process_area)
        else:
            raise AttributeError(f"{self} has no geo information assigned")

    def _run(self) -> Iterator[TaskResult]:
        if self._total == 0:
            return
        logger.debug("opening executor for job %s", repr(self))

        with Executor(
            concurrency=self.executor_concurrency, **self.executor_kwargs
        ) as self.executor:
            self.status = Status.running
            logger.debug("change of job status: %s", self)
            yield from self.func(*self.fargs, executor=self.executor, **self.fkwargs)
            self.status = Status.finished
            logger.debug("change of job status: %s", self)

    def set_executor_kwargs(self, executor_kwargs):
        """
        Overwrite default or previously set Executor creation kwargs.

        This only has an effect if Job was initialized with 'as_iterator' and has not yet run.
        """
        self.executor_kwargs = executor_kwargs

    def set_executor_concurrency(self, executor_concurrency):
        """
        Overwrite default or previously set Executor concurrency.

        This only has an effect if Job was initialized with 'as_iterator' and has not yet run.
        """
        self.executor_concurrency = executor_concurrency

    def cancel(self):
        """Cancel all running and pending Job tasks."""
        if self._as_iterator:
            # requires client and futures
            if self.executor is None:  # pragma: no cover
                raise ValueError("nothing to cancel because no executor is running")
            self.executor.cancel()
            self.status = Status.cancelled

    def __len__(self):
        return self._total

    def __iter__(self) -> Iterator[TaskResult]:
        if self._as_iterator:
            yield from self._run()
        else:
            return self._results

    def __repr__(self):  # pragma: no cover
        return f"<{self.status} Job with {self._total} tasks.>"
