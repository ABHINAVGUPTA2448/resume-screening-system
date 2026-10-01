import re


# ============================================================
# 1. ROLE / JOB TITLE PATTERNS
# ============================================================

ROLE_PATTERNS = [

    # AI / ML
    (
        r"\bmachine\s+learning\s+engineer\b",
        "Machine Learning Engineer"
    ),
    (
        r"\bmachine\s+learning\s+intern\b",
        "Machine Learning Intern"
    ),
    (
        r"\bmachine\s+learning\s+developer\b",
        "Machine Learning Developer"
    ),
    (
        r"\bai\s+engineer\b",
        "AI Engineer"
    ),
    (
        r"\bartificial\s+intelligence\s+engineer\b",
        "AI Engineer"
    ),
    (
        r"\bdata\s+scientist\b",
        "Data Scientist"
    ),
    (
        r"\bdata\s+science\s+intern\b",
        "Data Science Intern"
    ),
    (
        r"\bdata\s+analyst\b",
        "Data Analyst"
    ),
    (
        r"\bml\s+engineer\b",
        "Machine Learning Engineer"
    ),

    # Software
    (
        r"\bsoftware\s+engineer\b",
        "Software Engineer"
    ),
    (
        r"\bsoftware\s+developer\b",
        "Software Developer"
    ),
    (
        r"\bsoftware\s+development\s+intern\b",
        "Software Development Intern"
    ),
    (
        r"\bbackend\s+developer\b",
        "Backend Developer"
    ),
    (
        r"\bbackend\s+engineer\b",
        "Backend Engineer"
    ),
    (
        r"\bfrontend\s+developer\b",
        "Frontend Developer"
    ),
    (
        r"\bfull\s*stack\s+developer\b",
        "Full Stack Developer"
    ),

    # Programming
    (
        r"\bpython\s+developer\b",
        "Python Developer"
    ),
    (
        r"\bpython\s+developer\s+intern\b",
        "Python Developer Intern"
    ),
    (
        r"\bjava\s+developer\b",
        "Java Developer"
    ),
    (
        r"\bc\+\+\s+developer\b",
        "C++ Developer"
    ),

    # Web
    (
        r"\bweb\s+developer\b",
        "Web Developer"
    ),
    (
        r"\bweb\s+development\s+intern\b",
        "Web Development Intern"
    ),

    # Data
    (
        r"\bdata\s+engineer\b",
        "Data Engineer"
    ),
    (
        r"\bbusiness\s+analyst\b",
        "Business Analyst"
    ),

    # Cloud / DevOps
    (
        r"\bdevops\s+engineer\b",
        "DevOps Engineer"
    ),
    (
        r"\bcloud\s+engineer\b",
        "Cloud Engineer"
    ),

    # Security
    (
        r"\bcyber\s+security\s+engineer\b",
        "Cyber Security Engineer"
    ),
    (
        r"\bsecurity\s+analyst\b",
        "Security Analyst"
    ),

    # General internships
    (
        r"\bsoftware\s+intern\b",
        "Software Intern"
    ),
    (
        r"\bengineering\s+intern\b",
        "Engineering Intern"
    ),
    (
        r"\bdeveloper\s+intern\b",
        "Developer Intern"
    ),
    (
        r"\bintern\b",
        "Intern"
    )
]


# ============================================================
# 2. ROLE EXTRACTION
# ============================================================

def extract_roles(text):
    """
    Extract job roles/titles from resume text.
    """

    if not text:

        return []

    roles = []

    seen = set()

    for pattern, role in ROLE_PATTERNS:

        matches = re.finditer(
            pattern,
            text,
            re.IGNORECASE
        )

        for match in matches:

            normalized_role = role

            if normalized_role not in seen:

                seen.add(
                    normalized_role
                )

                roles.append({
                    "role": normalized_role,
                    "matched_text": match.group(0),
                    "start": match.start(),
                    "end": match.end()
                })

    return roles


# ============================================================
# 3. PRIMARY ROLE
# ============================================================

def extract_primary_role(text):
    """
    Select the first detected role as the primary role.

    Later this will be improved using:
    - dates
    - seniority
    - relevance
    - experience duration
    """

    roles = extract_roles(text)

    if not roles:

        return "Not specified"

    return roles[0]["role"]


# ============================================================
# 4. ROLE CATEGORY
# ============================================================

def classify_role(role):

    if not role:

        return "Other"

    role_lower = role.lower()

    if any(
        keyword in role_lower
        for keyword in [
            "machine learning",
            "ai engineer",
            "artificial intelligence",
            "data scientist"
        ]
    ):

        return "AI/ML"

    if any(
        keyword in role_lower
        for keyword in [
            "data analyst",
            "data engineer",
            "business analyst"
        ]
    ):

        return "Data"

    if any(
        keyword in role_lower
        for keyword in [
            "software",
            "backend",
            "frontend",
            "full stack",
            "developer"
        ]
    ):

        return "Software Development"

    if any(
        keyword in role_lower
        for keyword in [
            "devops",
            "cloud"
        ]
    ):

        return "Cloud/DevOps"

    if any(
        keyword in role_lower
        for keyword in [
            "security",
            "cyber"
        ]
    ):

        return "Cyber Security"

    return "Other"


# ============================================================
# 5. COMPLETE ROLE PROFILE
# ============================================================

def build_role_profile(text):

    roles = extract_roles(text)

    primary_role = extract_primary_role(text)

    category = classify_role(
        primary_role
    )

    return {
        "roles": roles,
        "primary_role": primary_role,
        "category": category
    }


# ============================================================
# 6. TEST
# ============================================================

if __name__ == "__main__":

    sample_resume = """
    Abhinav Gupta

    EXPERIENCE

    Machine Learning Intern
    June 2025 - January 2026

    Python Developer Intern
    05/2024 - 11/2024

    Software Development Intern
    Jan 2024 - Mar 2024

    PROJECTS

    Built a machine learning based traffic
    congestion prediction system using Python
    and Scikit-learn.
    """

    profile = build_role_profile(
        sample_resume
    )

    print("\n" + "=" * 60)
    print("ROLE PROFILE")
    print("=" * 60)

    print("\nDetected Roles:")

    for role in profile["roles"]:

        print(
            f"  {role['role']}"
            f" → matched: {role['matched_text']}"
        )

    print(
        "\nPrimary Role:",
        profile["primary_role"]
    )

    print(
        "Role Category:",
        profile["category"]
    )