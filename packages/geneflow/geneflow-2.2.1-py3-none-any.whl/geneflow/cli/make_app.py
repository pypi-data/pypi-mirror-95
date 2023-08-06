"""This module contains methods for the make-app CLI command."""


from pathlib import Path
import yaml

from geneflow.log import Log
from geneflow.app_installer import AppInstaller


def init_subparser(subparsers):
    """
    Initialize argument sub-parser for make-app sub-command.

    Args:
        subparsers: list of argparse subparsers

    Returns:
        None

    """
    parser = subparsers.add_parser(
        'make-app', help='make app from templates'
    )
    parser.add_argument(
        'app_path',
        type=str,
        help='GeneFlow app package path'
    )
    parser.add_argument(
        '-t', '--target',
        type=str,
        required=False,
        default='all',
        help=(
            'App file to make '
            '(agave, wrapper, test, all [default])'
        )
    )
    parser.set_defaults(func=make_app)

    return parser


def make_app(args, other_args, subparser=None):
    """
    Make app files from templates.

    Args:
        args: contains all command-line arguments.

    Returns:
        On success: True.
        On failure: False.

    """
    app_installer = AppInstaller(str(Path(args.app_path).resolve()), {})

    if not app_installer.load_app():
        Log.an().error('cannot load app config file')
        return False

    if args.target == 'agave':
        if not app_installer.make_agave():
            Log.an().error('cannot make app agave definition')
            return False

    elif args.target == 'wrapper':
        if not app_installer.make_wrapper():
            Log.an().error('cannot make app wrapper script')
            return False

    elif args.target == 'test':
        if not app_installer.make_test():
            Log.an().error('cannot make app test script')
            return False

    elif args.target == 'all':
        if not app_installer.make():
            Log.an().error('cannot make app files')
            return False

    else:
        Log.an().error(
            'invalid target, please specify agave, wrapper, or test'
        )
        return False

    return True
