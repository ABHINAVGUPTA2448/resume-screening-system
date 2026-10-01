import os
import pymupdf

from screening_engine import (
    screen_candidate,
    DEFAULT_WEIGHTS,
)

from semantic_similarity import (
    load_semantic_model,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

RESUME_DIR = os.path.join(
    BASE_DIR,
    "data",
    "resumes"
)

JD_PATH = os.path.join(
    BASE_DIR,
    "data",
    "job_descriptions",
    "ml_engineer.txt"
)


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(pdf_path):
    """
    Extract complete text from a PDF.
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
# CANDIDATE NAME
# ============================================================

def extract_candidate_name(
    text,
    filename
):
    """
    Extract candidate name from the resume.

    Uses the first few non-empty lines as a
    lightweight fallback.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # --------------------------------------------------------
    # Look for explicit name label
    # --------------------------------------------------------

    for line in lines[:15]:

        lower = line.lower()

        if lower.startswith("name:"):

            name = line.split(
                ":",
                1
            )[1].strip()

            if name:

                return name

    # --------------------------------------------------------
    # Otherwise use first suitable line
    # --------------------------------------------------------

    for line in lines[:10]:

        clean = line.strip()

        if (
            len(clean) >= 3
            and len(clean) <= 50
            and not any(
                symbol in clean
                for symbol in [
                    "@",
                    "http",
                    "www.",
                ]
            )
        ):

            lower = clean.lower()

            if lower not in [
                "resume",
                "curriculum vitae",
                "cv",
                "profile",
            ]:

                return clean

    # --------------------------------------------------------
    # Filename fallback
    # --------------------------------------------------------

    return os.path.splitext(
        filename
    )[0]


# ============================================================
# SCREEN ALL RESUMES
# ============================================================

def screen_all_candidates():

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
    # Load semantic model once
    # --------------------------------------------------------

    print(
        "\nLoading semantic model..."
    )

    semantic_model = load_semantic_model()

    # --------------------------------------------------------
    # Find PDFs
    # --------------------------------------------------------

    resume_files = sorted(

        filename

        for filename in os.listdir(
            RESUME_DIR
        )

        if filename.lower().endswith(
            ".pdf"
        )
    )

    if not resume_files:

        print(
            "No PDF resumes found."
        )

        return []

    results = []

    # --------------------------------------------------------
    # Process every resume
    # --------------------------------------------------------

    print(
        "\nScreening candidates..."
    )

    for filename in resume_files:

        pdf_path = os.path.join(
            RESUME_DIR,
            filename
        )

        print(
            f"\nProcessing: {filename}"
        )

        try:

            resume_text = extract_pdf_text(
                pdf_path
            )

            candidate_name = (
                extract_candidate_name(
                    resume_text,
                    filename
                )
            )

            result = screen_candidate(

                candidate_name=candidate_name,

                candidate_text=resume_text,

                jd_text=jd_text,

                semantic_model=semantic_model,

                weights=DEFAULT_WEIGHTS,

                threshold=60.0,
            )

            result["resume"] = filename

            results.append(
                result
            )

        except Exception as error:

            print(
                f"ERROR processing "
                f"{filename}: {error}"
            )

    # --------------------------------------------------------
    # Rank candidates
    # --------------------------------------------------------

    results.sort(

        key=lambda result:
            result["score"],

        reverse=True
    )

    return results


# ============================================================
# DISPLAY RANKING
# ============================================================

def display_ranking(
    results
):

    print("\n")
    print("=" * 90)
    print(
        "AI RESUME SCREENING — CANDIDATE RANKING"
    )
    print("=" * 90)

    if not results:

        print(
            "No candidates were successfully processed."
        )

        return

    print()

    for index, result in enumerate(
        results,
        start=1
    ):

        features = result[
            "features"
        ]

        skills = features[
            "skills"
        ]

        print(
            f"Rank {index}: "
            f"{result['candidate_name']}"
        )

        print(
            f"Resume: "
            f"{result['resume']}"
        )

        print(
            f"Final Score: "
            f"{result['score']:.2f}%"
        )

        print(
            f"Status: "
            f"{result['status']}"
        )

        print(
            f"Required Skills: "
            f"{skills['overall_score']:.2f}%"
        )

        print(
            f"Education: "
            f"{features['education']['score']:.2f}%"
        )

        print(
            f"Role: "
            f"{features['role']['score']:.2f}%"
        )

        print(
            f"Projects: "
            f"{features['projects']['score']:.2f}%"
        )

        print(
            f"Semantic: "
            f"{features['similarity']['semantic_score']:.2f}%"
        )

        if skills["missing_required"]:

            print(
                "Missing Required Skills: "
                +
                ", ".join(
                    skills[
                        "missing_required"
                    ]
                )
            )

        else:

            print(
                "Missing Required Skills: None"
            )

        print(
            "-" * 90
        )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    shortlisted = [

        result

        for result in results

        if result["status"]
        == "SHORTLISTED"
    ]

    print()
    print("=" * 90)
    print("SCREENING SUMMARY")
    print("=" * 90)

    print(
        f"Total Candidates: "
        f"{len(results)}"
    )

    print(
        f"Shortlisted: "
        f"{len(shortlisted)}"
    )

    print(
        f"Not Shortlisted: "
        f"{len(results) - len(shortlisted)}"
    )

    print("=" * 90)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    results = screen_all_candidates()

    display_ranking(
        results
    )