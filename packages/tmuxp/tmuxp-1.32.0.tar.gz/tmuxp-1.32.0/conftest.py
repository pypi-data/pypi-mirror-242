"""Conftest.py (root-level)

We keep this in root pytest fixtures in pytest's doctest plugin to be available, as well
as avoiding conftest.py from being included in the wheel.
"""
import logging
import os
import pathlib
import shutil
import typing as t

import pytest
from _pytest.doctest import DoctestItem
from libtmux.test import namer

from tests.fixtures import utils as test_utils
from tmuxp.workspace.finders import get_workspace_dir

if t.TYPE_CHECKING:
    from libtmux.session import Session

logger = logging.getLogger(__name__)
USING_ZSH = "zsh" in os.getenv("SHELL", "")


@pytest.mark.skipif(not USING_ZSH, reason="Using ZSH")
@pytest.fixture(autouse=USING_ZSH, scope="session")
def zshrc(user_path: pathlib.Path) -> pathlib.Path:
    """This quiets ZSH default message.

    Needs a startup file .zshenv, .zprofile, .zshrc, .zlogin.
    """
    p = user_path / ".zshrc"
    p.touch()
    return p


@pytest.fixture(autouse=True)
def home_path_default(monkeypatch: pytest.MonkeyPatch, user_path: pathlib.Path) -> None:
    monkeypatch.setenv("HOME", str(user_path))


@pytest.fixture
def tmuxp_configdir(user_path: pathlib.Path) -> pathlib.Path:
    xdg_config_dir = user_path / ".config"
    xdg_config_dir.mkdir(exist_ok=True)

    tmuxp_configdir = xdg_config_dir / "tmuxp"
    tmuxp_configdir.mkdir(exist_ok=True)
    return tmuxp_configdir


@pytest.fixture
def tmuxp_configdir_default(
    monkeypatch: pytest.MonkeyPatch, tmuxp_configdir: pathlib.Path
) -> None:
    monkeypatch.setenv("TMUXP_CONFIGDIR", str(tmuxp_configdir))
    assert get_workspace_dir() == str(tmuxp_configdir)


@pytest.fixture(scope="function")
def monkeypatch_plugin_test_packages(monkeypatch: pytest.MonkeyPatch) -> None:
    paths = [
        "tests/fixtures/pluginsystem/plugins/tmuxp_test_plugin_bwb/",
        "tests/fixtures/pluginsystem/plugins/tmuxp_test_plugin_bs/",
        "tests/fixtures/pluginsystem/plugins/tmuxp_test_plugin_r/",
        "tests/fixtures/pluginsystem/plugins/tmuxp_test_plugin_owc/",
        "tests/fixtures/pluginsystem/plugins/tmuxp_test_plugin_awf/",
        "tests/fixtures/pluginsystem/plugins/tmuxp_test_plugin_fail/",
    ]
    for path in paths:
        monkeypatch.syspath_prepend(str(pathlib.Path(path).resolve()))


@pytest.fixture(scope="function")
def session_params(session_params: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
    session_params.update({"x": 800, "y": 600})
    return session_params


@pytest.fixture(scope="function")
def socket_name(request: pytest.FixtureRequest) -> str:
    return "tmuxp_test%s" % next(namer)


@pytest.fixture(autouse=True)
def add_doctest_fixtures(
    request: pytest.FixtureRequest,
    doctest_namespace: t.Dict[str, t.Any],
    tmp_path: pathlib.Path,
) -> None:
    if isinstance(request._pyfuncitem, DoctestItem) and shutil.which("tmux"):
        doctest_namespace["server"] = request.getfixturevalue("server")
        session: "Session" = request.getfixturevalue("session")
        doctest_namespace["session"] = session
        doctest_namespace["window"] = session.attached_window
        doctest_namespace["pane"] = session.attached_pane
        doctest_namespace["test_utils"] = test_utils
        doctest_namespace["tmp_path"] = tmp_path
