
from textwrap import indent
from typing import List   # required to support py3.8, else just use "list"

from rich.console import Console, ConsoleOptions, RenderResult
from rich.markdown import Markdown
from rich_rst import RestructuredText

from qpp.metadata import PackageMetadata, PackageSummary



class SearchResultRenderable:
    def __init__(self, results: List[PackageSummary]):
        self._search_results = results

    def __rich_console__(self,
                         _: Console,
                         __: ConsoleOptions) -> RenderResult:
        for pkg in self._search_results:
            output = (
                f'[b]{pkg.name}[/b]\n'
                f'   [i]{pkg.description}[/i]\n'
                f'   Version: [bold cyan]v{pkg.version}[/]\n'
                f'   Released: {pkg.date}\n'
                f'   URL: {pkg.pypi_url}\n'
            )
            yield output


class PackageMetadataRenderable:
    def __init__(self,
                 package_info: PackageMetadata,
                 with_description: bool=False):
        self._package_info = package_info
        self._with_desciption = with_description

    def __rich_console__(self,
                         _: Console,
                         __: ConsoleOptions) -> RenderResult:
        pkg = self._package_info
        yield f'[b]{pkg.name}[/b] [bold cyan]v{pkg.version}'
        yield f'[i]{pkg.summary}\n'
        yield f'Author: {pkg.author} [bright_blue]<{pkg.author_email}>'
        yield f'License: {pkg.license}'
        yield f'Homepage:    {pkg.home_page}'
        yield f'Package URL: {pkg.package_url}'
        yield f'Project URL: {pkg.project_url}'
        yield f'Python versions: {pkg.requires_python}'
        yield f'Keywords: {pkg.keywords}'
        classifiers = indent("\n".join(pkg.classifiers), '    ')
        yield f'Classifiers:\n{classifiers}'
        if self._with_desciption:
            yield '\nFull description:\n'
            if pkg.description_content_type == 'text/markdown':
                # twine's is nice and short
                yield Markdown(pkg.description)
            elif pkg.description_content_type == 'text/x-rst':
                # One package which uses RST is flit.
                yield RestructuredText(pkg.description)
            else:
                # One package which uses RST is flitter, pypi.
                yield pkg.description
