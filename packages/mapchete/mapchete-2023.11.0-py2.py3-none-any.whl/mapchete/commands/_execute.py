"""Execute a process."""

import logging
import traceback
import warnings
from multiprocessing import cpu_count
from typing import Callable, Iterator, List, Tuple, Union

from rasterio.crs import CRS
from shapely.geometry.base import BaseGeometry

import mapchete
from mapchete.config.parse import bounds_from_opts, raw_conf, raw_conf_process_pyramid
from mapchete.enums import Concurrency, ProcessingMode
from mapchete.processing.types import (
    PreprocessingProcessInfo,
    TaskResult,
    TileProcessInfo,
)

logger = logging.getLogger(__name__)


def execute(
    mapchete_config: Union[str, dict],
    zoom: Union[int, List[int]] = None,
    area: Union[BaseGeometry, str, dict] = None,
    area_crs: Union[CRS, str] = None,
    bounds: Tuple[float] = None,
    bounds_crs: Union[CRS, str] = None,
    point: Tuple[float, float] = None,
    point_crs: Tuple[float, float] = None,
    tile: Tuple[int, int, int] = None,
    overwrite: bool = False,
    mode: ProcessingMode = ProcessingMode.CONTINUE,
    concurrency: Concurrency = Concurrency.processes,
    workers: int = None,
    multi: int = None,
    multiprocessing_start_method: str = None,
    dask_scheduler: str = None,
    dask_max_submitted_tasks=1000,
    dask_chunksize=100,
    dask_client=None,
    dask_compute_graph=True,
    dask_propagate_results=True,
    msg_callback: Callable = None,
    as_iterator: bool = False,
    profiling: bool = False,
    **kwargs,
) -> mapchete.Job:
    """
    Execute a Mapchete process.

    Parameters
    ----------
    mapchete_config : str or dict
        Mapchete configuration as file path or dictionary.
    zoom : integer or list of integers
        Single zoom, minimum and maximum zoom or a list of zoom levels.
    area : str, dict, BaseGeometry
        Geometry to override bounds or area provided in process configuration. Can be either a
        WKT string, a GeoJSON mapping, a shapely geometry or a path to a Fiona-readable file.
    area_crs : CRS or str
        CRS of area (default: process CRS).
    bounds : tuple
        Override bounds or area provided in process configuration.
    bounds_crs : CRS or str
        CRS of area (default: process CRS).
    point : iterable
        X and y coordinates of point whose corresponding process tile bounds will be used.
    point_crs : str or CRS
        CRS of point (defaults to process pyramid CRS).
    tile : tuple
        Zoom, row and column of tile to be processed (cannot be used with zoom)
    overwrite : bool
        Overwrite existing output.
    mode : str
        Set process mode. One of "readonly", "continue" or "overwrite".
    workers : int
        Number of execution workers when processing concurrently.
    multiprocessing_start_method : str
        Method used by multiprocessing module to start child workers. Availability of methods
        depends on OS.
    concurrency : str
        Concurrency to be used. Could either be "processes", "threads" or "dask".
    dask_scheduler : str
        URL to dask scheduler if required.
    dask_max_submitted_tasks : int
        Make sure that not more tasks are submitted to dask scheduler at once. (default: 500)
    dask_chunksize : int
        Number of tasks submitted to the scheduler at once. (default: 100)
    dask_client : dask.distributed.Client
        Reusable Client instance if required. Otherwise a new client will be created.
    dask_compute_graph : bool
        Build and compute dask graph instead of submitting tasks as preprocessing & zoom tiles
        batches. (default: True)
    dask_propagate_results : bool
        Propagate results between tasks. This helps to minimize read calls when building overviews
        but can lead to a much higher memory consumption on the cluster. Only with effect if
        dask_compute_graph is activated. (default: True)
    msg_callback : Callable
        Optional callback function for process messages.
    as_iterator : bool
        Returns as generator but with a __len__() property.

    Returns
    -------
    mapchete.Job instance either with already processed items or a generator with known length.

    Examples
    --------
    >>> execute("foo")

    This will run the whole execute process.

    >>> for i in execute("foo", as_iterator=True):
    >>>     print(i)

    This will return a generator where through iteration, tiles are copied.

    >>> list(tqdm.tqdm(execute("foo", as_iterator=True)))

    Usage within a process bar.
    """
    mode = "overwrite" if overwrite else mode

    def _empty_callback(_):
        pass

    print_task_details = msg_callback is not None
    msg_callback = msg_callback or _empty_callback
    if multi is not None:  # pragma: no cover
        warnings.warn("The 'multi' parameter is deprecated and is now named 'workers'")
    workers = workers or multi or cpu_count()

    if tile:
        tile = raw_conf_process_pyramid(raw_conf(mapchete_config)).tile(*tile)
        bounds = tile.bounds
        zoom = tile.zoom
    else:
        bounds = bounds_from_opts(
            point=point,
            point_crs=point_crs,
            bounds=bounds,
            bounds_crs=bounds_crs,
            raw_conf=raw_conf(mapchete_config),
        )

    # be careful opening mapchete not as context manager
    with mapchete.Timer() as t:
        mp = mapchete.open(
            mapchete_config,
            mode=mode,
            bounds=bounds,
            zoom=zoom,
            area=area,
            area_crs=area_crs,
        )
    logger.debug("initialized process in %s", t)
    try:
        preprocessing_tasks = mp.config.preprocessing_tasks_count()
        tiles_tasks = 1 if tile else mp.count_tiles()
        total_tasks = preprocessing_tasks + tiles_tasks
        msg_callback(
            f"processing {preprocessing_tasks} preprocessing tasks and {tiles_tasks} tile tasks on {workers} worker(s)"
        )
        # automatically use dask Executor if dask scheduler is defined
        if dask_scheduler or dask_client or concurrency == "dask":
            concurrency = "dask"
        # use sequential Executor if only one tile or only one worker is defined
        elif total_tasks == 1 or workers == 1:
            logger.debug(
                "using sequential Executor because there is only one %s",
                "task" if total_tasks == 1 else "worker",
            )
            concurrency = None
        stac_item_path = mp.config.output.stac_path
        return mapchete.Job(
            _process_everything,
            fargs=(
                msg_callback,
                mp,
            ),
            fkwargs=dict(
                tile=tile,
                workers=workers,
                zoom=None if tile else zoom,
                print_task_details=print_task_details,
                dask_max_submitted_tasks=dask_max_submitted_tasks,
                dask_chunksize=dask_chunksize,
                dask_compute_graph=dask_compute_graph,
                dask_propagate_results=dask_propagate_results,
                profiling=profiling,
            ),
            executor_concurrency=concurrency,
            executor_kwargs=dict(
                dask_scheduler=dask_scheduler,
                dask_client=dask_client,
                multiprocessing_start_method=multiprocessing_start_method,
                max_workers=workers,
            ),
            as_iterator=as_iterator,
            preprocessing_tasks=preprocessing_tasks,
            tiles_tasks=tiles_tasks,
            process_area=mp.config.init_area,
            stac_item_path=stac_item_path,
        )
    # explicitly exit the mp object on failure
    except Exception as exc:  # pragma: no cover
        mp.__exit__(exc, repr(exc), traceback.format_exc())
        raise


def _process_everything(
    msg_callback,
    mp,
    print_task_details=True,
    **kwargs,
) -> Iterator[TaskResult]:
    try:
        for future in mp.compute(**kwargs):
            result = TaskResult.from_future(future)
            if print_task_details:
                msg = f"task {result.id}: {result.process_msg}"
                if result.profiling:  # pragma: no cover
                    max_allocated = (
                        result.profiling["memory"].max_allocated / 1024 / 1024
                    )
                    head_requests = result.profiling["requests"].head_count
                    get_requests = result.profiling["requests"].get_count
                    requests = head_requests + get_requests
                    transfer = result.profiling["requests"].get_bytes / 1024 / 1024
                    msg += f" (max memory usage: {max_allocated:.2f}MB, {requests} GET and HEAD requests, {transfer:.2f}MB transferred)"
                msg_callback(msg)
            yield result
        # explicitly exit the mp object on success
        mp.__exit__(None, None, None)
    except Exception as exc:  # pragma: no cover
        mp.__exit__(exc, repr(exc), traceback.format_exc())
        raise
