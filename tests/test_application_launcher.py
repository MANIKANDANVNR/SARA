import pytest

from tools.application_launcher import (
    ApplicationLauncher
)


class FakeProcess:

    pid = 12345


def test_launcher_has_correct_name():

    tool = ApplicationLauncher()

    assert tool.name == "application_launcher"


def test_launcher_has_description():

    tool = ApplicationLauncher()

    assert (
        "approved desktop applications"
        in tool.description
    )


def test_allowed_application_is_accepted():

    tool = ApplicationLauncher()

    assert "notepad" in tool.APPLICATIONS
    assert "calculator" in tool.APPLICATIONS
    assert "explorer" in tool.APPLICATIONS
    assert "chrome" in tool.APPLICATIONS
    assert "vscode" in tool.APPLICATIONS
    assert "pycharm" in tool.APPLICATIONS


def test_application_name_is_case_insensitive():

    tool = ApplicationLauncher()

    assert "chrome" in tool.APPLICATIONS


def test_empty_application_is_rejected():

    tool = ApplicationLauncher()

    with pytest.raises(
        ValueError,
        match="Application name cannot be empty"
    ):

        tool.execute("")


def test_none_application_is_rejected():

    tool = ApplicationLauncher()

    with pytest.raises(
        ValueError,
        match="Application name cannot be empty"
    ):

        tool.execute(None)


def test_unknown_application_is_rejected():

    tool = ApplicationLauncher()

    with pytest.raises(
        ValueError,
        match="is not allowed"
    ):

        tool.execute(
            "unknown_application"
        )


def test_arbitrary_executable_path_is_rejected():

    tool = ApplicationLauncher()

    with pytest.raises(
        ValueError,
        match="is not allowed"
    ):

        tool.execute(
            r"C:\Windows\System32\cmd.exe"
        )


def test_application_commands_do_not_use_shell():

    tool = ApplicationLauncher()

    for configuration in (
        tool.APPLICATIONS.values()
    ):

        command = configuration[
            "command"
        ]

        assert isinstance(
            command,
            list
        )


def test_launch_uses_subprocess_without_shell(
    monkeypatch
):

    tool = ApplicationLauncher()

    captured = {}

    def fake_popen(
        command,
        shell,
        stdout,
        stderr
    ):

        captured["command"] = command
        captured["shell"] = shell
        captured["stdout"] = stdout
        captured["stderr"] = stderr

        return FakeProcess()

    monkeypatch.setattr(
        "tools.application_launcher.subprocess.Popen",
        fake_popen
    )

    result = tool.execute(
        "notepad"
    )

    assert result["application"] == "notepad"
    assert result["pid"] == 12345
    assert result["launched"] is True

    assert captured["command"] == [
        "notepad.exe"
    ]

    assert captured["shell"] is False


def test_launch_failure_is_reported(
    monkeypatch
):

    tool = ApplicationLauncher()

    def fake_popen(
        command,
        shell,
        stdout,
        stderr
    ):

        raise FileNotFoundError()

    monkeypatch.setattr(
        "tools.application_launcher.subprocess.Popen",
        fake_popen
    )

    with pytest.raises(
        RuntimeError,
        match="Unable to launch"
    ):

        tool.execute(
            "notepad"
        )


def test_os_error_is_reported(
    monkeypatch
):

    tool = ApplicationLauncher()

    def fake_popen(
        command,
        shell,
        stdout,
        stderr
    ):

        raise OSError()

    monkeypatch.setattr(
        "tools.application_launcher.subprocess.Popen",
        fake_popen
    )

    with pytest.raises(
        RuntimeError,
        match="Unable to launch"
    ):

        tool.execute(
            "notepad"
        )


def test_whitespace_is_removed():

    tool = ApplicationLauncher()

    monkeypatch_result = tool.APPLICATIONS.get(
        "notepad"
    )

    assert monkeypatch_result is not None