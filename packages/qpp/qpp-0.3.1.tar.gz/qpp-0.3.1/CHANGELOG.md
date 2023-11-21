# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Version numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## 0.3.1 - 2023-11-20

### Changed

- Confirmed to work with Python 3.12.

## 0.3.0 - 2023-05-05

### Added

- Support for Linux and Windows (Git Bash). (Prior to this version only macOS
  was supported.)
- Nicely colored command line help.
- A -n option for pypi search to limit the amount of matches found.

### Changed

- Renamed the askpypi package to qpp (Query PyPI). There already is a package
  called ask-pypi on PyPI.

### Removed

- Support for Python 3.8.

## 0.2.0 - 2023-03-14

### Added

- `qpp info <package_name>` displays the info PyPI has on the package.
  Package descriptions in Markdown or reStructuredText or plain text formats are beautifully rendered with colors and styles applied.
- `qpp open <package_name>` opens the project's PyPI homepage in the
  system's default browser.
- `qpp search <name>` lists all projects which PyPI found for \<name>.

## 0.1.0 - 2023-03-11

### Added

- `qpp exists <package_name>` informs whether a package called
  package_name is available on PyPI.
