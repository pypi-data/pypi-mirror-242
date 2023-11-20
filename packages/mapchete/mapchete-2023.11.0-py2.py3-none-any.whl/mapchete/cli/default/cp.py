import click
import tqdm

from mapchete import commands
from mapchete.cli import options


def _cb_none_concurrency(ctx, param, value):
    return None if value == "none" else value


@click.command(help="Copy TileDirectory from one source to another.")
@options.arg_src_tiledir
@options.arg_dst_tiledir
@options.opt_zoom
@options.opt_area
@options.opt_area_crs
@options.opt_bounds
@options.opt_bounds_crs
@options.opt_point
@options.opt_point_crs
@options.opt_overwrite
@options.opt_verbose
@options.opt_no_pbar
@options.opt_debug
@options.opt_logfile
@options.opt_workers
@options.opt_dask_scheduler
@click.option(
    "--concurrency",
    type=click.Choice(["processes", "threads", "dask", "none"]),
    default="threads",
    callback=_cb_none_concurrency,
    help="Decide which Executor to use for concurrent processing.",
)
@options.opt_http_username
@options.opt_http_password
@options.opt_src_fs_opts
@options.opt_dst_fs_opts
def cp(*args, debug=False, no_pbar=False, verbose=False, logfile=None, **kwargs):
    """Copy TileDirectory in full or a subset from one source to another."""
    # handle deprecated options
    for x in ["password", "username"]:
        if kwargs.get(x):  # pragma: no cover
            raise click.BadOptionUsage(
                x,
                f"'--{x} foo' is deprecated. You should use '--src-fs-opts {x}=foo' instead.",
            )
        kwargs.pop(x)
    # copy
    list(
        tqdm.tqdm(
            commands.cp(
                *args,
                as_iterator=True,
                msg_callback=tqdm.tqdm.write if verbose else None,
                **kwargs,
            ),
            unit="tile",
            disable=debug or no_pbar,
        )
    )
