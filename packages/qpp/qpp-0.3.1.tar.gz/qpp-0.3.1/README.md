# qpp - Query PyPI

[![Python versions](https://img.shields.io/pypi/pyversions/qpp.svg)](https://pypi.org/project/qpp/)
[![PyPI version](https://img.shields.io/pypi/v/qpp.svg)](https://pypi.org/project/qpp/)
[![License](https://img.shields.io/pypi/l/qpp.svg)](https://pypi.org/project/qpp/)

Find Python projects on pypi.org on the command line or from your own code.

## Usage

### On the command line

```bash
% qpp exists talk-like-a-pirate
The package name talk-like-a-pirate has not yet been registered on PyPI.
%
```

```bash
% qpp info pip
pip v23.1.1
The PyPA recommended tool for installing Python packages.

Author: The pip developers <distutils-sig@python.org>
License: MIT
Homepage:    https://pip.pypa.io/
Package URL: https://pypi.org/project/pip/
Project URL: https://pypi.org/project/pip/
Python versions: >=3.7
Keywords:
Classifiers:
    Development Status :: 4 - Beta
    Intended Audience :: Developers
    License :: OSI Approved :: MIT License
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3 :: Only
    Programming Language :: Python :: 3.10
    Programming Language :: Python :: 3.11
    Programming Language :: Python :: 3.9
    Programming Language :: Python :: Implementation :: CPython
    Programming Language :: Python :: Implementation :: PyPy
    Topic :: Software Development :: Build Tools
%
```

`qpp info --description pip` or, short, `qpp info pip -d`, displays the same as above, but also includes the project's README.

`qpp` can render READMEs written in Markdown (using [rich](https://pypi.org/project/rich/)), reStructuredText (using [rich-rst](https://pypi.org/project/rich-rst/)), and plain text.

`qpp open <name>` opens the package's PyPI project page in the system's default browser.

```bash
% qpp search pypi -n 3
pypi
   PyPI is the Python Package Index at http://pypi.org/
   Version: v2.1
   Released: Mar 24, 2018
   URL: https://pypi.org/project/pypi/

pypi1108
   My short description for my project.
   Version: v5.2.0
   Released: Nov 8, 2022
   URL: https://pypi.org/project/pypi1108/

pypi-client
   PyPI command-line tool
   Version: v0.2.3
   Released: Dec 17, 2020
   URL: https://pypi.org/project/pypi-client/
%
```

The -n option limits the amount of results shown.

### As a library

```python
from qpp import queries as pypi
# exists:
assert pypi.exists('pypi')
assert not pypi.exists('talk-like-a-pirate')
# info:
pkg_info = pypi.info('rich')
from qpp.renderables import PackageMetadataRenderable
from rich.console import Console
console = Console()
console.print(PackageMetadataRenderable(pkg_info))
# Output not shown.
# Or with the long description:
console.print(PackageMetadataRenderable(pkg_info, with_description=True))
# Output not shown.
# Search:
found = pypi.search('pypi')
assert len(found)
```

## Credits

`qpp` was cooked with the tastiest ingredients:

- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)
- [rich](https://pypi.org/project/rich/)
- [rich-argparse-plus](https://pypi.org/project/rich_argparse_plus/)
- [rich-rst](https://pypi.org/project/rich-rst/)
