"""Remove tiles from Tile Directory."""

import logging
from typing import Callable, List, Tuple, Union

from rasterio.crs import CRS
from shapely.geometry.base import BaseGeometry

import mapchete
from mapchete.io import tiles_exist
from mapchete.path import MPath

logger = logging.getLogger(__name__)


def rm(
    tiledir: str,
    zoom: Union[int, List[int]] = None,
    area: Union[BaseGeometry, str, dict] = None,
    area_crs: Union[CRS, str] = None,
    bounds: Tuple[float] = None,
    bounds_crs: Union[CRS, str] = None,
    multi: int = None,
    fs_opts: dict = None,
    msg_callback: Callable = None,
    as_iterator: bool = False,
) -> mapchete.Job:
    """
    Remove tiles from TileDirectory.

    Parameters
    ----------
    tiledir : str
        TileDirectory or mapchete file.
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
    multi : int
        Number of threads used to check whether tiles exist.
    fs_opts : dict
        Configuration options for fsspec filesystem.
    msg_callback : Callable
        Optional callback function for process messages.
    as_iterator : bool
        Returns as generator but with a __len__() property.

    Returns
    -------
    mapchete.Job instance either with already processed items or a generator with known length.

    Examples
    --------
    >>> rm("foo", zoom=5)

    This will run the whole rm process.

    >>> for i in rm("foo", zoom=5, as_iterator=True):
    >>>     print(i)

    This will return a generator where through iteration, tiles are removed.

    >>> list(tqdm.tqdm(rm("foo", zoom=5, as_iterator=True)))

    Usage within a process bar.

    """

    def _empty_callback(*_):
        pass

    msg_callback = msg_callback or _empty_callback
    if zoom is None:  # pragma: no cover
        raise ValueError("zoom level(s) required")

    tiledir = MPath.from_inp(tiledir, storage_options=fs_opts)

    with mapchete.open(
        tiledir,
        zoom=zoom,
        area=area,
        area_crs=area_crs,
        bounds=bounds,
        bounds_crs=bounds_crs,
        mode="readonly",
    ) as mp:
        tp = mp.config.output_pyramid

        tiles = {}
        for zoom in mp.config.init_zoom_levels:
            tiles[zoom] = []
            # check which source tiles exist
            logger.debug("looking for existing source tiles in zoom %s...", zoom)
            for tile, exists in tiles_exist(
                config=mp.config,
                output_tiles=[
                    t
                    for t in tp.tiles_from_geom(mp.config.area_at_zoom(zoom), zoom)
                    # this is required to omit tiles touching the config area
                    if mp.config.area_at_zoom(zoom).intersection(t.bbox).area
                ],
                workers=multi,
            ):
                if exists:
                    tiles[zoom].append(tile)

        paths = [
            mp.config.output_reader.get_path(tile)
            for zoom_tiles in tiles.values()
            for tile in zoom_tiles
        ]
        return mapchete.Job(
            _rm,
            fargs=(
                paths,
                tiledir.fs,
                msg_callback,
            ),
            as_iterator=as_iterator,
            tiles_tasks=len(paths),
        )


def _rm(paths, fs, msg_callback, recursive=False, **_):
    """
    Remove one or multiple paths from file system.

    Note: all paths have to be from the same file system!

    Parameters
    ----------
    paths : str or list
    fs : fsspec.FileSystem
    """
    logger.debug("got %s path(s) on %s", len(paths), fs)

    # s3fs enables multiple paths as input, so let's use this:
    if "s3" in fs.protocol:  # pragma: no cover
        fs.rm(paths, recursive=recursive)
        for path in paths:
            msg = f"deleted {path}"
            logger.debug(msg)
            yield msg

    # otherwise, just iterate through the paths
    else:
        for path in paths:
            fs.rm(path, recursive=recursive)
            msg = f"deleted {path}"
            logger.debug(msg)
            yield msg

    msg_callback(f"{len(paths)} tiles deleted")
