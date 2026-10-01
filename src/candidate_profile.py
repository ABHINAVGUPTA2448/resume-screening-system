import re
from datetime import datetime


# ============================================================
# EXPERIENCE SECTION
# ============================================================

EXPERIENCE_HEADINGS = [
    "experience",
    "work experience",
    "professional experience",
    "employment",
    "internship",
    "internships",
    "work history",
    "career history",
]

EXPERIENCE_STOP_HEADINGS = [
    "education",
    "academic background",
    "skills",
    "technical skills",
    "projects",
    "academic projects",
    "certifications",
    "certificates",
    "achievements",
    "awards",
    "publications",
    "languages",
    "interests",
    "hobbies",
    "references",
]


def normalize_text(text):
    """Normalize whitespace and line breaks."""

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    lines = []

    for line in text.split("\n"):
        line = re.sub(r"\s+", " ", line).strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def extract_experience_section(text):
    """
    Extract only the experience section from a resume.

    This prevents dates from education/project sections
    being incorrectly counted as work experience.
    """

    text = normalize_text(text)

    if not text:
        return ""

    lines = text.split("\n")

    start_index = None

    # Find experience heading
    for i, line in enumerate(lines):

        clean = line.lower().strip(" :-")

        if clean in EXPERIENCE_HEADINGS:
            start_index = i + 1
            break

    if start_index is None:
        return ""

    section_lines = []

    # Collect until next major section
    for line in lines[start_index:]:

        clean = line.lower().strip(" :-")

        if clean in EXPERIENCE_STOP_HEADINGS:
            break

        section_lines.append(line)

    return "\n".join(section_lines).strip()


# ============================================================
# DATE HELPERS
# ============================================================

MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,

    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "sept": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def month_to_number(month_name):
    """Convert month name/abbreviation to month number."""

    return MONTHS.get(month_name.lower().strip())


def months_between(start_year, start_month, end_year, end_month):
    """
    Calculate duration in months.

    Inclusive month calculation:
    June 2025 -> January 2026 = 8 months
    """

    return (end_year - start_year) * 12 + (end_month - start_month) + 1


def get_present_date():
    """Return current year and month."""

    now = datetime.now()

    return now.year, now.month


# ============================================================
# EXPERIENCE EXTRACTION
# ============================================================

def extract_experience(text):
    """
    Extract professional experience from resume.

    Supports:

    1. June 2025 - January 2026
    2. Jan 2024 - Mar 2024
    3. 05/2024 - 11/2024
    4. 2023 - 2025
    5. June 2025 - Present
    6. 2 years
    7. 1 year 6 months
    8. 8 months
    """

    section = extract_experience_section(text)

    if not section:
        return {
            "experiences": [],
            "total_experience_months": 0,
            "total_experience_years": 0.0,
        }

    experiences = []

    # --------------------------------------------------------
    # Pattern 1:
    # June 2025 - January 2026
    # Jan 2024 to Mar 2024
    # June 2025 - Present
    # --------------------------------------------------------

    month_name_pattern = re.compile(
        r"\b"
        r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|"
        r"Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|"
        r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
        r"\s+"
        r"(\d{4})"
        r"\s*"
        r"(?:-|–|—|to)\s*"
        r"(Present|Current|"
        r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|"
        r"Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|"
        r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
        r"\s+(\d{4}))"
        r"\b",
        re.IGNORECASE,
    )

    for match in month_name_pattern.finditer(section):

        start_month_name = match.group(1)
        start_year = int(match.group(2))

        end_part = match.group(3)

        start_month = month_to_number(start_month_name)

        if end_part.lower() in ["present", "current"]:
            end_year, end_month = get_present_date()
            end_display = "Present"
        else:
            end_month_name = match.group(4)
            end_year = int(match.group(5))
            end_month = month_to_number(end_month_name)
            end_display = f"{end_month_name} {end_year}"

        if start_month and end_month:

            duration = months_between(
                start_year,
                start_month,
                end_year,
                end_month,
            )

            if duration > 0:

                experiences.append({
                    "start": f"{start_month_name} {start_year}",
                    "end": end_display,
                    "months": duration,
                    "type": "date_range",
                })

    # --------------------------------------------------------
    # Pattern 2:
    # 05/2024 - 11/2024
    # 05/2024 to Present
    # --------------------------------------------------------

    numeric_pattern = re.compile(
        r"\b"
        r"(0?[1-9]|1[0-2])"
        r"[/-]"
        r"(\d{4})"
        r"\s*"
        r"(?:-|–|—|to)\s*"
        r"(Present|Current|"
        r"(0?[1-9]|1[0-2])[/-](\d{4}))"
        r"\b",
        re.IGNORECASE,
    )

    for match in numeric_pattern.finditer(section):

        start_month = int(match.group(1))
        start_year = int(match.group(2))

        end_part = match.group(3)

        if end_part.lower() in ["present", "current"]:

            end_year, end_month = get_present_date()
            end_display = "Present"

        else:

            end_month = int(match.group(4))
            end_year = int(match.group(5))

            end_display = f"{end_month:02d}/{end_year}"

        duration = months_between(
            start_year,
            start_month,
            end_year,
            end_month,
        )

        if duration > 0:

            experiences.append({
                "start": f"{start_month:02d}/{start_year}",
                "end": end_display,
                "months": duration,
                "type": "date_range",
            })

    # --------------------------------------------------------
    # Pattern 3:
    # 2023 - 2025
    # 2022 - Present
    # --------------------------------------------------------

    year_pattern = re.compile(
        r"\b"
        r"(20\d{2})"
        r"\s*"
        r"(?:-|–|—|to)\s*"
        r"(Present|Current|20\d{2})"
        r"\b",
        re.IGNORECASE,
    )

    for match in year_pattern.finditer(section):

        start_year = int(match.group(1))

        end_part = match.group(2)

        if end_part.lower() in ["present", "current"]:

            end_year, _ = get_present_date()

        else:

            end_year = int(end_part)

        duration = (end_year - start_year + 1) * 12

        if duration > 0:

            experiences.append({
                "start": str(start_year),
                "end": "Present" if end_part.lower() in ["present", "current"] else str(end_year),
                "months": duration,
                "type": "year_range",
            })

    # --------------------------------------------------------
    # Pattern 4:
    # Explicit duration
    # "2 years"
    # "1 year 6 months"
    # "8 months"
    # --------------------------------------------------------

    duration_pattern = re.compile(
        r"\b"
        r"(?:(\d+(?:\.\d+)?)\s*years?)?"
        r"\s*"
        r"(?:(\d+)\s*months?)?"
        r"\b",
        re.IGNORECASE,
    )

    for match in duration_pattern.finditer(section):

        years_value = match.group(1)
        months_value = match.group(2)

        if not years_value and not months_value:
            continue

        # Avoid accidentally treating date numbers as durations
        start_pos = match.start()
        end_pos = match.end()

        surrounding = section[max(0, start_pos - 15):min(len(section), end_pos + 15)]

        if re.search(r"\d{4}", surrounding):
            continue

        years = float(years_value) if years_value else 0
        months = int(months_value) if months_value else 0

        total_months = round(years * 12) + months

        if total_months > 0:

            experiences.append({
                "start": None,
                "end": None,
                "months": total_months,
                "type": "explicit_duration",
            })

    # --------------------------------------------------------
    # Remove duplicate experiences
    # --------------------------------------------------------

    unique = []

    seen = set()

    for experience in experiences:

        key = (
            experience["start"],
            experience["end"],
            experience["months"],
            experience["type"],
        )

        if key not in seen:

            seen.add(key)
            unique.append(experience)

    experiences = unique

    # --------------------------------------------------------
    # IMPORTANT:
    # Avoid double counting overlapping date ranges.
    #
    # For now, date ranges are treated as independent
    # unless they have exactly the same dates.
    # --------------------------------------------------------

    total_months = sum(
        experience["months"]
        for experience in experiences
    )

    total_years = round(total_months / 12, 2)

    return {
        "experiences": experiences,
        "total_experience_months": total_months,
        "total_experience_years": total_years,
    }


# ============================================================
# EDUCATION EXTRACTION
# ============================================================

DEGREE_PATTERNS = [
    ("B.Tech", r"\bB\.?\s*Tech\b|\bBTech\b"),
    ("B.E", r"\bB\.?\s*E\.?\b"),
    ("B.Sc", r"\bB\.?\s*Sc\.?\b"),
    ("BCA", r"\bBCA\b"),
    ("M.Tech", r"\bM\.?\s*Tech\b|\bMTech\b"),
    ("MCA", r"\bMCA\b"),
    ("M.Sc", r"\bM\.?\s*Sc\.?\b"),
    ("MBA", r"\bMBA\b"),
]


FIELD_PATTERNS = [
    ("Computer Science", r"\bcomputer science\b|\bcse\b"),
    ("Information Technology", r"\binformation technology\b|\bit\b"),
    ("Data Science", r"\bdata science\b"),
    ("Artificial Intelligence", r"\bartificial intelligence\b"),
    ("Machine Learning", r"\bmachine learning\b"),
    ("Electronics", r"\belectronics\b"),
    ("Electrical", r"\belectrical\b"),
    ("Mechanical", r"\bmechanical\b"),
    ("Civil", r"\bcivil\b"),
]


def extract_education(text):
    """Extract highest degree and fields from resume."""

    text_lower = normalize_text(text).lower()

    degrees = []
    fields = []

    for degree_name, pattern in DEGREE_PATTERNS:

        if re.search(pattern, text_lower, re.IGNORECASE):
            degrees.append(degree_name)

    for field_name, pattern in FIELD_PATTERNS:

        if re.search(pattern, text_lower, re.IGNORECASE):
            fields.append(field_name)

    return {
        "degrees": sorted(set(degrees)),
        "fields": sorted(set(fields)),
    }


# ============================================================
# COMPLETE CANDIDATE PROFILE
# ============================================================

def build_candidate_profile(text):
    """
    Build complete candidate profile.

    This function intentionally exposes both:
        total_experience_years
        total_experience_months

    so downstream modules can reliably consume the result.
    """

    experience = extract_experience(text)

    education = extract_education(text)

    return {
        "experience": experience["experiences"],
        "experiences": experience["experiences"],

        "total_experience_months": experience[
            "total_experience_months"
        ],

        "total_experience_years": experience[
            "total_experience_years"
        ],

        # Backward-compatible key
        "experience_years": experience[
            "total_experience_years"
        ],

        "education": education,
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sample_resume = """
    Abhinav Gupta

    EXPERIENCE

    Machine Learning Intern
    June 2025 - January 2026

    Data Science Intern
    05/2024 - 11/2024

    Software Development Intern
    Jan 2024 - Mar 2024

    EDUCATION

    B.Tech Computer Science
    ABES Engineering College

    SKILLS

    Python
    Machine Learning
    SQL
    """

    profile = build_candidate_profile(sample_resume)

    print("=" * 60)
    print("CANDIDATE PROFILE")
    print("=" * 60)

    print("\nEXPERIENCE:")

    for experience in profile["experience"]:

        print(
            f"  {experience['start']} - "
            f"{experience['end']} → "
            f"{experience['months']} months "
            f"[{experience['type']}]"
        )

    print(
        f"\nTotal Professional Experience: "
        f"{profile['total_experience_years']} years"
    )

    print(
        f"Total Experience Months: "
        f"{profile['total_experience_months']}"
    )

    print("\nEDUCATION:")

    print(
        "  Degrees:",
        ", ".join(profile["education"]["degrees"])
    )

    print(
        "  Fields:",
        ", ".join(profile["education"]["fields"])
    )