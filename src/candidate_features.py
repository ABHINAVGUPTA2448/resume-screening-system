import os
import pymupdf


from skill_intelligence import (
    build_skill_profile,
)

from candidate_profile import (
    build_candidate_profile,
)

from role_extractor import (
    build_role_profile,
)

from jd_requirements import (
    extract_jd_requirements,
    calculate_experience_match,
)

from education_matcher import (
    extract_education_profile,
    extract_jd_education_requirement,
    calculate_education_match,
)

from project_extractor import (
    build_project_profile,
)

from tfidf_similarity import (
    calculate_tfidf_score,
)

from semantic_similarity import (
    load_semantic_model,
    calculate_semantic_score,
)


# ============================================================
# HELPER
# ============================================================

def safe_float(value, default=0.0):
    """
    Safely convert a value to float.

    Handles:
    - None
    - strings
    - integers
    - floats
    - invalid values
    """

    try:
        return float(value)

    except (TypeError, ValueError):

        return default


# ============================================================
# JD SKILL EXTRACTION
# ============================================================

def get_required_preferred_skills(jd_text):
    """
    Extract required and preferred skills from the JD.

    Expected JD format:

        Required Skills:
        - Python
        - Machine Learning

        Preferred Skills:
        - TensorFlow
        - PyTorch

    Returns:
        (
            required_skills,
            preferred_skills
        )
    """

    from skill_intelligence import extract_normalized_skills

    if not jd_text:
        return [], []

    lines = jd_text.splitlines()

    required_text = []
    preferred_text = []

    current_section = None

    for line in lines:

        clean = line.strip().lower()

        if not clean:
            continue

        # ----------------------------------------------------
        # Section starts
        # ----------------------------------------------------

        if "required skills" in clean:

            current_section = "required"

            continue

        if "preferred skills" in clean:

            current_section = "preferred"

            continue

        # ----------------------------------------------------
        # Sections where skill collection should stop
        # ----------------------------------------------------

        if (
            clean.startswith("education")
            or clean.startswith("experience")
            or clean.startswith("job title")
            or clean.startswith("job description")
            or clean.startswith("responsibilities")
        ):

            current_section = None

        # ----------------------------------------------------
        # Collect required skills
        # ----------------------------------------------------

        if current_section == "required":

            required_text.append(line)

        # ----------------------------------------------------
        # Collect preferred skills
        # ----------------------------------------------------

        elif current_section == "preferred":

            preferred_text.append(line)

    required_skills = extract_normalized_skills(
        "\n".join(required_text)
    )

    preferred_skills = extract_normalized_skills(
        "\n".join(preferred_text)
    )

    return (
        required_skills,
        preferred_skills,
    )


# ============================================================
# SKILL FEATURES
# ============================================================

def extract_skill_features(
    candidate_text,
    jd_text,
):
    """
    Extract candidate skill features and compare
    them against required and preferred JD skills.
    """

    (
        required_skills,
        preferred_skills,
    ) = get_required_preferred_skills(
        jd_text
    )

    profile = build_skill_profile(
        candidate_text,
        required_skills,
        preferred_skills,
    )

    return {

        "candidate_skills":
            profile.get(
                "candidate_skills",
                []
            ),

        "matched_required":
            profile.get(
                "matched_required",
                []
            ),

        "missing_required":
            profile.get(
                "missing_required",
                []
            ),

        "matched_preferred":
            profile.get(
                "matched_preferred",
                []
            ),

        "missing_preferred":
            profile.get(
                "missing_preferred",
                []
            ),

        "required_score":
            safe_float(
                profile.get(
                    "required_score",
                    0.0
                )
            ),

        "preferred_score":
            safe_float(
                profile.get(
                    "preferred_score",
                    0.0
                )
            ),

        "overall_score":
            safe_float(
                profile.get(
                    "overall_score",
                    0.0
                )
            ),

        "evidence":
            profile.get(
                "evidence",
                {}
            ),

        "primary_evidence":
            profile.get(
                "primary_evidence",
                {}
            ),
    }


# ============================================================
# EXPERIENCE FEATURES
# ============================================================

def extract_experience_features(
    candidate_text,
    jd_text,
):
    """
    Extract candidate experience and compare
    it against the JD experience requirement.
    """

    candidate_profile = build_candidate_profile(
        candidate_text
    )

    candidate_years = safe_float(
        candidate_profile.get(
            "total_experience_years",
            candidate_profile.get(
                "experience_years",
                0.0
            )
        )
    )

    candidate_months = candidate_profile.get(
        "total_experience_months",
        round(candidate_years * 12)
    )

    requirement = extract_jd_requirements(
        jd_text
    )

    # --------------------------------------------------------
    # Check whether JD contains experience requirement
    # --------------------------------------------------------

    has_requirement = requirement.get(
        "has_experience_requirement",
        False
    )

    if not has_requirement:

        return {

            "candidate_years":
                candidate_years,

            "candidate_months":
                candidate_months,

            "requirement":
                requirement,

            "score":
                None,

            "status":
                "NOT_SPECIFIED",
        }

    # --------------------------------------------------------
    # Calculate experience match
    # --------------------------------------------------------

    result = calculate_experience_match(
        candidate_years,
        requirement
    )

    score = result.get(
        "score",
        result.get(
            "match_score",
            0.0
        )
    )

    status = result.get(
        "status",
        "UNKNOWN"
    )

    return {

        "candidate_years":
            candidate_years,

        "candidate_months":
            candidate_months,

        "requirement":
            requirement,

        "score":
            safe_float(
                score
            ),

        "status":
            status,
    }


# ============================================================
# EDUCATION FEATURES
# ============================================================

def extract_education_features(
    candidate_text,
    jd_text,
):
    """
    Extract candidate education information
    and calculate education matching.

    calculate_education_match() expects raw
    candidate and JD text.
    """

    candidate_education = (
        extract_education_profile(
            candidate_text
        )
    )

    jd_education = (
        extract_jd_education_requirement(
            jd_text
        )
    )

    result = calculate_education_match(
        candidate_text,
        jd_text
    )

    return {

        "candidate":
            candidate_education,

        "requirement":
            jd_education,

        "degree_match":
            result.get(
                "degree_match",
                {}
            ),

        "field_match":
            result.get(
                "field_match",
                {}
            ),

        "score":
            safe_float(
                result.get(
                    "education_score",
                    0.0
                )
            ),

        "status":
            result.get(
                "status",
                "UNKNOWN"
            ),
    }


# ============================================================
# ROLE FEATURES
# ============================================================

def extract_role_features(
    candidate_text,
    jd_text,
):
    """
    Extract candidate and JD role profiles
    and calculate role relevance.
    """

    candidate_role = build_role_profile(
        candidate_text
    )

    jd_role = build_role_profile(
        jd_text
    )

    candidate_primary = candidate_role.get(
        "primary_role"
    )

    jd_primary = jd_role.get(
        "primary_role"
    )

    candidate_category = candidate_role.get(
        "role_category",
        candidate_role.get(
            "category",
            "Other"
        )
    )

    jd_category = jd_role.get(
        "role_category",
        jd_role.get(
            "category",
            "Other"
        )
    )

    score = 0.0

    # --------------------------------------------------------
    # Exact role match
    # --------------------------------------------------------

    if candidate_primary and jd_primary:

        candidate_normalized = (
            candidate_primary.lower()
        )

        jd_normalized = (
            jd_primary.lower()
        )

        if candidate_normalized == jd_normalized:

            score = 100.0

        elif candidate_category == jd_category:

            score = 75.0

        elif (
            candidate_category == "Other"
            or
            jd_category == "Other"
        ):

            score = 50.0

        else:

            score = 25.0

    # --------------------------------------------------------
    # Category-only match
    # --------------------------------------------------------

    elif candidate_category == jd_category:

        score = 50.0

    return {

        "candidate":
            candidate_role,

        "job":
            jd_role,

        "candidate_primary_role":
            candidate_primary,

        "job_primary_role":
            jd_primary,

        "candidate_category":
            candidate_category,

        "job_category":
            jd_category,

        "score":
            round(
                score,
                2
            ),
    }


# ============================================================
# PROJECT FEATURES
# ============================================================

def extract_project_features(
    candidate_text,
    jd_text,
):
    """
    Extract candidate projects and calculate
    their relevance against the JD.

    Project relevance considers:

        1. Required skill overlap
        2. Preferred skill overlap
        3. Combined skill relevance
        4. JD keyword overlap
        5. JD category match
        6. Number of relevant projects

    The project_extractor.py module calculates
    combined skill relevance using:

        70% required skills
        30% preferred skills

    This function then combines:

        Skill relevance    -> 50%
        Keyword relevance  -> 20%
        Category relevance -> 30%

    A small evidence bonus is added when the
    candidate has relevant projects.
    """

    profile = build_project_profile(
        candidate_text,
        jd_text
    )

    # --------------------------------------------------------
    # Basic project information
    # --------------------------------------------------------

    project_count = int(
        profile.get(
            "project_count",
            0
        )
    )

    relevant_count = int(
        profile.get(
            "relevant_project_count",
            0
        )
    )

    # --------------------------------------------------------
    # Best project relevance
    # --------------------------------------------------------

    best_required_skill_overlap = safe_float(
        profile.get(
            "best_required_skill_overlap",
            0.0
        )
    )

    best_preferred_skill_overlap = safe_float(
        profile.get(
            "best_preferred_skill_overlap",
            0.0
        )
    )

    best_skill_overlap = safe_float(
        profile.get(
            "best_skill_overlap",
            0.0
        )
    )

    best_keyword_overlap = safe_float(
        profile.get(
            "best_keyword_overlap",
            0.0
        )
    )

    best_category_match = safe_float(
        profile.get(
            "best_category_match",
            0.0
        )
    )

    # --------------------------------------------------------
    # Average project relevance
    # --------------------------------------------------------

    average_required_skill_overlap = safe_float(
        profile.get(
            "average_required_skill_overlap",
            0.0
        )
    )

    average_preferred_skill_overlap = safe_float(
        profile.get(
            "average_preferred_skill_overlap",
            0.0
        )
    )

    average_skill_overlap = safe_float(
        profile.get(
            "average_skill_overlap",
            0.0
        )
    )

    average_keyword_overlap = safe_float(
        profile.get(
            "average_keyword_overlap",
            0.0
        )
    )

    average_category_match = safe_float(
        profile.get(
            "average_category_match",
            0.0
        )
    )

    # --------------------------------------------------------
    # Project score
    # --------------------------------------------------------
    #
    # best_skill_overlap already contains the
    # required/preferred weighting from project_extractor.py.
    #
    # Therefore we do not apply another required/preferred
    # weighting here.
    #
    # Main score:
    #
    #   Skill relevance    = 50%
    #   Keyword relevance  = 20%
    #   Category relevance = 30%
    #
    # --------------------------------------------------------

    score = (

        best_skill_overlap * 0.50

        +

        best_keyword_overlap * 0.20

        +

        best_category_match * 0.30
    )

    # --------------------------------------------------------
    # Evidence bonus
    # --------------------------------------------------------
    #
    # Multiple relevant projects provide stronger evidence.
    #
    # 2+ relevant projects -> +5
    # 1 relevant project   -> +2
    #

    if relevant_count >= 2:

        score += 5.0

    elif relevant_count == 1:

        score += 2.0

    score = min(
        100.0,
        score
    )

    # --------------------------------------------------------
    # Return complete project feature set
    # --------------------------------------------------------

    return {

        "profile":
            profile,

        "project_count":
            project_count,

        "relevant_project_count":
            relevant_count,

        "score":
            round(
                score,
                2
            ),

        # ----------------------------------------------------
        # Best project metrics
        # ----------------------------------------------------

        "best_required_skill_overlap":
            best_required_skill_overlap,

        "best_preferred_skill_overlap":
            best_preferred_skill_overlap,

        "best_skill_overlap":
            best_skill_overlap,

        "best_keyword_overlap":
            best_keyword_overlap,

        "best_category_match":
            best_category_match,

        # ----------------------------------------------------
        # Average project metrics
        # ----------------------------------------------------

        "average_required_skill_overlap":
            average_required_skill_overlap,

        "average_preferred_skill_overlap":
            average_preferred_skill_overlap,

        "average_skill_overlap":
            average_skill_overlap,

        "average_keyword_overlap":
            average_keyword_overlap,

        "average_category_match":
            average_category_match,
    }


# ============================================================
# SIMILARITY FEATURES
# ============================================================

def extract_similarity_features(
    candidate_text,
    jd_text,
    semantic_model=None,
):
    """
    Calculate TF-IDF and semantic similarity.
    """

    tfidf_score = calculate_tfidf_score(
        jd_text,
        candidate_text
    )

    semantic_score = calculate_semantic_score(
        jd_text,
        candidate_text,
        semantic_model
    )

    return {

        "tfidf_score":
            safe_float(
                tfidf_score
            ),

        "semantic_score":
            safe_float(
                semantic_score
            ),
    }


# ============================================================
# COMPLETE FEATURE EXTRACTION
# ============================================================

def extract_candidate_features(
    candidate_text,
    jd_text,
    semantic_model=None,
):
    """
    Build the complete feature vector for one candidate.

    Final candidate scoring is intentionally handled
    separately by screening_engine.py.
    """

    if not candidate_text:

        candidate_text = ""

    if not jd_text:

        jd_text = ""

    # --------------------------------------------------------
    # Feature groups
    # --------------------------------------------------------

    skills = extract_skill_features(
        candidate_text,
        jd_text
    )

    experience = extract_experience_features(
        candidate_text,
        jd_text
    )

    education = extract_education_features(
        candidate_text,
        jd_text
    )

    role = extract_role_features(
        candidate_text,
        jd_text
    )

    projects = extract_project_features(
        candidate_text,
        jd_text
    )

    similarity = extract_similarity_features(
        candidate_text,
        jd_text,
        semantic_model
    )

    return {

        "skills":
            skills,

        "experience":
            experience,

        "education":
            education,

        "role":
            role,

        "projects":
            projects,

        "similarity":
            similarity,

        "final_score":
            None,
    }


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def build_candidate_features(
    candidate_text,
    jd_text,
    semantic_model=None,
):
    """
    Backward-compatible function name.

    screening_engine.py currently imports
    build_candidate_features().

    Internally this uses the unified
    feature extraction pipeline.
    """

    return extract_candidate_features(
        candidate_text,
        jd_text,
        semantic_model
    )


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(pdf_path):
    """
    Extract text from a PDF resume.
    """

    document = pymupdf.open(
        pdf_path
    )

    pages = []

    for page in document:

        pages.append(
            page.get_text()
        )

    document.close()

    return "\n".join(
        pages
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("CANDIDATE FEATURE EXTRACTION TEST")
    print("=" * 70)

    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    jd_path = os.path.join(
        BASE_DIR,
        "data",
        "job_descriptions",
        "ml_engineer.txt"
    )

    resume_path = os.path.join(
        BASE_DIR,
        "data",
        "resumes",
        "resume_5.pdf"
    )

    # --------------------------------------------------------
    # Read JD
    # --------------------------------------------------------

    with open(
        jd_path,
        "r",
        encoding="utf-8"
    ) as file:

        jd_text = file.read()

    # --------------------------------------------------------
    # Extract resume
    # --------------------------------------------------------

    candidate_text = extract_pdf_text(
        resume_path
    )

    # --------------------------------------------------------
    # Load semantic model
    # --------------------------------------------------------

    print("\nLoading semantic model...")

    model = load_semantic_model()

    # --------------------------------------------------------
    # Build features
    # --------------------------------------------------------

    features = build_candidate_features(
        candidate_text,
        jd_text,
        model
    )

    # ========================================================
    # SKILLS
    # ========================================================

    print("\n" + "=" * 70)
    print("SKILLS")
    print("=" * 70)

    print(
        "Candidate Skills:",
        features["skills"]["candidate_skills"]
    )

    print(
        "Matched Required:",
        features["skills"]["matched_required"]
    )

    print(
        "Missing Required:",
        features["skills"]["missing_required"]
    )

    print(
        "Matched Preferred:",
        features["skills"]["matched_preferred"]
    )

    print(
        "Missing Preferred:",
        features["skills"]["missing_preferred"]
    )

    print(
        "Required Score:",
        features["skills"]["required_score"],
        "%"
    )

    print(
        "Preferred Score:",
        features["skills"]["preferred_score"],
        "%"
    )

    print(
        "Overall Skill Score:",
        features["skills"]["overall_score"],
        "%"
    )

    # ========================================================
    # EXPERIENCE
    # ========================================================

    print("\n" + "=" * 70)
    print("EXPERIENCE")
    print("=" * 70)

    print(
        "Candidate Experience:",
        features["experience"]["candidate_years"],
        "years"
    )

    print(
        "Experience Score:",
        features["experience"]["score"]
    )

    print(
        "Experience Status:",
        features["experience"]["status"]
    )

    # ========================================================
    # EDUCATION
    # ========================================================

    print("\n" + "=" * 70)
    print("EDUCATION")
    print("=" * 70)

    print(
        "Education Score:",
        features["education"]["score"],
        "%"
    )

    print(
        "Education Status:",
        features["education"]["status"]
    )

    print(
        "Degree Match:",
        features["education"]["degree_match"]
    )

    print(
        "Field Match:",
        features["education"]["field_match"]
    )

    # ========================================================
    # ROLE
    # ========================================================

    print("\n" + "=" * 70)
    print("ROLE")
    print("=" * 70)

    print(
        "Candidate Role:",
        features["role"]["candidate_primary_role"]
    )

    print(
        "Candidate Category:",
        features["role"]["candidate_category"]
    )

    print(
        "JD Role:",
        features["role"]["job_primary_role"]
    )

    print(
        "JD Category:",
        features["role"]["job_category"]
    )

    print(
        "Role Score:",
        features["role"]["score"],
        "%"
    )

    # ========================================================
    # PROJECTS
    # ========================================================

    print("\n" + "=" * 70)
    print("PROJECTS")
    print("=" * 70)

    print(
        "Project Count:",
        features["projects"]["project_count"]
    )

    print(
        "Relevant Projects:",
        features["projects"]["relevant_project_count"]
    )

    print(
        "Project Score:",
        features["projects"]["score"],
        "%"
    )

    print(
        "Best Required Skill Overlap:",
        features["projects"]["best_required_skill_overlap"],
        "%"
    )

    print(
        "Best Preferred Skill Overlap:",
        features["projects"]["best_preferred_skill_overlap"],
        "%"
    )

    print(
        "Best Combined Skill Overlap:",
        features["projects"]["best_skill_overlap"],
        "%"
    )

    print(
        "Best Keyword Overlap:",
        features["projects"]["best_keyword_overlap"],
        "%"
    )

    print(
        "Best Category Match:",
        features["projects"]["best_category_match"],
        "%"
    )

    print(
        "Average Required Skill Overlap:",
        features["projects"]["average_required_skill_overlap"],
        "%"
    )

    print(
        "Average Preferred Skill Overlap:",
        features["projects"]["average_preferred_skill_overlap"],
        "%"
    )

    print(
        "Average Combined Skill Overlap:",
        features["projects"]["average_skill_overlap"],
        "%"
    )

    # ========================================================
    # SIMILARITY
    # ========================================================

    print("\n" + "=" * 70)
    print("SIMILARITY")
    print("=" * 70)

    print(
        "TF-IDF:",
        features["similarity"]["tfidf_score"],
        "%"
    )

    print(
        "Semantic:",
        features["similarity"]["semantic_score"],
        "%"
    )

    # ========================================================
    # COMPLETE
    # ========================================================

    print("\n" + "=" * 70)
    print("FEATURE EXTRACTION COMPLETE")
    print("=" * 70)