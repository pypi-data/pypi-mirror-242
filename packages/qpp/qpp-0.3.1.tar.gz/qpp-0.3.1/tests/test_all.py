
import platform
import sys

import pytest
from rich.text import Text

import qpp.__main__ as main
from qpp.__main__ import main as cli


class ArgumentsHolder:
    pass


def test_exists(capsys):
    args = ArgumentsHolder()
    args.package = 'Today is talk-like-a-pirate-day. ARRR!'
    main.on_exists(args)
    out, _ = capsys.readouterr()
    result = Text.from_ansi(out).plain.replace('\n', '')
    assert 'has not yet been registered on PyPI' in result
    args.package = 'pypi'
    main.on_exists(args)
    out, _ = capsys.readouterr()
    result = Text.from_ansi(out).plain.replace('\n', '')
    assert 'has already been registered' in result


def test_info(capsys):
    args = ArgumentsHolder()
    args.package = 'Today is talk-like-a-pirate-day. ARRR!'
    main.on_info(args)
    out, _ = capsys.readouterr()
    assert not out
    args.package = 'pypi'
    args.description = False
    main.on_info(args)
    out, _ = capsys.readouterr()
    assert 'PyPI is the Python Package Index' in out
    # Now, verify that a readme in plain text format is rendered.
    # Projects with plain text readmes are e.g. fliiter and pypi
    args.description = True
    main.on_info(args)
    out, _ = capsys.readouterr()
    assert 'PyPI has a new home' in out
    # Now, verify this works with a project like flit - its readme is
    # in RST format.
    # Note that this test emits a DeprecationWarning because rich_rst
    # uses a deprecated option in Docutils.
    args.package = 'flit'
    main.on_info(args)
    out, _ = capsys.readouterr()
    if platform.uname().system != 'Windows':
        # The rendered rST output contains ANSI escape codes around the square
        # brackets so --symlink and --python path/to/python are rendered bold.
        # Therefore the following assertion must work.
        assert 'flit install [--symlink] [--python path/to/python]' not in out
        # Unfortunately, I could not yet get the Windows terminal to render bold
        # text in Git Bash when this test is run by tox. It works when pytest is
        # run direclty. <scratching my head/>
    result = Text.from_ansi(out).plain
    assert 'flit install [--symlink] [--python path/to/python]' in result
    # Finally, test with a project with a readme in Markdown format.
    # twine's is nice and short.
    args.package = 'twine'
    main.on_info(args)
    out, _ = capsys.readouterr()
    if platform.uname().system != 'Windows':
        # This must be false due to the embedded ANSI codes.
        # But, see above re. Windows.
        assert 'Twine is a utility for publishing Python packages' not in out
    result = Text.from_ansi(out).plain
    # With the ANSI codes removed, this must be true.
    assert 'Twine is a utility for publishing Python packages' in result


def test_open():
    open_func = main.webbrowser.open
    try:
        main.webbrowser.open = _webbrowser_open_mock
        args = ArgumentsHolder()
        args.package = 'pytest'
        main.on_open(args)
        assert 'https://pypi.org/project/pytest/' == arguments
    finally:
        main.webbrowser.open = open_func


def _webbrowser_open_mock(url):
    global arguments
    arguments = url


def test_search(capsys):
    args = ArgumentsHolder()
    args.query = 'twine'
    args.num = 3
    main.on_search(args)
    out, _ = capsys.readouterr()
    assert 'Collection of utilities for publishing packages on PyPI' in out
    args.num = None
    main.on_search(args)
    out, _ = capsys.readouterr()
    assert 'Collection of utilities for publishing packages on PyPI' in out


def test_cli(capsys):
    sys.argv = ['qpp', '-h']
    with pytest.raises(SystemExit):
        cli()
    # Consume the screen output. We don't want it to mess up pytest's output.
    capsys.readouterr()
