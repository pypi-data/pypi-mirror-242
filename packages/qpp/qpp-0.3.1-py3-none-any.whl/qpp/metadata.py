
from dataclasses import dataclass, fields
from typing import List   # required to support py3.8, else just use "list"


@dataclass
class PackageSummary:
    pypi_url: str
    name: str
    date: str
    version: str
    description: str


@dataclass
class PackageMetadata:
    author: str
    author_email: str
    classifiers: List[str]
    description: str
    description_content_type: str
    home_page: str
    keywords: str
    license: str
    name: str
    package_url: str
    project_url: str
    requires_python: str
    summary: str
    version: str

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in [attr.name for attr in fields(PackageMetadata)]:
                setattr(self, key, value)
