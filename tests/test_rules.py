import pytest

from bug_severity_classifier.rules import guess_severity, count_by_severity



def test_crash_is_critical() -> None:
    assert guess_severity("App crash on login") == "critical"


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("App CRASH on login", "critical"),
        ("Security hole in API", "critical"),
        ("Login button broken", "major"),
        ("Request timeout on search", "major"),
        ("Typo in footer", "minor"),
        ("Crash after error message", "critical"),
    ],
)
def test_guess_severity(title: str, expected: str) -> None:
    assert guess_severity(title) == expected

def test_count_by_severity() -> None:
    titles = ["App crash", "Login broken", "Typo in footer", "Data loss on save"]
    assert count_by_severity(titles) == {"critical": 2, "major": 1, "minor": 1}


def test_count_by_severity_empty_list() -> None:
    assert count_by_severity([]) == {"critical": 0, "major": 0, "minor": 0}