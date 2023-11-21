#!/usr/bin/env python3

'''
This tool checks if a given name is already registered as a package on
PyPI. This is useful when starting a new project, and when preparing
to register that new project with PyPI.
'''


import argparse
import webbrowser

from requests.exceptions import Timeout as PyPITimeout
from rich_argparse_plus import RichHelpFormatterPlus

from qpp import queries
from qpp.console import console
from qpp.renderables import (PackageMetadataRenderable,
                             SearchResultRenderable)


def configure_cmdline():
    RichHelpFormatterPlus.choose_theme('black_and_white')
    RichHelpFormatterPlus.styles['argparse.args'] = 'default'
    RichHelpFormatterPlus.styles['argparse.groups'] = 'bold'
    RichHelpFormatterPlus.styles['argparse.help'] = 'default'
    RichHelpFormatterPlus.styles['argparse.metavar'] = 'default'
    RichHelpFormatterPlus.styles['argparse.syntax'] = 'bold'
    RichHelpFormatterPlus.styles['argparse.text'] = 'default'
    RichHelpFormatterPlus.group_name_formatter = str.title

    parser = argparse.ArgumentParser(
        description='Obtains information on packages from pypi.org.',
        formatter_class=RichHelpFormatterPlus,
    )
    subparsers = parser.add_subparsers(
        metavar='COMMAND',
        help='[u]Description[/]',
        dest='subcommand'
    )
    # classifiers_parser = subparsers.add_parser(
    #     'classifiers',
    #     description='Fetches the known Trove classifiers from PyPI. The '
    #                 'selects which ones to apply to the current project. '
    #                 'The tool updates the project\'s metadata accordingly.',
    #     help='applies Trove classifiers to a project\'s metadata')
    #     # Note: Either DIY or
    #     # from Trove_classifiers import classifiers
    #     # https://github.com/pypa/trove-classifiers
    #     # This is from the PyPA i.e the source of what is seen on PyPI.
    #     # So don't DIY !
    #     # tool / app name:
    #     #     trover
    #     #     metapher or metaphur   (metaphor is already taken)
    #     #     for a more capable py metadata editor
    #     #     also avail: metaditor, meteditor
    #     # should also check if the classifiers used in setup.cfg/pyproject.toml
    #     # are valid i.e. classiefier in trove-classifiers
    exists_parser = subparsers.add_parser(
        'exists',
        aliases=['x'],
        description='This command checks if the PyPI contains the named '
                    'package.',
        help='check if the named package has been registered with PyPI',
        formatter_class=RichHelpFormatterPlus,
    )
    info_parser = subparsers.add_parser(
        'info',
        aliases=['i'],
        description='Obtains information on a Python package from PyPI '
                    'and prints it out.',
        help='ask PyPI for info on packages',
        formatter_class=RichHelpFormatterPlus,
    )
    open_parser = subparsers.add_parser(
        'open',
        aliases=['o'],
        description='This is a shortcut to quickly open a PyPI package\'s '
                    'project page in a browser.',
        help='open the package\'s project page in a browser',
        formatter_class=RichHelpFormatterPlus,
    )
    search_parser = subparsers.add_parser(
        'search',
        aliases=['s'],
        description='Searches PyPI for packages whose name contains '
                    'project',
        help='search the PyPI for packages',
        formatter_class=RichHelpFormatterPlus,
    )
    info_parser.add_argument(
        '-d', '--description',
        default=False,
        action='store_true',
        help="output the package's long description as well",
    )
    search_parser.add_argument(
        '-n', '--num',
        type=int,
        default=None,
        help="only output the first [b]NUM[/] matches found",
    )

    for prsr in [info_parser, exists_parser, open_parser]:
        prsr.add_argument(
            'package',
            help='the package name to check for'
        )
    search_parser.add_argument(
        'query',
        help='what to look for'
    )

    exists_parser.set_defaults(func=on_exists)
    info_parser.set_defaults(func=on_info)
    open_parser.set_defaults(func=on_open)
    search_parser.set_defaults(func=on_search)

    return parser


def on_exists(args):
    registered = queries.exists(args.package)
    result = ('[bold orange3]already[/]'
              if registered
              else '[light_green]not yet[/]')
    console.print(f'The package name [b]{args.package}[/] has {result} '
                   'been registered on PyPI.')


def on_info(args):
    info = queries.info(args.package)
    if not info:
        # console.print('Package not found')
        return
    console.print(PackageMetadataRenderable(info,
                                            with_description=args.description))


def on_open(args):
    results = queries.info(args.package)
    if not results:
        console.print('Package not found')
        return
    webbrowser.open(results.package_url)


def on_search(args):
    max = args.num
    results = queries.search(args.query)
    console.print(SearchResultRenderable(results[:max]))


def main():
    parser = configure_cmdline()
    args = parser.parse_args()
    if not args.subcommand:
        parser.print_usage()
    try:
        args.func(args)
    except PyPITimeout:
        console.print('No response from pypi.org')


if __name__ == "__main__":
    main()


# pypi info <project>
#      calls https://pypi.org/pypi/<project>/json/
#      shows info on the project such as description, author, homepage
# pypi exists <project>'
#      calls https://pypi.org/pypi/<project>/json/
#      shows whether the project name has been registered or not
# pypi search <query>
#      calls https://pypi.org/search/?q=<query>
# pypi open <project>
#      calls https://pypy.org/pypi/<project>/json/
#      to get the project_url, then
#      opens https://pypi.org/project/<project>/
#      in a browser
