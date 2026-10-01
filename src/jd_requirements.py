import re


# ============================================================
# 1. EXPERIENCE REQUIREMENT EXTRACTION
# ============================================================

def extract_required_experience(jd_text):
    """
    Extract experience requirements from a job description.

    Examples:

        2 years of experience
        1+ years experience
        minimum 2 years
        3-5 years of experience
        0-2 years
        freshers welcome
    """

    if not jd_text:
        return {
            "min_years": 0.0,
            "max_years": None,
            "raw": None,
            "type": "not_specified"
        }

    text = jd_text.lower()

    # --------------------------------------------------------
    # Freshers
    # --------------------------------------------------------

    fresher_patterns = [
        r"\bfreshers?\b",
        r"\bno\s+experience\s+required\b",
        r"\b0\s*(?:-\s*)?1\s*years?\b"
    ]

    for pattern in fresher_patterns:

        if re.search(pattern, text):

            return {
                "min_years": 0.0,
                "max_years": 1.0,
                "raw": "Fresher / 0-1 years",
                "type": "fresher"
            }

    # --------------------------------------------------------
    # Range
    # Example: 2-4 years
    # --------------------------------------------------------

    range_pattern = (
        r"\b"
        r"(\d+(?:\.\d+)?)"
        r"\s*(?:-|–|—|to)"
        r"\s*"
        r"(\d+(?:\.\d+)?)"
        r"\s*"
        r"(?:\+?\s*)?"
        r"years?"
    )

    match = re.search(
        range_pattern,
        text,
        re.IGNORECASE
    )

    if match:

        min_years = float(
            match.group(1)
        )

        max_years = float(
            match.group(2)
        )

        return {
            "min_years": min_years,
            "max_years": max_years,
            "raw": match.group(0),
            "type": "range"
        }

    # --------------------------------------------------------
    # Plus requirement
    # Example:
    # 2+ years
    # 3+ years of experience
    # --------------------------------------------------------

    plus_pattern = (
        r"\b"
        r"(\d+(?:\.\d+)?)"
        r"\s*\+\s*"
        r"years?"
    )

    match = re.search(
        plus_pattern,
        text,
        re.IGNORECASE
    )

    if match:

        min_years = float(
            match.group(1)
        )

        return {
            "min_years": min_years,
            "max_years": None,
            "raw": match.group(0),
            "type": "minimum"
        }

    # --------------------------------------------------------
    # Minimum requirement
    # Example:
    # minimum 2 years
    # at least 2 years
    # --------------------------------------------------------

    minimum_pattern = (
        r"(?:"
        r"minimum"
        r"|at\s+least"
        r"|more\s+than"
        r")"
        r"\s+"
        r"(\d+(?:\.\d+)?)"
        r"\s*"
        r"years?"
    )

    match = re.search(
        minimum_pattern,
        text,
        re.IGNORECASE
    )

    if match:

        min_years = float(
            match.group(1)
        )

        return {
            "min_years": min_years,
            "max_years": None,
            "raw": match.group(0),
            "type": "minimum"
        }

    # --------------------------------------------------------
    # Simple requirement
    # Example:
    # 2 years of experience
    # --------------------------------------------------------

    simple_pattern = (
        r"\b"
        r"(\d+(?:\.\d+)?)"
        r"\s*"
        r"years?"
        r"\s+"
        r"(?:of\s+)?"
        r"experience\b"
    )

    match = re.search(
        simple_pattern,
        text,
        re.IGNORECASE
    )

    if match:

        min_years = float(
            match.group(1)
        )

        return {
            "min_years": min_years,
            "max_years": None,
            "raw": match.group(0),
            "type": "minimum"
        }

    # --------------------------------------------------------
    # Nothing found
    # --------------------------------------------------------

    return {
        "min_years": 0.0,
        "max_years": None,
        "raw": None,
        "type": "not_specified"
    }


# ============================================================
# 2. EXPERIENCE MATCHING
# ============================================================

def calculate_experience_match(
    candidate_years,
    requirement
):
    """
    Compare candidate experience with JD requirement.

    Returns:
        score
        status
    """

    if not requirement:

        return {
            "score": 100.0,
            "status": "NOT_SPECIFIED"
        }

    min_years = requirement.get(
        "min_years",
        0.0
    )

    max_years = requirement.get(
        "max_years"
    )

    # --------------------------------------------------------
    # No minimum requirement
    # --------------------------------------------------------

    if min_years <= 0:

        return {
            "score": 100.0,
            "status": "MEETS_REQUIREMENT"
        }

    # --------------------------------------------------------
    # Candidate meets minimum
    # --------------------------------------------------------

    if candidate_years >= min_years:

        if (
            max_years is not None
            and candidate_years > max_years
        ):

            return {
                "score": 100.0,
                "status": "ABOVE_RANGE"
            }

        return {
            "score": 100.0,
            "status": "MEETS_REQUIREMENT"
        }

    # --------------------------------------------------------
    # Candidate has less experience
    # --------------------------------------------------------

    score = (
        candidate_years
        / min_years
    ) * 100

    score = min(
        round(score, 2),
        100.0
    )

    return {
        "score": score,
        "status": "BELOW_REQUIREMENT"
    }


# ============================================================
# 3. COMPLETE JD REQUIREMENTS
# ============================================================

def extract_jd_requirements(jd_text):

    experience = extract_required_experience(
        jd_text
    )

    return {
        "experience": experience
    }


# ============================================================
# 4. TEST
# ============================================================

if __name__ == "__main__":

    sample_jd = """
    Junior Machine Learning Engineer

    We are looking for a Junior Machine Learning Engineer.

    Candidates should have at least 1 year
    of experience working with machine learning.

    Required Skills:
    Python
    Machine Learning
    Pandas
    NumPy
    Scikit-learn
    SQL
    """

    requirements = extract_jd_requirements(
        sample_jd
    )

    print("\n" + "=" * 60)
    print("JOB REQUIREMENTS")
    print("=" * 60)

    experience = requirements[
        "experience"
    ]

    print(
        "\nMinimum Experience:",
        experience["min_years"],
        "years"
    )

    print(
        "Maximum Experience:",
        experience["max_years"]
    )

    print(
        "Raw Requirement:",
        experience["raw"]
    )

    print(
        "Requirement Type:",
        experience["type"]
    )

    # Test candidate

    candidate_years = 0.8

    result = calculate_experience_match(
        candidate_years,
        experience
    )

    print(
        "\nCandidate Experience:",
        candidate_years,
        "years"
    )

    print(
        "Experience Score:",
        result["score"],
        "%"
    )

    print(
        "Status:",
        result["status"]
    )