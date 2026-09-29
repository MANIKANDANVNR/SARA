import sys

from tools.system_info_tool import SystemInfoTool


def test_system_info_tool_name():

    tool = SystemInfoTool()

    assert tool.name == "system_info"


def test_system_info_tool_description():

    tool = SystemInfoTool()

    assert isinstance(
        tool.description,
        str
    )

    assert tool.description


def test_system_info_returns_dictionary():

    tool = SystemInfoTool()

    result = tool.execute()

    assert isinstance(
        result,
        dict
    )


def test_system_info_contains_required_fields():

    tool = SystemInfoTool()

    result = tool.execute()

    required_fields = {
        "operating_system",
        "os_release",
        "os_version",
        "machine",
        "processor",
        "python_version",
        "architecture"
    }

    assert required_fields.issubset(
        result.keys()
    )


def test_system_info_values_are_strings():

    tool = SystemInfoTool()

    result = tool.execute()

    for value in result.values():

        assert isinstance(
            value,
            str
        )


def test_system_info_python_version_matches_runtime():

    tool = SystemInfoTool()

    result = tool.execute()

    expected = sys.version.split()[0]

    assert result["python_version"] == expected


def test_system_info_architecture_is_valid():

    tool = SystemInfoTool()

    result = tool.execute()

    assert result["architecture"] in {
        "32bit",
        "64bit"
    }


def test_system_info_operating_system_is_available():

    tool = SystemInfoTool()

    result = tool.execute()

    assert result["operating_system"]


def test_system_info_machine_is_available():

    tool = SystemInfoTool()

    result = tool.execute()

    assert result["machine"]


def test_system_info_does_not_require_arguments():

    tool = SystemInfoTool()

    result = tool.execute()

    assert result is not None