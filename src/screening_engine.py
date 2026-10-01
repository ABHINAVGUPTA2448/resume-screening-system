import os

from candidate_features import (
    build_candidate_features,
)

from semantic_similarity import (
    load_semantic_model,
)


# ============================================================
# DEFAULT WEIGHTS
# ============================================================
#
# These are INITIAL weights.
# They are NOT claimed to be optimal.
#
# We will evaluate and tune them later using
# labeled candidate data.
#
# Experience is handled dynamically when the JD
# does not specify an experience requirement.
# ============================================================

DEFAULT_WEIGHTS = {
    "skills": 0.30,
    "experience": 0.10,
    "education": 0.10,
    "role": 0.10,
    "projects": 0.10,
    "tfidf": 0.10,
    "semantic": 0.20,
}


# ============================================================
# WEIGHT VALIDATION
# ============================================================

def validate_weights(weights):
    """
    Validate that all weights are numeric, non-negative,
    and sum to approximately 1.0.
    """

    if not isinstance(weights, dict):

        raise ValueError(
            "Weights must be provided as a dictionary."
        )

    required_keys = [
        "skills",
        "experience",
        "education",
        "role",
        "projects",
        "tfidf",
        "semantic",
    ]

    for key in required_keys:

        if key not in weights:

            raise ValueError(
                f"Missing weight: {key}"
            )

        try:

            value = float(
                weights[key]
            )

        except (
            TypeError,
            ValueError
        ):

            raise ValueError(
                f"Weight for {key} must be numeric."
            )

        if value < 0:

            raise ValueError(
                f"Weight for {key} cannot be negative."
            )

    total = sum(
        float(value)
        for value in weights.values()
    )

    if abs(total - 1.0) > 1e-6:

        raise ValueError(
            f"Weights must sum to 1.0. "
            f"Current sum: {total}"
        )

    return True


# ============================================================
# SAFE SCORE
# ============================================================

def safe_score(value):
    """
    Convert a score into a safe 0-100 float.

    None means the feature is unavailable.
    """

    if value is None:

        return None

    try:

        score = float(value)

    except (
        TypeError,
        ValueError
    ):

        return None

    return max(
        0.0,
        min(
            100.0,
            score
        )
    )


# ============================================================
# PROJECT SCORE
# ============================================================

def calculate_project_score(
    project_features
):
    """
    Calculate project relevance score.

    Starting heuristic:

        Skill overlap    -> 50%
        Keyword overlap  -> 20%
        Category match   -> 30%

    A small evidence bonus is given when
    multiple relevant projects are detected.

    This will be evaluated/tuned later.
    """

    if not project_features:

        return 0.0

    best_skill_overlap = safe_score(
        project_features.get(
            "best_skill_overlap",
            0.0
        )
    ) or 0.0

    best_keyword_overlap = safe_score(
        project_features.get(
            "best_keyword_overlap",
            0.0
        )
    ) or 0.0

    best_category_match = safe_score(
        project_features.get(
            "best_category_match",
            0.0
        )
    ) or 0.0

    relevant_projects = int(
        project_features.get(
            "relevant_project_count",
            0
        )
    )

    score = (

        best_skill_overlap * 0.50

        +

        best_keyword_overlap * 0.20

        +

        best_category_match * 0.30
    )

    if relevant_projects >= 2:

        score += 5.0

    return round(
        min(
            100.0,
            score
        ),
        2
    )


# ============================================================
# EDUCATION STATUS
# ============================================================

def normalize_education_status(
    education_features
):
    """
    Generate a consistent human-readable education status.

    The education matcher currently returns the actual
    degree/field matching information, while its overall
    status can sometimes remain UNKNOWN.

    Therefore we derive the status from the scores.
    """

    if not education_features:

        return "NOT_SPECIFIED"

    score = safe_score(
        education_features.get(
            "score"
        )
    )

    degree_match = education_features.get(
        "degree_match",
        {}
    )

    field_match = education_features.get(
        "field_match",
        {}
    )

    degree_status = degree_match.get(
        "status"
    )

    field_status = field_match.get(
        "status"
    )

    if (
        degree_status == "DEGREE_SATISFIED"
        and
        field_status == "FIELD_SATISFIED"
    ):

        return "SATISFIED"

    if score is None:

        return "NOT_SPECIFIED"

    if score >= 75:

        return "PARTIALLY_SATISFIED"

    if score > 0:

        return "PARTIAL_MATCH"

    return "NOT_SATISFIED"


# ============================================================
# FINAL SCORE
# ============================================================

def calculate_final_score(
    features,
    weights=None,
):
    """
    Calculate final candidate score.

    Features whose requirements are unavailable
    are excluded and their weights are redistributed
    proportionally across available features.

    This prevents candidates from being unfairly
    penalized when the JD does not specify something
    such as experience.
    """

    if weights is None:

        weights = DEFAULT_WEIGHTS.copy()

    validate_weights(
        weights
    )

    feature_scores = {

        "skills":
            safe_score(
                features["skills"].get(
                    "overall_score"
                )
            ),

        "experience":
            safe_score(
                features["experience"].get(
                    "score"
                )
            ),

        "education":
            safe_score(
                features["education"].get(
                    "score"
                )
            ),

        "role":
            safe_score(
                features["role"].get(
                    "score"
                )
            ),

        "projects":
            safe_score(
                features["projects"].get(
                    "score"
                )
            ),

        "tfidf":
            safe_score(
                features["similarity"].get(
                    "tfidf_score"
                )
            ),

        "semantic":
            safe_score(
                features["similarity"].get(
                    "semantic_score"
                )
            ),
    }

    # --------------------------------------------------------
    # Find available features
    # --------------------------------------------------------

    available_features = {

        key: score

        for key, score
        in feature_scores.items()

        if score is not None
    }

    if not available_features:

        return {
            "final_score": 0.0,
            "feature_scores": feature_scores,
            "contributions": {},
            "used_weights": {},
        }

    # --------------------------------------------------------
    # Redistribute unavailable weights
    # --------------------------------------------------------

    available_weight_total = sum(

        weights[key]

        for key in available_features
    )

    used_weights = {

        key:
        weights[key] / available_weight_total

        for key in available_features
    }

    # --------------------------------------------------------
    # Calculate contributions
    # --------------------------------------------------------

    contributions = {}

    for key, score in available_features.items():

        contributions[key] = round(
            score *
            used_weights[key],
            2
        )

    final_score = sum(
        contributions.values()
    )

    final_score = round(
        final_score,
        2
    )

    return {

        "final_score":
            final_score,

        "feature_scores":
            feature_scores,

        "contributions":
            contributions,

        "used_weights":
            used_weights,
    }


# ============================================================
# SHORTLIST STATUS
# ============================================================

def determine_status(
    final_score,
    threshold=60.0,
):
    """
    Determine shortlist status.
    """

    if final_score >= threshold:

        return "SHORTLISTED"

    return "NOT SHORTLISTED"


# ============================================================
# EXPLANATION GENERATOR
# ============================================================

def generate_explanation(
    features,
    score_result,
):
    """
    Generate an explainable screening summary.
    """

    explanation = []

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    skills = features.get(
        "skills",
        {}
    )

    missing_required = skills.get(
        "missing_required",
        []
    )

    matched_required = skills.get(
        "matched_required",
        []
    )

    if missing_required:

        explanation.append(
            "Missing required skills: "
            +
            ", ".join(
                missing_required
            )
        )

    elif matched_required:

        explanation.append(
            "All required skills matched."
        )

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    education = features.get(
        "education",
        {}
    )

    education_score = safe_score(
        education.get(
            "score"
        )
    )

    education_status = (
        normalize_education_status(
            education
        )
    )

    if education_score is not None:

        explanation.append(
            f"Education status: "
            f"{education_status} "
            f"({education_score:.1f}%)."
        )

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    experience = features.get(
        "experience",
        {}
    )

    experience_score = safe_score(
        experience.get(
            "score"
        )
    )

    experience_status = experience.get(
        "status"
    )

    if experience_score is not None:

        explanation.append(
            f"Experience status: "
            f"{experience_status} "
            f"({experience_score:.1f}%)."
        )

    elif experience_status == "NOT_SPECIFIED":

        explanation.append(
            "Experience requirement was not specified "
            "in the job description."
        )

    # --------------------------------------------------------
    # Role
    # --------------------------------------------------------

    role = features.get(
        "role",
        {}
    )

    role_score = safe_score(
        role.get(
            "score"
        )
    )

    candidate_role = role.get(
        "candidate_primary_role"
    )

    job_role = role.get(
        "job_primary_role"
    )

    if role_score is not None:

        explanation.append(
            f"Role relevance: "
            f"{role_score:.1f}%."
        )

    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    projects = features.get(
        "projects",
        {}
    )

    project_score = safe_score(
        projects.get(
            "score"
        )
    )

    project_count = projects.get(
        "project_count",
        0
    )

    relevant_count = projects.get(
        "relevant_project_count",
        0
    )

    explanation.append(
        f"Relevant projects: "
        f"{relevant_count}/{project_count}."
    )

    # --------------------------------------------------------
    # TF-IDF
    # --------------------------------------------------------

    similarity = features.get(
        "similarity",
        {}
    )

    tfidf = safe_score(
        similarity.get(
            "tfidf_score"
        )
    )

    semantic = safe_score(
        similarity.get(
            "semantic_score"
        )
    )

    if tfidf is not None:

        explanation.append(
            f"TF-IDF similarity: "
            f"{tfidf:.1f}%."
        )

    if semantic is not None:

        explanation.append(
            f"Semantic similarity: "
            f"{semantic:.1f}%."
        )

    return explanation


# ============================================================
# SCREEN ONE CANDIDATE
# ============================================================

def screen_candidate(
    candidate_name,
    candidate_text,
    jd_text,
    semantic_model=None,
    weights=None,
    threshold=60.0,
):
    """
    Complete screening pipeline for one candidate.
    """

    if semantic_model is None:

        semantic_model = load_semantic_model()

    features = build_candidate_features(
        candidate_text,
        jd_text,
        semantic_model
    )

    score_result = calculate_final_score(
        features,
        weights
    )

    final_score = score_result[
        "final_score"
    ]

    status = determine_status(
        final_score,
        threshold
    )

    explanation = generate_explanation(
        features,
        score_result
    )

    # Add derived education status
    features["education"][
        "status"
    ] = normalize_education_status(
        features["education"]
    )

    return {

        "candidate_name":
            candidate_name,

        "features":
            features,

        "score":
            final_score,

        "status":
            status,

        "score_details":
            score_result,

        "explanation":
            explanation,
    }


# ============================================================
# DISPLAY RESULT
# ============================================================

def display_screening_result(
    result
):
    """
    Print a readable screening result.
    """

    print("\n" + "=" * 70)

    print(
        f"CANDIDATE: "
        f"{result['candidate_name']}"
    )

    print("=" * 70)

    print(
        f"\nFINAL SCORE: "
        f"{result['score']:.2f}%"
    )

    print(
        f"STATUS: "
        f"{result['status']}"
    )

    features = result[
        "features"
    ]

    details = result[
        "score_details"
    ]

    print(
        "\n--- FEATURE SCORES ---"
    )

    feature_scores = details[
        "feature_scores"
    ]

    labels = {

        "skills":
            "Skills",

        "experience":
            "Experience",

        "education":
            "Education",

        "role":
            "Role",

        "projects":
            "Projects",

        "tfidf":
            "TF-IDF",

        "semantic":
            "Semantic",
    }

    for key, label in labels.items():

        value = feature_scores.get(
            key
        )

        if value is None:

            print(
                f"{label}: Not specified"
            )

        else:

            print(
                f"{label}: "
                f"{value:.2f}%"
            )

    print(
        "\n--- SCORE CONTRIBUTIONS ---"
    )

    contributions = details[
        "contributions"
    ]

    for key, label in labels.items():

        if key in contributions:

            print(
                f"{label}: "
                f"{contributions[key]:.2f}"
            )

        else:

            print(
                f"{label}: Not used"
            )

    print(
        "\n--- EXPLANATION ---"
    )

    for item in result[
        "explanation"
    ]:

        print(
            f"• {item}"
        )

    print(
        "=" * 70
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    JD_PATH = os.path.join(
        BASE_DIR,
        "data",
        "job_descriptions",
        "ml_engineer.txt"
    )

    RESUME_PATH = os.path.join(
        BASE_DIR,
        "data",
        "resumes",
        "resume_5.pdf"
    )

    # --------------------------------------------------------
    # Read JD
    # --------------------------------------------------------

    with open(
        JD_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        jd_text = file.read()

    # --------------------------------------------------------
    # Read resume
    # --------------------------------------------------------

    import pymupdf

    document = pymupdf.open(
        RESUME_PATH
    )

    pages = []

    for page in document:

        pages.append(
            page.get_text()
        )

    document.close()

    candidate_text = "\n".join(
        pages
    )

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    print(
        "\nLoading semantic model..."
    )

    semantic_model = load_semantic_model()

    # --------------------------------------------------------
    # Screen candidate
    # --------------------------------------------------------

    result = screen_candidate(

        candidate_name="Kavya Gupta",

        candidate_text=candidate_text,

        jd_text=jd_text,

        semantic_model=semantic_model,

        weights=DEFAULT_WEIGHTS,

        threshold=60.0,
    )

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    display_screening_result(
        result
    )