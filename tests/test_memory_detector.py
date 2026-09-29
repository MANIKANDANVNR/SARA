from core.memory_detector import (
    MemoryDetector
)


def test_personal_memory_detection():

    detector = MemoryDetector()

    result = detector.detect(
        "My name is Mani."
    )

    assert result is not None
    assert result["important"] is True
    assert result["category"] == "personal"
    assert result["content"] == "My name is Mani."


def test_technical_memory_detection():

    detector = MemoryDetector()

    result = detector.detect(
        "I am learning Python."
    )

    assert result is not None
    assert result["important"] is True
    assert result["category"] == "technical"


def test_preference_memory_detection():

    detector = MemoryDetector()

    result = detector.detect(
        "I like dark mode."
    )

    assert result is not None
    assert result["important"] is True
    assert result["category"] == "preferences"


def test_career_memory_detection():

    detector = MemoryDetector()

    result = detector.detect(
        "I want a Python developer job."
    )

    assert result is not None
    assert result["important"] is True
    assert result["category"] == "career"


def test_project_memory_detection():

    detector = MemoryDetector()

    result = detector.detect(
        "I am building SARA."
    )

    assert result is not None
    assert result["important"] is True
    assert result["category"] == "projects"


def test_normal_question_is_not_memory():

    detector = MemoryDetector()

    result = detector.detect(
        "What is Python?"
    )

    assert result is None


def test_casual_message_is_not_memory():

    detector = MemoryDetector()

    result = detector.detect(
        "Tell me a joke."
    )

    assert result is None


def test_empty_content_is_not_memory():

    detector = MemoryDetector()

    assert detector.detect("") is None
    assert detector.detect(None) is None


def test_is_important():

    detector = MemoryDetector()

    assert detector.is_important(
        "My name is Mani."
    ) is True

    assert detector.is_important(
        "What is Python?"
    ) is False


def test_detect_category():

    detector = MemoryDetector()

    assert (
        detector.detect_category(
            "I am learning Python."
        )
        == "technical"
    )

    assert (
        detector.detect_category(
            "What is Python?"
        )
        == "general"
    )

def test_memory_question_with_important_pattern_is_not_memory():

    detector = MemoryDetector()

    result = detector.detect(
        "What is my favorite programming language?"
    )

    assert result is None


def test_memory_forget_command_with_important_pattern_is_not_memory():

    detector = MemoryDetector()

    result = detector.detect(
        "Forget my favorite programming language."
    )

    assert result is None


def test_memory_recall_command_with_important_pattern_is_not_memory():

    detector = MemoryDetector()

    result = detector.detect(
        "Recall my favorite programming language."
    )

    assert result is None


def test_memory_question_about_personal_information_is_not_memory():

    detector = MemoryDetector()

    result = detector.detect(
        "What is my name?"
    )

    assert result is None


def test_memory_question_about_career_is_not_memory():

    detector = MemoryDetector()

    result = detector.detect(
        "What is my current job?"
    )

    assert result is None


def test_memory_statement_with_favorite_pattern_remains_memory():

    detector = MemoryDetector()

    result = detector.detect(
        "My favorite programming language is Python."
    )

    assert result is not None
    assert result["important"] is True
    assert result["category"] == "preferences"


def test_memory_statement_with_personal_pattern_remains_memory():

    detector = MemoryDetector()

    result = detector.detect(
        "My name is Mani."
    )

    assert result is not None
    assert result["important"] is True
    assert result["category"] == "personal"