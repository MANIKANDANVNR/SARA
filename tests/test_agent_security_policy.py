from agent.security_policy import (
    AgentSecurityPolicy
)

from security.permission import (
    PermissionType,
    PermissionLevel
)


def test_policy_requires_known_tool():

    policy = AgentSecurityPolicy()

    assert policy.get_policy(
        "unknown_tool"
    ) is None


def test_calculator_policy():

    policy = AgentSecurityPolicy()

    result = policy.get_policy(
        "calculator"
    )

    assert result[
        "permission_type"
    ] == PermissionType.CALCULATOR

    assert result[
        "level"
    ] == PermissionLevel.LOW


def test_file_write_policy():

    policy = AgentSecurityPolicy()

    result = policy.get_policy(
        "file_write"
    )

    assert result[
        "permission_type"
    ] == PermissionType.WRITE_FILE

    assert result[
        "level"
    ] == PermissionLevel.LOW

    assert result[
        "resource_argument"
    ] == "path"


def test_python_policy():

    policy = AgentSecurityPolicy()

    assert policy.get_permission_type(
        "python"
    ) == PermissionType.PYTHON

    assert policy.get_level(
        "python"
    ) == PermissionLevel.LOW


def test_web_search_policy():

    policy = AgentSecurityPolicy()

    assert policy.get_permission_type(
        "web_search"
    ) == PermissionType.INTERNET

    assert policy.get_level(
        "web_search"
    ) == PermissionLevel.MEDIUM


def test_application_launcher_policy():

    policy = AgentSecurityPolicy()

    assert policy.get_permission_type(
        "application_launcher"
    ) == PermissionType.SYSTEM

    assert policy.get_level(
        "application_launcher"
    ) == PermissionLevel.MEDIUM


def test_file_resource_is_taken_from_arguments():

    policy = AgentSecurityPolicy()

    resource = policy.get_resource(
        "file_write",
        {
            "path": "test.txt",
            "content": "hello"
        }
    )

    assert resource == "test.txt"


def test_non_resource_tool_has_no_resource():

    policy = AgentSecurityPolicy()

    resource = policy.get_resource(
        "calculator",
        {
            "expression": "25 * 4"
        }
    )

    assert resource is None


def test_invalid_arguments_have_no_resource():

    policy = AgentSecurityPolicy()

    assert policy.get_resource(
        "file_write",
        None
    ) is None


def test_policy_returns_copy():

    policy = AgentSecurityPolicy()

    first = policy.get_policy(
        "calculator"
    )

    first["level"] = PermissionLevel.CRITICAL

    second = policy.get_policy(
        "calculator"
    )

    assert second[
        "level"
    ] == PermissionLevel.LOW


def test_get_resource_strips_whitespace():

    policy = AgentSecurityPolicy()

    assert policy.get_resource(
        "file_write",
        {
            "path": " test.txt "
        }
    ) == "test.txt"


def test_get_resource_rejects_empty_resource():

    policy = AgentSecurityPolicy()

    assert policy.get_resource(
        "file_write",
        {
            "path": "   "
        }
    ) is None


def test_policy_normalizes_tool_name():

    policy = AgentSecurityPolicy()

    result = policy.get_policy(
        " Calculator "
    )

    assert result is not None

    assert result[
        "permission_type"
    ] == PermissionType.CALCULATOR


def test_resource_normalizes_tool_name():

    policy = AgentSecurityPolicy()

    resource = policy.get_resource(
        " File_Write ",
        {
            "path": "test.txt"
        }
    )

    assert resource == "test.txt"
