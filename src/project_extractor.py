import re


# ============================================================
# PROJECT CATEGORIES
# ============================================================

PROJECT_CATEGORIES = {
    "AI/ML": [
        "machine learning",
        "artificial intelligence",
        "deep learning",
        "natural language processing",
        "nlp",
        "computer vision",
        "tensorflow",
        "pytorch",
        "scikit-learn",
    ],

    "Data": [
        "data analysis",
        "data science",
        "data engineering",
        "analytics",
        "statistics",
        "pandas",
        "numpy",
        "sql",
    ],

    "Web Development": [
        "web development",
        "web application",
        "frontend",
        "backend",
        "full stack",
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
    ],

    "Mobile Development": [
        "android",
        "ios",
        "mobile development",
        "flutter",
        "react native",
        "kotlin",
        "swift",
    ],

    "Cloud/DevOps": [
        "cloud",
        "devops",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "ci/cd",
    ],

    "Cyber Security": [
        "cyber security",
        "cybersecurity",
        "security",
        "penetration testing",
        "network security",
        "ethical hacking",
        "vulnerability",
    ],

    "IoT": [
        "iot",
        "internet of things",
        "arduino",
        "raspberry pi",
        "embedded",
        "sensors",
    ],
}


# ============================================================
# HEADINGS
# ============================================================

PROJECT_HEADINGS = {
    "projects",
    "academic projects",
    "personal projects",
    "key projects",
    "relevant projects",
    "major projects",
    "project experience",
}

STOP_HEADINGS = {
    "experience",
    "work experience",
    "professional experience",
    "education",
    "skills",
    "technical skills",
    "certifications",
    "certificates",
    "achievements",
    "awards",
    "publications",
    "languages",
    "interests",
    "hobbies",
    "references",
}


# ============================================================
# DESCRIPTION START WORDS
# ============================================================

DESCRIPTION_START_WORDS = {
    "developed",
    "built",
    "created",
    "designed",
    "implemented",
    "developing",
    "building",
    "used",
    "using",
    "worked",
    "working",
    "performed",
    "conducted",
    "applied",
    "integrated",
    "deployed",
    "analyzed",
    "develop",
    "build",
    "create",
    "design",
    "implement",
    "with",
    "features",
}


# ============================================================
# TEXT UTILITIES
# ============================================================

def normalize_line(line):
    """Clean a single line."""

    if not line:
        return ""

    line = line.strip()

    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line


def normalize_text(text):
    """Normalize complete text."""

    if not text:
        return ""

    text = text.replace(
        "\r",
        "\n"
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# ============================================================
# PROJECT SECTION
# ============================================================

def extract_project_section(text):
    """
    Extract only the Projects section.
    """

    text = normalize_text(text)

    if not text:
        return ""

    lines = text.splitlines()

    start_index = None

    for i, line in enumerate(lines):

        clean = normalize_line(
            line
        ).lower()

        clean = re.sub(
            r"[:\-]+$",
            "",
            clean
        )

        if clean in PROJECT_HEADINGS:

            start_index = i + 1

            break

    if start_index is None:
        return ""

    collected = []

    for line in lines[start_index:]:

        clean = normalize_line(
            line
        )

        heading = clean.lower()

        heading = re.sub(
            r"[:\-]+$",
            "",
            heading
        )

        if heading in STOP_HEADINGS:
            break

        collected.append(line)

    return "\n".join(
        collected
    ).strip()


# ============================================================
# TITLE DETECTION
# ============================================================

def is_description_line(line):
    """
    Detect whether a line is likely a project description
    rather than a project title.
    """

    clean = normalize_line(
        line
    )

    if not clean:
        return False

    lower = clean.lower()

    # Remove bullet
    lower_without_bullet = re.sub(
        r"^[•*\-]\s*",
        "",
        lower
    ).strip()

    first_word_match = re.match(
        r"^([a-zA-Z]+)",
        lower_without_bullet
    )

    if first_word_match:

        first_word = (
            first_word_match.group(1)
        )

        if first_word in DESCRIPTION_START_WORDS:
            return True

    # Sentence-like lines are descriptions.
    if clean.endswith(
        (".", ",", ";")
    ):
        return True

    # Long lines are usually descriptions.
    if len(
        clean.split()
    ) > 12:
        return True

    return False


def looks_like_project_title(line):
    """
    Determine whether a line can represent
    a project title.
    """

    clean = normalize_line(
        line
    )

    if not clean:
        return False

    if is_description_line(
        clean
    ):
        return False

    lower = clean.lower()

    project_keywords = [
        "project",
        "system",
        "platform",
        "application",
        "prediction",
        "classifier",
        "dashboard",
        "website",
        "portal",
        "model",
        "analysis",
        "management",
        "detection",
        "recommendation",
        "screening",
        "congestion",
    ]

    if any(
        keyword in lower
        for keyword in project_keywords
    ):
        return True

    words = clean.split()

    if 2 <= len(words) <= 8:
        return True

    return False


# ============================================================
# PROJECT BLOCK SPLITTING
# ============================================================

def split_project_blocks(
    project_section
):
    """
    Split a Projects section into individual
    project blocks.

    A description line does NOT start a new project.
    """

    if not project_section:
        return []

    raw_lines = project_section.splitlines()

    lines = []

    for line in raw_lines:

        clean = normalize_line(
            line
        )

        if clean:
            lines.append(
                clean
            )

    if not lines:
        return []

    blocks = []

    current_block = []

    for line in lines:

        candidate = re.sub(
            r"^[•*\-]\s*",
            "",
            line
        ).strip()

        is_new_project = (
            looks_like_project_title(
                candidate
            )
            and not is_description_line(
                candidate
            )
        )

        if (
            is_new_project
            and current_block
        ):

            blocks.append(
                "\n".join(
                    current_block
                )
            )

            current_block = [
                candidate
            ]

        else:

            current_block.append(
                candidate
            )

    if current_block:

        blocks.append(
            "\n".join(
                current_block
            )
        )

    return blocks


# ============================================================
# PROJECT TITLE
# ============================================================

def clean_project_title(
    block
):
    """
    Extract project title from block.
    """

    lines = [
        normalize_line(line)
        for line in block.splitlines()
        if normalize_line(line)
    ]

    if not lines:
        return "Unknown Project"

    title = lines[0]

    title = re.sub(
        r"^[•*\-]\s*",
        "",
        title
    )

    title = re.sub(
        r"\s*\|\s*.*$",
        "",
        title
    )

    return title.strip()


# ============================================================
# TECHNOLOGY EXTRACTION
# ============================================================

def extract_project_technologies(
    text
):
    """
    Extract known technologies and ML/data skills
    from project text.
    """

    if not text:
        return []

    lower = text.lower()

    technologies = set()

    aliases = {

        "python": [
            "python",
        ],

        "java": [
            "java",
        ],

        "c++": [
            "c++",
            "cpp",
        ],

        "javascript": [
            "javascript",
            "js",
        ],

        "html": [
            "html",
            "html5",
        ],

        "css": [
            "css",
            "css3",
        ],

        "react": [
            "react",
            "react.js",
            "reactjs",
        ],

        "node.js": [
            "node.js",
            "nodejs",
        ],

        "machine learning": [
            "machine learning",
        ],

        "deep learning": [
            "deep learning",
        ],

        "natural language processing": [
            "natural language processing",
            "nlp",
        ],

        "computer vision": [
            "computer vision",
        ],

        "tensorflow": [
            "tensorflow",
        ],

        "pytorch": [
            "pytorch",
        ],

        "scikit-learn": [
            "scikit-learn",
            "sklearn",
        ],

        "pandas": [
            "pandas",
        ],

        "numpy": [
            "numpy",
        ],

        "sql": [
            "sql",
        ],

        "git": [
            "git",
            "github",
        ],

        "docker": [
            "docker",
        ],

        "kubernetes": [
            "kubernetes",
        ],

        "aws": [
            "aws",
            "amazon web services",
        ],

        "azure": [
            "azure",
        ],

        "gcp": [
            "gcp",
            "google cloud",
        ],

        "mongodb": [
            "mongodb",
            "mongo db",
        ],

        "mysql": [
            "mysql",
        ],

        "postgresql": [
            "postgresql",
            "postgres",
        ],
    }

    for normalized_name, alias_list in (
        aliases.items()
    ):

        for alias in alias_list:

            pattern = (
                r"(?<!\w)"
                + re.escape(alias)
                + r"(?!\w)"
            )

            if re.search(
                pattern,
                lower
            ):

                technologies.add(
                    normalized_name
                )

                break

    return sorted(
        technologies
    )


# ============================================================
# PROJECT CLASSIFICATION
# ============================================================

def classify_project(
    text
):
    """
    Classify project using the complete
    project block.
    """

    if not text:
        return "Other"

    lower = text.lower()

    scores = {}

    for category, keywords in (
        PROJECT_CATEGORIES.items()
    ):

        score = 0

        for keyword in keywords:

            if keyword.lower() in lower:
                score += 1

        scores[
            category
        ] = score

    if not scores:
        return "Other"

    best_category = max(
        scores,
        key=scores.get
    )

    if scores[
        best_category
    ] == 0:

        return "Other"

    return best_category


# ============================================================
# JD SKILLS
# ============================================================

def extract_jd_skills(
    jd_text
):
    """
    Extract all normalized skills from JD.
    """

    if not jd_text:
        return set()

    try:

        from skill_intelligence import (
            extract_normalized_skills
        )

        return set(
            extract_normalized_skills(
                jd_text
            )
        )

    except ImportError:

        return set(
            extract_project_technologies(
                jd_text
            )
        )


# ============================================================
# JD REQUIRED / PREFERRED SKILLS
# ============================================================

def extract_jd_skill_sections(
    jd_text
):
    """
    Extract required and preferred skills separately.

    This prevents preferred skills from being treated
    as equally important as required skills.
    """

    required_skills = set()
    preferred_skills = set()

    if not jd_text:
        return (
            required_skills,
            preferred_skills
        )

    current_section = None

    for line in jd_text.splitlines():

        clean = normalize_line(
            line
        )

        if not clean:
            continue

        lower = clean.lower()

        # Section starts
        if lower.startswith(
            "required skills"
        ):

            current_section = "required"
            continue

        if lower.startswith(
            "preferred skills"
        ):

            current_section = "preferred"
            continue

        # Section stops
        if lower.startswith(
            (
                "education:",
                "experience:",
                "job title:",
                "job description:",
                "responsibilities:",
            )
        ):

            current_section = None
            continue

        if current_section not in {
            "required",
            "preferred",
        }:

            continue

        # Remove bullet
        clean = re.sub(
            r"^[•*\-]\s*",
            "",
            clean
        ).strip()

        if not clean:
            continue

        try:

            from skill_intelligence import (
                extract_normalized_skills
            )

            detected = set(
                extract_normalized_skills(
                    clean
                )
            )

        except ImportError:

            detected = set(
                extract_project_technologies(
                    clean
                )
            )

        if current_section == "required":

            required_skills.update(
                detected
            )

        else:

            preferred_skills.update(
                detected
            )

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    # If no sections could be detected,
    # treat all extracted JD skills as required.
    if not required_skills and not preferred_skills:

        required_skills = set(
            extract_jd_skills(
                jd_text
            )
        )

    return (
        required_skills,
        preferred_skills
    )


# ============================================================
# PROJECT RELEVANCE
# ============================================================

def calculate_project_relevance(
    project,
    jd_text=""
):
    """
    Calculate independent project relevance signals.

    Signals:
    - Required skill overlap
    - Preferred skill overlap
    - Combined skill relevance
    - Keyword overlap
    - Category match

    Required skills receive greater importance than
    preferred skills in the combined skill relevance.
    """

    if not jd_text:

        return {
            "skill_overlap": 0.0,
            "required_skill_overlap": 0.0,
            "preferred_skill_overlap": 0.0,
            "matched_required_skills": [],
            "matched_preferred_skills": [],
            "keyword_overlap": 0.0,
            "category_match": 0.0,
            "matched_category_terms": [],
        }

    project_text = project.get(
        "raw_text",
        ""
    )

    category = project.get(
        "category",
        "Other"
    )

    # --------------------------------------------------------
    # PROJECT SKILLS
    # --------------------------------------------------------

    project_skills = set(
        extract_project_technologies(
            project_text
        )
    )

    # --------------------------------------------------------
    # JD REQUIRED / PREFERRED SKILLS
    # --------------------------------------------------------

    (
        required_skills,
        preferred_skills
    ) = extract_jd_skill_sections(
        jd_text
    )

    # --------------------------------------------------------
    # REQUIRED SKILL OVERLAP
    # --------------------------------------------------------

    matched_required_skills = sorted(
        project_skills
        & required_skills
    )

    if required_skills:

        required_skill_overlap = (
            len(
                matched_required_skills
            )
            / len(required_skills)
        ) * 100

    else:

        required_skill_overlap = 0.0

    # --------------------------------------------------------
    # PREFERRED SKILL OVERLAP
    # --------------------------------------------------------

    matched_preferred_skills = sorted(
        project_skills
        & preferred_skills
    )

    if preferred_skills:

        preferred_skill_overlap = (
            len(
                matched_preferred_skills
            )
            / len(preferred_skills)
        ) * 100

    else:

        preferred_skill_overlap = 0.0

    # --------------------------------------------------------
    # COMBINED SKILL OVERLAP
    # --------------------------------------------------------

    # Required skills are given 70% of the skill signal.
    # Preferred skills contribute the remaining 30%.
    if required_skills and preferred_skills:

        skill_overlap = (
            required_skill_overlap * 0.70
            + preferred_skill_overlap * 0.30
        )

    elif required_skills:

        skill_overlap = (
            required_skill_overlap
        )

    elif preferred_skills:

        skill_overlap = (
            preferred_skill_overlap
        )

    else:

        skill_overlap = 0.0

    # --------------------------------------------------------
    # KEYWORD OVERLAP
    # --------------------------------------------------------

    jd_words = set(
        re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+#.\-]*\b",
            jd_text.lower()
        )
    )

    project_words = set(
        re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+#.\-]*\b",
            project_text.lower()
        )
    )

    stop_words = {
        "this",
        "that",
        "with",
        "from",
        "into",
        "using",
        "work",
        "team",
        "develop",
        "developed",
        "developing",
        "implement",
        "implemented",
        "perform",
        "performing",
        "document",
        "documentation",
        "results",
        "system",
        "candidate",
        "candidates",
        "looking",
        "join",
        "responsibilities",
        "required",
        "preferred",
        "skills",
        "education",
        "degree",
        "related",
        "field",
        "years",
        "experience",
        "company",
        "role",
        "engineer",
    }

    important_words = {
        word
        for word in jd_words
        if len(word) >= 4
        and word not in stop_words
    }

    if important_words:

        keyword_overlap = (
            len(
                project_words
                & important_words
            )
            / len(important_words)
        ) * 100

    else:

        keyword_overlap = 0.0

    # --------------------------------------------------------
    # CATEGORY MATCH
    # --------------------------------------------------------

    jd_lower = jd_text.lower()

    category_terms = (
        PROJECT_CATEGORIES.get(
            category,
            []
        )
    )

    matched_category_terms = []

    for term in category_terms:

        if term.lower() in jd_lower:

            matched_category_terms.append(
                term
            )

    category_match = (
        100.0
        if matched_category_terms
        else 0.0
    )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    return {
        # Backward-compatible combined field
        "skill_overlap": round(
            skill_overlap,
            2
        ),

        # New detailed fields
        "required_skill_overlap": round(
            required_skill_overlap,
            2
        ),

        "preferred_skill_overlap": round(
            preferred_skill_overlap,
            2
        ),

        "matched_required_skills":
            matched_required_skills,

        "matched_preferred_skills":
            matched_preferred_skills,

        "keyword_overlap": round(
            keyword_overlap,
            2
        ),

        "category_match": round(
            category_match,
            2
        ),

        "matched_category_terms":
            matched_category_terms,
    }


# ============================================================
# PARSE PROJECT BLOCK
# ============================================================

def parse_project_block(
    block,
    jd_text=""
):
    """
    Convert one project block into
    structured information.
    """

    if not block:
        return None

    title = clean_project_title(
        block
    )

    technologies = (
        extract_project_technologies(
            block
        )
    )

    category = classify_project(
        block
    )

    lines = [
        normalize_line(line)
        for line in block.splitlines()
        if normalize_line(line)
    ]

    description_lines = []

    for line in lines[1:]:

        lower = line.lower()

        if lower.startswith(
            (
                "technologies:",
                "tech stack:",
                "tools:",
                "skills:",
            )
        ):
            continue

        description_lines.append(
            line
        )

    description = " ".join(
        description_lines
    ).strip()

    project = {
        "title": title,
        "category": category,
        "technologies": technologies,
        "description": description,
        "raw_text": block,
    }

    project["relevance"] = (
        calculate_project_relevance(
            project,
            jd_text
        )
    )

    return project


# ============================================================
# EXTRACT PROJECTS
# ============================================================

def extract_projects(
    text,
    jd_text=""
):
    """
    Extract projects from resume.
    """

    section = extract_project_section(
        text
    )

    if not section:
        return []

    blocks = split_project_blocks(
        section
    )

    projects = []

    for block in blocks:

        project = parse_project_block(
            block,
            jd_text
        )

        if project:
            projects.append(
                project
            )

    return projects


# ============================================================
# BUILD PROJECT PROFILE
# ============================================================

def build_project_profile(
    text,
    jd_text=""
):
    """
    Build complete project profile.
    """

    projects = extract_projects(
        text,
        jd_text
    )

    category_counts = {}

    for project in projects:

        category = project.get(
            "category",
            "Other"
        )

        category_counts[
            category
        ] = (
            category_counts.get(
                category,
                0
            ) + 1
        )

    skill_values = []
    required_skill_values = []
    preferred_skill_values = []
    keyword_values = []
    category_values = []

    for project in projects:

        relevance = project.get(
            "relevance",
            {}
        )

        skill_values.append(
            relevance.get(
                "skill_overlap",
                0.0
            )
        )

        required_skill_values.append(
            relevance.get(
                "required_skill_overlap",
                0.0
            )
        )

        preferred_skill_values.append(
            relevance.get(
                "preferred_skill_overlap",
                0.0
            )
        )

        keyword_values.append(
            relevance.get(
                "keyword_overlap",
                0.0
            )
        )

        category_values.append(
            relevance.get(
                "category_match",
                0.0
            )
        )

    # --------------------------------------------------------
    # AVERAGES
    # --------------------------------------------------------

    average_skill_overlap = (
        sum(skill_values)
        / len(skill_values)
        if skill_values
        else 0.0
    )

    average_required_skill_overlap = (
        sum(required_skill_values)
        / len(required_skill_values)
        if required_skill_values
        else 0.0
    )

    average_preferred_skill_overlap = (
        sum(preferred_skill_values)
        / len(preferred_skill_values)
        if preferred_skill_values
        else 0.0
    )

    average_keyword_overlap = (
        sum(keyword_values)
        / len(keyword_values)
        if keyword_values
        else 0.0
    )

    average_category_match = (
        sum(category_values)
        / len(category_values)
        if category_values
        else 0.0
    )

    # --------------------------------------------------------
    # BEST VALUES
    # --------------------------------------------------------

    best_skill_overlap = (
        max(skill_values)
        if skill_values
        else 0.0
    )

    best_required_skill_overlap = (
        max(required_skill_values)
        if required_skill_values
        else 0.0
    )

    best_preferred_skill_overlap = (
        max(preferred_skill_values)
        if preferred_skill_values
        else 0.0
    )

    best_keyword_overlap = (
        max(keyword_values)
        if keyword_values
        else 0.0
    )

    best_category_match = (
        max(category_values)
        if category_values
        else 0.0
    )

    # --------------------------------------------------------
    # RELEVANT PROJECT COUNT
    # --------------------------------------------------------

    relevant_project_count = 0

    for project in projects:

        relevance = project.get(
            "relevance",
            {}
        )

        if (
            relevance.get(
                "skill_overlap",
                0.0
            ) > 0
            or
            relevance.get(
                "category_match",
                0.0
            ) > 0
        ):

            relevant_project_count += 1

    # --------------------------------------------------------
    # RETURN PROFILE
    # --------------------------------------------------------

    return {
        "project_count": len(
            projects
        ),

        "projects": projects,

        "category_counts":
            category_counts,

        "relevant_project_count":
            relevant_project_count,

        "average_skill_overlap":
            round(
                average_skill_overlap,
                2
            ),

        "average_required_skill_overlap":
            round(
                average_required_skill_overlap,
                2
            ),

        "average_preferred_skill_overlap":
            round(
                average_preferred_skill_overlap,
                2
            ),

        "average_keyword_overlap":
            round(
                average_keyword_overlap,
                2
            ),

        "average_category_match":
            round(
                average_category_match,
                2
            ),

        "best_skill_overlap":
            round(
                best_skill_overlap,
                2
            ),

        "best_required_skill_overlap":
            round(
                best_required_skill_overlap,
                2
            ),

        "best_preferred_skill_overlap":
            round(
                best_preferred_skill_overlap,
                2
            ),

        "best_keyword_overlap":
            round(
                best_keyword_overlap,
                2
            ),

        "best_category_match":
            round(
                best_category_match,
                2
            ),
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sample_resume = """
    Abhinav Gupta

    PROJECTS

    AI Resume Screening System
    Developed an AI-based resume screening system using Python,
    NLP, TF-IDF, and machine learning to rank candidates.

    Traffic Congestion Prediction
    Built a machine learning classification system using Python,
    Pandas, NumPy and Scikit-learn to predict traffic congestion.

    QuizHub Web Platform
    Created a web-based quiz platform using HTML, CSS and JavaScript
    with timer, leaderboard and ranking features.

    EDUCATION

    B.Tech Computer Science
    """

    sample_jd = """
    Job Title: Junior Machine Learning Engineer

    Responsibilities:
    Develop and implement machine learning models.
    Clean and preprocess datasets.
    Perform data analysis and feature engineering.

    Required Skills:
    Python
    Machine Learning
    Pandas
    NumPy
    Scikit-learn
    SQL
    Data Analysis
    Statistics

    Preferred Skills:
    Deep Learning
    TensorFlow
    PyTorch
    Natural Language Processing
    Git
    Docker

    Education:
    Bachelor's degree in Computer Science.
    """

    profile = build_project_profile(
        sample_resume,
        sample_jd
    )

    print("=" * 70)
    print("PROJECT PROFILE")
    print("=" * 70)

    print(
        f"\nTotal Projects: "
        f"{profile['project_count']}"
    )

    print("\nCategory Counts:")

    for category, count in (
        profile["category_counts"].items()
    ):

        print(
            f"  {category}: {count}"
        )

    print("\nProjects:")

    for i, project in enumerate(
        profile["projects"],
        start=1
    ):

        print(
            f"\nProject {i}"
        )

        print("-" * 40)

        print(
            f"Title: "
            f"{project['title']}"
        )

        print(
            f"Category: "
            f"{project['category']}"
        )

        print(
            "Technologies:",
            ", ".join(
                project["technologies"]
            )
            if project["technologies"]
            else "None detected"
        )

        print(
            f"Description: "
            f"{project['description']}"
        )

        relevance = project[
            "relevance"
        ]

        print(
            "Required Skill Overlap:",
            relevance[
                "required_skill_overlap"
            ],
            "%"
        )

        print(
            "Preferred Skill Overlap:",
            relevance[
                "preferred_skill_overlap"
            ],
            "%"
        )

        print(
            "Combined Skill Relevance:",
            relevance[
                "skill_overlap"
            ],
            "%"
        )

        print(
            "Matched Required Skills:",
            ", ".join(
                relevance.get(
                    "matched_required_skills",
                    []
                )
            )
            if relevance.get(
                "matched_required_skills",
                []
            )
            else "None"
        )

        print(
            "Matched Preferred Skills:",
            ", ".join(
                relevance.get(
                    "matched_preferred_skills",
                    []
                )
            )
            if relevance.get(
                "matched_preferred_skills",
                []
            )
            else "None"
        )

        print(
            "JD Keyword Overlap:",
            relevance[
                "keyword_overlap"
            ],
            "%"
        )

        print(
            "JD Category Match:",
            relevance[
                "category_match"
            ],
            "%"
        )

        matched = relevance.get(
            "matched_category_terms",
            []
        )

        if matched:

            print(
                "Matched Category Terms:",
                ", ".join(matched)
            )

    print()

    print("=" * 70)
    print("PROJECT RELEVANCE SUMMARY")
    print("=" * 70)

    print(
        "Relevant Projects:",
        profile[
            "relevant_project_count"
        ]
    )

    print(
        "Average Required Skill Overlap:",
        profile[
            "average_required_skill_overlap"
        ],
        "%"
    )

    print(
        "Average Preferred Skill Overlap:",
        profile[
            "average_preferred_skill_overlap"
        ],
        "%"
    )

    print(
        "Average Combined Skill Overlap:",
        profile[
            "average_skill_overlap"
        ],
        "%"
    )

    print(
        "Average Keyword Overlap:",
        profile[
            "average_keyword_overlap"
        ],
        "%"
    )

    print(
        "Average Category Match:",
        profile[
            "average_category_match"
        ],
        "%"
    )

    print(
        "Best Required Skill Overlap:",
        profile[
            "best_required_skill_overlap"
        ],
        "%"
    )

    print(
        "Best Preferred Skill Overlap:",
        profile[
            "best_preferred_skill_overlap"
        ],
        "%"
    )

    print(
        "Best Combined Skill Overlap:",
        profile[
            "best_skill_overlap"
        ],
        "%"
    )

    print(
        "Best Keyword Overlap:",
        profile[
            "best_keyword_overlap"
        ],
        "%"
    )

    print(
        "Best Category Match:",
        profile[
            "best_category_match"
        ],
        "%"
    )

    print("=" * 70)