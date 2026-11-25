CRITICAL_KEYWORDS = ["crash", "data loss" , "security" , "500"]
MAJOR_KEYWORDS = ["error", "fail" , "broken" , "timeout"]

def guess_severity(title: str) -> str:
    text = title.lower()

    for keyword in CRITICAL_KEYWORDS:
        if keyword in text:
            return "critical"

    for keyword in MAJOR_KEYWORDS:
        if keyword in text:
            return "major"

    return "minor"

def count_by_severity(titles: list[str]) -> dict[str, int]:
    counts = {"critical": 0, "major": 0, "minor": 0}

    for title in titles:
        severity = guess_severity(title)
        counts[severity] += 1

    return counts