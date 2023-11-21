
'''
Ask pypi.org interesting things.
'''

import re
from typing import List

import requests
from bs4 import BeautifulSoup

from .metadata import PackageSummary, PackageMetadata

TIMEOUT = 2   # in seconds


def info(project: str) -> PackageMetadata:
    '''Ask PyPI for information of the given package.'''
    response = requests.get(f'https://pypi.org/pypi/{project}/json',
                            timeout=TIMEOUT)
    if response.status_code == 404:
        return None
    # Some packages, for instance those uploaded by flit, have neither
    # author nor license items. Glean those from the author_email and
    # classifiers items.
    info = response.json()['info']
    if not info['author']:
        match = re.match(r'^(.+) <(.+)>$', info['author_email'])
        if match and len(match.groups()) == 2:
            info['author'] = match.groups()[0]
            info['author_email'] = match.groups()[1]
    if not info['license']:
        # Get it from the classifiers
        if found := [x for x in info['classifiers'] if 'License ::' in x]:
            info['license'] = found[0].split('::')[-1]
        pass
    return PackageMetadata(**info)


def exists(project: str) -> bool:
    '''Ask PyPI if a project of the given name exists.'''
    return info(project) is not None


def search(query: str) -> List[PackageSummary]:
    '''Search PyPI for packages.'''
    response = requests.get(f'https://pypi.org/search/?q={query}',
                            timeout=TIMEOUT)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = []
    #project = namedtuple('project', 'description url')
    for item in soup.findAll('a', class_='package-snippet'):
        spans = item.h3.findAll('span')
        proj = {}
        proj['url'] = f'https://pypi.org{item.get("href")}'
        proj['description'] = item.p.get_text()
        proj['name'] = spans[0].get_text()
        proj['version'] = spans[1].get_text()
        pkg_info = PackageSummary(
            pypi_url=f'https://pypi.org{item.get("href")}',
            name=spans[0].get_text(),
            date=spans[2].get_text().strip(),
            version=spans[1].get_text(),
            description=item.p.get_text()
        )
        result.append(pkg_info)
    return result
