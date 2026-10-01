import re


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    # --------------------------------------------------------
    # Programming Languages
    # --------------------------------------------------------

    "python": [
        "python",
        "python3",
    ],

    "java": [
        "java",
        "java programming",
    ],

    "c++": [
        "c++",
        "cpp",
    ],

    "javascript": [
        "javascript",
        "js",
    ],

    # --------------------------------------------------------
    # AI / ML
    # --------------------------------------------------------

    "machine learning": [
        "machine learning",
        "machine-learning",
    ],

    "deep learning": [
        "deep learning",
        "deep-learning",
    ],

    "natural language processing": [
        "natural language processing",
        "nlp",
    ],

    "computer vision": [
        "computer vision",
    ],

    "generative ai": [
        "generative ai",
        "generative artificial intelligence",
        "genai",
    ],

    "large language models": [
        "large language model",
        "large language models",
        "llm",
        "llms",
    ],

    "transformers": [
        "transformer",
        "transformers",
    ],

    # --------------------------------------------------------
    # Data Science
    # --------------------------------------------------------

    "pandas": [
        "pandas",
    ],

    "numpy": [
        "numpy",
    ],

    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn",
    ],

    "sql": [
        "sql",
        "structured query language",
    ],

    "data analysis": [
        "data analysis",
        "data analytics",
    ],

    "statistics": [
        "statistics",
        "statistical analysis",
    ],

    "data visualization": [
        "data visualization",
        "data visualisation",
    ],

    # --------------------------------------------------------
    # ML Frameworks
    # --------------------------------------------------------

    "tensorflow": [
        "tensorflow",
        "tensor flow",
    ],

    "pytorch": [
        "pytorch",
        "py torch",
    ],

    "keras": [
        "keras",
    ],

    "hugging face": [
        "hugging face",
        "huggingface",
    ],

    # --------------------------------------------------------
    # Version Control / DevOps
    # --------------------------------------------------------

    "git": [
        "git",
    ],

    "github": [
        "github",
        "git hub",
    ],

    "docker": [
        "docker",
    ],

    "kubernetes": [
        "kubernetes",
        "k8s",
    ],

    # --------------------------------------------------------
    # Web
    # --------------------------------------------------------

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
        "reactjs",
        "react.js",
    ],

    "node.js": [
        "node.js",
        "nodejs",
        "node js",
    ],

    "express": [
        "express",
        "express.js",
        "expressjs",
    ],

    "fastapi": [
        "fastapi",
        "fast api",
    ],

    "flask": [
        "flask",
    ],

    "streamlit": [
        "streamlit",
    ],

    "rest api": [
        "rest api",
        "restful api",
        "restful apis",
    ],

    # --------------------------------------------------------
    # Databases
    # --------------------------------------------------------

    "mysql": [
        "mysql",
        "my sql",
    ],

    "postgresql": [
        "postgresql",
        "postgres",
    ],

    "mongodb": [
        "mongodb",
        "mongo db",
    ],

    # --------------------------------------------------------
    # Cloud
    # --------------------------------------------------------

    "aws": [
        "aws",
        "amazon web services",
    ],

    "azure": [
        "azure",
        "microsoft azure",
    ],

    "gcp": [
        "gcp",
        "google cloud",
        "google cloud platform",
    ],
}


# ============================================================
# AMBIGUOUS / SHORT ALIASES
# ============================================================

# These aliases should NOT be searched blindly because
# they can create false positives in normal English text.

AMBIGUOUS_ALIASES = {
    "ml": "machine learning",
    "dl": "deep learning",
    "cv": "computer vision",
}


# ============================================================
# SECTION DEFINITIONS
# ============================================================

SECTION_ALIASES = {
    "skills": [
        "skills",
        "technical skills",
        "technical skill",
        "core skills",
        "core competencies",
        "competencies",
        "skill set",
        "skills & technologies",
        "skills and technologies",
        "technical expertise",
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "internship experience",
        "internships",
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "relevant projects",
        "major projects",
        "key projects",
        "project experience",
    ],

    "education": [
        "education",
        "academic background",
        "educational background",
        "qualifications",
    ],

    "certifications": [
        "certifications",
        "certificates",
        "licenses",
        "courses",
    ],

    "achievements": [
        "achievements",
        "awards",
        "honors",
        "accomplishments",
    ],

    "summary": [
        "summary",
        "professional summary",
        "profile",
        "objective",
        "career objective",
        "about me",
    ],
}


# ============================================================
# SECTION EVIDENCE WEIGHTS
# ============================================================

# Stronger evidence means the skill is explicitly presented
# in a technical/skills section or demonstrated in projects
# or professional experience.

SECTION_STRENGTH = {
    "skills": "HIGH",
    "experience": "HIGH",
    "projects": "HIGH",
    "certifications": "MEDIUM",
    "education": "MEDIUM",
    "achievements": "MEDIUM",
    "summary": "LOW",
    "other": "LOW",
}


SECTION_WEIGHT = {
    "skills": 1.00,
    "experience": 1.00,
    "projects": 1.00,
    "certifications": 0.80,
    "education": 0.70,
    "achievements": 0.70,
    "summary": 0.50,
    "other": 0.40,
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize resume/JD text before processing.
    """

    if not text:
        return ""

    text = str(text)

    # Common encoding issues
    replacements = {
        "Ã¢â‚¬â€œ": "-",
        "Ã¢â‚¬â€": "-",
        "â€“": "-",
        "â€”": "-",
        "â€˜": "'",
        "â€™": "'",
        "â€œ": '"',
        "â€": '"',
        "Â·": " ",
        "•": " ",
        "●": " ",
        "\u2022": " ",
        "\u2013": "-",
        "\u2014": "-",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.lower()

    # Normalize whitespace
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ============================================================
# REGEX HELPERS
# ============================================================

def alias_pattern(alias):
    """
    Build a regex pattern that safely detects an alias.
    """

    escaped = re.escape(alias)

    # Allow spaces/hyphens to be flexible.
    escaped = escaped.replace(r"\ ", r"[\s\-]+")

    return rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"


def contains_alias(text, alias):
    """
    Check whether an alias appears in text.

    Ambiguous aliases such as ML/DL/CV require
    additional technical context.
    """

    if not text:
        return False

    normalized = normalize_text(text)

    # --------------------------------------------------------
    # Handle ambiguous aliases separately
    # --------------------------------------------------------

    if alias in AMBIGUOUS_ALIASES:

        if not re.search(alias_pattern(alias), normalized):
            return False

        # Look for technical context nearby.
        technical_context = [
            "machine learning",
            "deep learning",
            "computer vision",
            "model",
            "models",
            "algorithm",
            "algorithms",
            "neural network",
            "neural networks",
            "training",
            "prediction",
            "classification",
            "regression",
            "dataset",
            "datasets",
            "tensorflow",
            "pytorch",
            "scikit-learn",
            "python",
        ]

        for context in technical_context:
            if re.search(alias_pattern(context), normalized):
                return True

        return False

    return bool(re.search(alias_pattern(alias), normalized))


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_normalized_skills(text):
    """
    Extract canonical skill names from text.

    Returns:
        sorted list of normalized skills
    """

    normalized = normalize_text(text)

    if not normalized:
        return []

    detected = set()

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if contains_alias(normalized, alias):
                detected.add(skill)
                break

    # Explicit ambiguous aliases
    for alias, canonical_skill in AMBIGUOUS_ALIASES.items():

        if contains_alias(normalized, alias):
            detected.add(canonical_skill)

    return sorted(detected)


# ============================================================
# SECTION DETECTION
# ============================================================

def normalize_heading(line):
    """
    Convert a possible heading into a comparable format.
    """

    line = line.strip().lower()

    # Remove common heading decorations
    line = re.sub(r"^[\-\*\•\●\#\d\.\)\(:]+", "", line)
    line = re.sub(r"[\:\-]+$", "", line)

    line = re.sub(r"\s+", " ", line)

    return line.strip()


def detect_section(line):
    """
    Detect whether a line represents a known resume section.
    """

    normalized = normalize_heading(line)

    if not normalized:
        return None

    for section, headings in SECTION_ALIASES.items():

        for heading in headings:

            if normalized == heading:
                return section

    return None


def extract_skill_sections(text):
    """
    Split resume text into logical sections.

    Returns:
        {
            "skills": "...",
            "experience": "...",
            "projects": "...",
            ...
        }
    """

    normalized = normalize_text(text)

    if not normalized:
        return {}

    lines = normalized.splitlines()

    sections = {}
    current_section = "other"
    current_lines = []

    def save_section():
        if current_lines:
            content = "\n".join(current_lines).strip()

            if content:
                sections.setdefault(current_section, "")
                sections[current_section] += "\n" + content

    for line in lines:

        detected = detect_section(line)

        if detected:

            save_section()

            current_section = detected
            current_lines = []

        else:
            current_lines.append(line)

    save_section()

    # Clean output
    for section in sections:

        sections[section] = sections[section].strip()

    return sections


# ============================================================
# EVIDENCE EXTRACTION
# ============================================================
def find_alias_evidence(text, canonical_skill):
    """
    Find concise, human-readable evidence for a skill.

    Instead of returning a large character window, this function
    identifies the sentence or bullet containing the skill.
    """

    normalized = normalize_text(text)

    aliases = list(
        SKILL_ALIASES.get(canonical_skill, [])
    )

    # Add ambiguous aliases where applicable.
    for ambiguous, canonical in AMBIGUOUS_ALIASES.items():
        if canonical == canonical_skill:
            aliases.append(ambiguous)

    # --------------------------------------------------------
    # Split text into evidence units
    # --------------------------------------------------------

    # First split by lines.
    lines = [
        line.strip()
        for line in normalized.splitlines()
        if line.strip()
    ]

    evidence_units = []

    for line in lines:

        # Remove common bullet characters.
        cleaned = re.sub(
            r"^[\-\*\•\●▪◦]+\s*",
            "",
            line
        ).strip()

        if not cleaned:
            continue

        # Split long lines into sentences.
        sentences = re.split(
            r"(?<=[.!?])\s+",
            cleaned
        )

        for sentence in sentences:

            sentence = sentence.strip()

            if sentence:
                evidence_units.append(sentence)

    # --------------------------------------------------------
    # Search for the best matching evidence unit
    # --------------------------------------------------------

    for alias in aliases:

        pattern = re.compile(
            alias_pattern(alias),
            re.IGNORECASE
        )

        for unit in evidence_units:

            if not pattern.search(unit):
                continue

            # Ambiguous aliases require technical context.
            if alias in AMBIGUOUS_ALIASES:

                technical_context = [
                    "machine learning",
                    "deep learning",
                    "computer vision",
                    "model",
                    "models",
                    "algorithm",
                    "algorithms",
                    "neural network",
                    "neural networks",
                    "training",
                    "prediction",
                    "classification",
                    "regression",
                    "dataset",
                    "datasets",
                    "tensorflow",
                    "pytorch",
                    "scikit-learn",
                    "python",
                ]

                has_context = any(
                    re.search(
                        alias_pattern(context),
                        unit
                    )
                    for context in technical_context
                )

                if not has_context:
                    continue

            # Keep evidence concise.
            evidence = re.sub(
                r"\s+",
                " ",
                unit
            ).strip()

            return {
                "alias": alias,
                "evidence": evidence,
            }

    return None


def extract_skill_evidence(text):
    """
    Extract detailed evidence for every detected skill.

    Returns a dictionary:

        {
            "python": [
                {
                    "section": "skills",
                    "strength": "HIGH",
                    "weight": 1.0,
                    "alias": "python",
                    "evidence": "..."
                }
            ]
        }
    """

    sections = extract_skill_sections(text)

    evidence = {}

    for section, section_text in sections.items():

        skills = extract_normalized_skills(section_text)

        for skill in skills:

            result = find_alias_evidence(
                section_text,
                skill
            )

            if not result:
                continue

            item = {
                "section": section,
                "strength": SECTION_STRENGTH.get(
                    section,
                    "LOW"
                ),
                "weight": SECTION_WEIGHT.get(
                    section,
                    0.40
                ),
                "alias": result["alias"],
                "evidence": result["evidence"],
            }

            evidence.setdefault(skill, [])

            # Avoid duplicate evidence entries.
            duplicate = False

            for existing in evidence[skill]:

                if (
                    existing["section"] == item["section"]
                    and existing["alias"] == item["alias"]
                ):
                    duplicate = True
                    break

            if not duplicate:
                evidence[skill].append(item)

    # --------------------------------------------------------
    # Important fallback:
    # If the resume has no recognizable sections,
    # search the complete document.
    # --------------------------------------------------------

    if not evidence:

        skills = extract_normalized_skills(text)

        for skill in skills:

            result = find_alias_evidence(
                text,
                skill
            )

            if result:

                evidence.setdefault(skill, []).append({
                    "section": "other",
                    "strength": "LOW",
                    "weight": SECTION_WEIGHT["other"],
                    "alias": result["alias"],
                    "evidence": result["evidence"],
                })

    return evidence


# ============================================================
# PRIMARY EVIDENCE PER SKILL
# ============================================================

def get_primary_skill_evidence(evidence):
    """
    Select the strongest evidence for every skill.

    Priority:
        HIGH > MEDIUM > LOW
        then section weight
    """

    strength_rank = {
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }

    primary = {}

    for skill, items in evidence.items():

        if not items:
            continue

        best = max(
            items,
            key=lambda item: (
                strength_rank.get(
                    item["strength"],
                    0
                ),
                item["weight"]
            )
        )

        primary[skill] = best

    return primary


# ============================================================
# SKILL COMPARISON
# ============================================================

def compare_skills(required_skills, preferred_skills, candidate_skills):
    """
    Compare JD skills against candidate skills.
    """

    required = set(
        normalize_text(skill)
        for skill in required_skills
    )

    preferred = set(
        normalize_text(skill)
        for skill in preferred_skills
    )

    candidate = set(
        normalize_text(skill)
        for skill in candidate_skills
    )

    matched_required = sorted(
        required.intersection(candidate)
    )

    missing_required = sorted(
        required.difference(candidate)
    )

    matched_preferred = sorted(
        preferred.intersection(candidate)
    )

    missing_preferred = sorted(
        preferred.difference(candidate)
    )

    return {
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred,
    }


# ============================================================
# SKILL SCORES
# ============================================================

def calculate_skill_scores(
    required_skills,
    preferred_skills,
    candidate_skills
):
    """
    Calculate skill-level scores.

    Required skills:
        75% of final skill score

    Preferred skills:
        25% of final skill score

    NOTE:
    These are feature-level weights only.
    They are NOT the final candidate ranking weights.
    """

    required_skills = set(
        normalize_text(skill)
        for skill in required_skills
    )

    preferred_skills = set(
        normalize_text(skill)
        for skill in preferred_skills
    )

    candidate_skills = set(
        normalize_text(skill)
        for skill in candidate_skills
    )

    if required_skills:

        matched_required = (
            required_skills.intersection(candidate_skills)
        )

        required_score = (
            len(matched_required)
            / len(required_skills)
        ) * 100

    else:

        required_score = 100.0

    if preferred_skills:

        matched_preferred = (
            preferred_skills.intersection(candidate_skills)
        )

        preferred_score = (
            len(matched_preferred)
            / len(preferred_skills)
        ) * 100

    else:

        preferred_score = 100.0

    overall_score = (
        required_score * 0.75
        +
        preferred_score * 0.25
    )

    return {
        "required_score": round(
            required_score,
            2
        ),
        "preferred_score": round(
            preferred_score,
            2
        ),
        "overall_score": round(
            overall_score,
            2
        ),
    }


# ============================================================
# COMPLETE SKILL PROFILE
# ============================================================

def build_skill_profile(
    candidate_text,
    required_skills=None,
    preferred_skills=None
):
    """
    Build a complete skill profile for a candidate.

    This combines:
        - normalized skills
        - evidence
        - primary evidence
        - required skill comparison
        - preferred skill comparison
        - scores
    """

    required_skills = required_skills or []
    preferred_skills = preferred_skills or []

    candidate_skills = extract_normalized_skills(
        candidate_text
    )

    evidence = extract_skill_evidence(
        candidate_text
    )

    primary_evidence = get_primary_skill_evidence(
        evidence
    )

    comparison = compare_skills(
        required_skills,
        preferred_skills,
        candidate_skills
    )

    scores = calculate_skill_scores(
        required_skills,
        preferred_skills,
        candidate_skills
    )

    return {
        "candidate_skills": candidate_skills,
        "evidence": evidence,
        "primary_evidence": primary_evidence,

        "matched_required": comparison[
            "matched_required"
        ],

        "missing_required": comparison[
            "missing_required"
        ],

        "matched_preferred": comparison[
            "matched_preferred"
        ],

        "missing_preferred": comparison[
            "missing_preferred"
        ],

        "required_score": scores[
            "required_score"
        ],

        "preferred_score": scores[
            "preferred_score"
        ],

        "overall_score": scores[
            "overall_score"
        ],
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SKILL INTELLIGENCE TEST")
    print("=" * 60)

    required = [
        "Python",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "SQL",
        "Data Analysis",
        "Statistics",
    ]

    preferred = [
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Natural Language Processing",
        "Git",
        "Docker",
    ]

    candidate_text = """
    ABHINAV GUPTA

    SUMMARY
    Computer Science student interested in machine learning
    and data science.

    TECHNICAL SKILLS
    Python, Pandas, NumPy, Scikit-learn, SQL,
    Data Analysis, Deep Learning, Git,
    Natural Language Processing

    PROJECTS

    AI Resume Screening System
    Developed a machine learning based resume screening
    system using Python, NLP, TF-IDF and Scikit-learn.

    Traffic Congestion Prediction
    Built a machine learning classification system using
    Python, Pandas, NumPy and Scikit-learn.

    EXPERIENCE

    Machine Learning Intern
    Used Python, SQL and Pandas for data analysis.

    EDUCATION

    B.Tech in Computer Science Engineering
    """

    profile = build_skill_profile(
        candidate_text,
        required,
        preferred
    )

    print("\nRequired Skills:")
    print(required)

    print("\nPreferred Skills:")
    print(preferred)

    print("\nCandidate Skills:")
    print(profile["candidate_skills"])

    print("\nMatched Required:")
    print(profile["matched_required"])

    print("\nMissing Required:")
    print(profile["missing_required"])

    print("\nMatched Preferred:")
    print(profile["matched_preferred"])

    print("\nMissing Preferred:")
    print(profile["missing_preferred"])

    print("\nScores:")

    print(
        f"  required_score: "
        f"{profile['required_score']}%"
    )

    print(
        f"  preferred_score: "
        f"{profile['preferred_score']}%"
    )

    print(
        f"  overall_score: "
        f"{profile['overall_score']}%"
    )

    print("\n" + "=" * 60)
    print("SKILL EVIDENCE")
    print("=" * 60)

    for skill, items in profile["primary_evidence"].items():

        print(f"\n{skill}")

        for item in items.items():

            key, value = item

            if key == "evidence":

                print(
                    f"  Evidence: {value}"
                )

            elif key == "section":

                print(
                    f"  Section: {value}"
                )

            elif key == "strength":

                print(
                    f"  Strength: {value}"
                )

            elif key == "alias":

                print(
                    f"  Alias: {value}"
                )

    print("\n" + "=" * 60)