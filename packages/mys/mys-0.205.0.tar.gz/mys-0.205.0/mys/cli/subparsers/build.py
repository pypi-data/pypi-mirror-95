from ..utils import add_coverage_argument
from ..utils import add_debug_symbols_argument
from ..utils import add_jobs_argument
from ..utils import add_no_ccache_argument
from ..utils import add_optimize_argument
from ..utils import add_verbose_argument
from ..utils import build_app
from ..utils import build_prepare


def do_build(_parser, args, _mys_config):
    is_application, build_dir = build_prepare(args.verbose,
                                              args.optimize,
                                              args.debug_symbols,
                                              args.no_ccache,
                                              args.coverage)
    build_app(args.debug,
              args.verbose,
              args.jobs,
              is_application,
              args.coverage,
              build_dir)


def add_subparser(subparsers):
    subparser = subparsers.add_parser(
        'build',
        description='Build the appliaction.')
    add_verbose_argument(subparser)
    add_jobs_argument(subparser)
    add_optimize_argument(subparser, 'speed')
    add_debug_symbols_argument(subparser)
    add_no_ccache_argument(subparser)
    add_coverage_argument(subparser)
    subparser.set_defaults(func=do_build)
