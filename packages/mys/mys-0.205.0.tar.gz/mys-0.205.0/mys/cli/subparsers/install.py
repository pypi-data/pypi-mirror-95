import glob
import os
import shutil
import sys
import tarfile
from tempfile import TemporaryDirectory

from ..utils import ERROR
from ..utils import Spinner
from ..utils import add_jobs_argument
from ..utils import add_no_ccache_argument
from ..utils import add_verbose_argument
from ..utils import box_print
from ..utils import build_app
from ..utils import build_prepare
from ..utils import read_package_configuration
from ..utils import run


def install_clean():
    if not os.path.exists('package.toml'):
        raise Exception('not a package')

    with Spinner(text='Cleaning'):
        shutil.rmtree('build', ignore_errors=True)

def install_download(args):
    command = [
        sys.executable, '-m', 'pip', 'download', f'mys-{args.package}'
    ]
    run(command, 'Downloading package', args.verbose)


def install_extract():
    archive = glob.glob('mys-*.tar.gz')[0]

    with Spinner(text='Extracting package'):
        with tarfile.open(archive) as fin:
            fin.extractall()

    os.remove(archive)


def install_build(args):
    config = read_package_configuration()
    is_application, build_dir = build_prepare(args.verbose,
                                              'speed',
                                              False,
                                              args.no_ccache,
                                              False,
                                              config)

    if not is_application:
        box_print(['There is no application to build in this package (src/main.mys ',
                   'missing).'],
                  ERROR)

        raise Exception()

    build_app(args.debug, args.verbose, args.jobs, is_application, False, build_dir)

    return config

def install_install(root, _args, config):
    bin_dir = os.path.join(root, 'bin')
    bin_name = config['package']['name']
    src_file = 'build/default/app'
    dst_file = os.path.join(bin_dir, bin_name)

    with Spinner(text=f"Installing {bin_name} in {bin_dir}"):
        os.makedirs(bin_dir, exist_ok=True)
        shutil.copyfile(src_file, dst_file)
        shutil.copymode(src_file, dst_file)


def install_from_current_dirctory(args, root):
    install_clean()
    config = install_build(args)
    install_install(root, args, config)


def install_from_registry(args, root):
    with TemporaryDirectory()as tmp_dir:
        os.chdir(tmp_dir)
        install_download(args)
        install_extract()
        os.chdir(glob.glob('mys-*')[0])
        config = install_build(args)
        install_install(root, args, config)


def do_install(_parser, args, _mys_config):
    root = os.path.abspath(os.path.expanduser(args.root))

    if args.package is None:
        install_from_current_dirctory(args, root)
    else:
        install_from_registry(args, root)


def add_subparser(subparsers):
    subparser = subparsers.add_parser(
        'install',
        description='Install an application from local package or registry.')
    add_verbose_argument(subparser)
    add_jobs_argument(subparser)
    add_no_ccache_argument(subparser)
    subparser.add_argument('--root',
                           default='~/.local',
                           help='Root folder to install into (default: %(default)s.')
    subparser.add_argument(
        'package',
        nargs='?',
        help=('Package to install application from. Installs current package if '
              'not given.'))
    subparser.set_defaults(func=do_install)
