from unittest.mock import Mock

from core.controller import SaraController
from core.intent import IntentType
from core.state import SaraState
from security.security_manager import SecurityManager


def create_controller():
    state = SaraState()

    security = SecurityManager(
        state
    )

    controller = SaraController(
        sara=Mock(),
        state=state,
        security=security,
        brain=Mock(),
        memory=Mock(),
        context=Mock(),
        conversation=Mock(),
        memory_store=Mock(),
        conversation_store=Mock(),
        profile=Mock(),
        profile_store=Mock(),
        tools=Mock(),
        voice=Mock(),
        ui=Mock()
    )

    return controller


def test_handle_system_info_success():

    controller = create_controller()

    tool = Mock()

    tool.execute.return_value = {
        "operating_system": "Windows",
        "os_release": "11",
        "os_version": "10.0.26200",
        "machine": "AMD64",
        "processor": "Intel",
        "python_version": "3.12.10",
        "architecture": "64bit"
    }

    controller.tool_exists = Mock(
        return_value=True
    )

    controller.get_tool = Mock(
        return_value=tool
    )

    result = controller.handle_system_info()

    assert "SYSTEM INFORMATION" in result
    assert "Operating System: Windows" in result
    assert "OS Release: 11" in result
    assert "OS Version: 10.0.26200" in result
    assert "Machine: AMD64" in result
    assert "Processor: Intel" in result
    assert "Architecture: 64bit" in result
    assert "Python Version: 3.12.10" in result

    tool.execute.assert_called_once()


def test_handle_system_info_emergency_shutdown():

    controller = create_controller()

    controller.state.emergency_shutdown = True

    result = controller.handle_system_info()

    assert result == (
        "Permission denied. "
        "Emergency shutdown is active."
    )


def test_handle_system_info_tool_not_found():

    controller = create_controller()

    controller.tool_exists = Mock(
        return_value=False
    )

    result = controller.handle_system_info()

    assert result == (
        "System Info tool is unavailable."
    )


def test_handle_system_info_tool_failure():

    controller = create_controller()

    tool = Mock()

    tool.execute.side_effect = RuntimeError(
        "system info failure"
    )

    controller.tool_exists = Mock(
        return_value=True
    )

    controller.get_tool = Mock(
        return_value=tool
    )

    result = controller.handle_system_info()

    assert result == (
        "System Info request failed: "
        "system info failure"
    )


def test_handle_system_info_invalid_response_type():

    controller = create_controller()

    tool = Mock()

    tool.execute.return_value = (
        "invalid response"
    )

    controller.tool_exists = Mock(
        return_value=True
    )

    controller.get_tool = Mock(
        return_value=tool
    )

    result = controller.handle_system_info()

    assert result == (
        "Invalid System Info tool response."
    )


def test_handle_system_info_missing_operating_system():

    controller = create_controller()

    tool = Mock()

    tool.execute.return_value = {
        "os_release": "11",
        "os_version": "10.0",
        "machine": "AMD64",
        "processor": "Intel",
        "python_version": "3.12.10",
        "architecture": "64bit"
    }

    controller.tool_exists = Mock(
        return_value=True
    )

    controller.get_tool = Mock(
        return_value=tool
    )

    result = controller.handle_system_info()

    assert result == (
        "Invalid System Info tool response."
    )


def test_handle_system_info_missing_os_release():

    controller = create_controller()

    tool = Mock()

    tool.execute.return_value = {
        "operating_system": "Windows",
        "os_version": "10.0",
        "machine": "AMD64",
        "processor": "Intel",
        "python_version": "3.12.10",
        "architecture": "64bit"
    }

    controller.tool_exists = Mock(
        return_value=True
    )

    controller.get_tool = Mock(
        return_value=tool
    )

    result = controller.handle_system_info()

    assert result == (
        "Invalid System Info tool response."
    )


def test_handle_system_info_missing_python_version():

    controller = create_controller()

    tool = Mock()

    tool.execute.return_value = {
        "operating_system": "Windows",
        "os_release": "11",
        "os_version": "10.0",
        "machine": "AMD64",
        "processor": "Intel",
        "architecture": "64bit"
    }

    controller.tool_exists = Mock(
        return_value=True
    )

    controller.get_tool = Mock(
        return_value=tool
    )

    result = controller.handle_system_info()

    assert result == (
        "Invalid System Info tool response."
    )


def test_handle_system_info_missing_processor_uses_unknown():

    controller = create_controller()

    tool = Mock()

    tool.execute.return_value = {
        "operating_system": "Windows",
        "os_release": "11",
        "os_version": "10.0",
        "machine": "AMD64",
        "processor": "",
        "python_version": "3.12.10",
        "architecture": "64bit"
    }

    controller.tool_exists = Mock(
        return_value=True
    )

    controller.get_tool = Mock(
        return_value=tool
    )

    result = controller.handle_system_info()

    assert "Processor: Unknown" in result


def test_handle_system_info_calls_tool_only_when_available():

    controller = create_controller()

    controller.tool_exists = Mock(
        return_value=False
    )

    controller.get_tool = Mock()

    result = controller.handle_system_info()

    assert result == (
        "System Info tool is unavailable."
    )

    controller.get_tool.assert_not_called()