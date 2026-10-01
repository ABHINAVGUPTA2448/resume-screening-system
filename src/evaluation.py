import os
import csv
import pymupdf

from screening_engine import (
    screen_candidate,
    DEFAULT_WEIGHTS
)

from semantic_similarity import load_semantic_model


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

LABELS_PATH = os.path.join(
    BASE_DIR,
    "data",
    "evaluation_labels.csv"
)


# ============================================================
# DEFAULT SETTINGS
# ============================================================

DEFAULT_THRESHOLD = 60.0

THRESHOLDS_TO_TEST = [
    40.0,
    45.0,
    50.0,
    55.0,
    60.0,
    65.0,
    70.0,
    75.0,
    80.0
]


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(pdf_path):
    """
    Extract all text from a PDF resume.
    """

    document = pymupdf.open(
        pdf_path
    )

    pages = []

    try:

        for page in document:

            pages.append(
                page.get_text()
            )

    finally:

        document.close()

    return "\n".join(
        pages
    )


# ============================================================
# LOAD EVALUATION LABELS
# ============================================================

def load_labels():
    """
    Load manually assigned evaluation labels.

    Expected CSV format:

        resume,actual_label
        resume_1.pdf,0
        resume_2.pdf,1

    Returns:
        dict:
            {
                "resume_1.pdf": 0,
                "resume_2.pdf": 1
            }
    """

    if not os.path.exists(LABELS_PATH):

        raise FileNotFoundError(
            f"Evaluation labels file not found: "
            f"{LABELS_PATH}"
        )

    labels = {}

    with open(
        LABELS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(
            file
        )

        # ----------------------------------------------------
        # Validate CSV columns
        # ----------------------------------------------------

        required_columns = {
            "resume",
            "actual_label"
        }

        if not required_columns.issubset(
            set(reader.fieldnames or [])
        ):

            raise ValueError(
                "evaluation_labels.csv must contain "
                "'resume' and 'actual_label' columns."
            )

        # ----------------------------------------------------
        # Read rows
        # ----------------------------------------------------

        for row_number, row in enumerate(
            reader,
            start=2
        ):

            resume_name = (
                row["resume"]
                .strip()
            )

            label_text = (
                row["actual_label"]
                .strip()
            )

            if not resume_name:

                raise ValueError(
                    f"Empty resume name at CSV row "
                    f"{row_number}."
                )

            try:

                actual_label = int(
                    label_text
                )

            except ValueError:

                raise ValueError(
                    f"Invalid label '{label_text}' "
                    f"for {resume_name} at row "
                    f"{row_number}. "
                    f"Expected 0 or 1."
                )

            if actual_label not in (0, 1):

                raise ValueError(
                    f"Invalid actual_label={actual_label} "
                    f"for {resume_name}. "
                    f"Expected 0 or 1."
                )

            if resume_name in labels:

                raise ValueError(
                    f"Duplicate resume entry: "
                    f"{resume_name}"
                )

            labels[resume_name] = actual_label

    if not labels:

        raise ValueError(
            "No evaluation labels were found."
        )

    return labels


# ============================================================
# CALCULATE METRICS
# ============================================================

def calculate_metrics(
    actual,
    predicted
):
    """
    Calculate binary classification metrics.

    Returns percentages for:
        accuracy
        precision
        recall
        f1
    """

    if len(actual) != len(predicted):

        raise ValueError(
            "Actual and predicted lists must "
            "have the same length."
        )

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for a, p in zip(
        actual,
        predicted
    ):

        if a == 1 and p == 1:

            tp += 1

        elif a == 0 and p == 0:

            tn += 1

        elif a == 0 and p == 1:

            fp += 1

        elif a == 1 and p == 0:

            fn += 1

    total = (
        tp
        + tn
        + fp
        + fn
    )

    # --------------------------------------------------------
    # Accuracy
    # --------------------------------------------------------

    accuracy = (
        (tp + tn) / total * 100
        if total > 0
        else 0.0
    )

    # --------------------------------------------------------
    # Precision
    # --------------------------------------------------------

    precision = (
        tp / (tp + fp) * 100
        if (tp + fp) > 0
        else 0.0
    )

    # --------------------------------------------------------
    # Recall
    # --------------------------------------------------------

    recall = (
        tp / (tp + fn) * 100
        if (tp + fn) > 0
        else 0.0
    )

    # --------------------------------------------------------
    # F1
    # --------------------------------------------------------

    if (
        precision + recall
    ) > 0:

        f1 = (
            2
            * precision
            * recall
            / (precision + recall)
        )

    else:

        f1 = 0.0

    return {

        "tp": tp,

        "tn": tn,

        "fp": fp,

        "fn": fn,

        "accuracy":
            accuracy,

        "precision":
            precision,

        "recall":
            recall,

        "f1":
            f1
    }


# ============================================================
# PREDICTIONS
# ============================================================

def generate_predictions(
    results,
    threshold
):
    """
    Convert candidate scores into binary predictions.

    Score >= threshold:
        1 = shortlisted

    Score < threshold:
        0 = not shortlisted
    """

    return [

        1
        if result["score"] >= threshold
        else 0

        for result in results
    ]


# ============================================================
# EVALUATE SYSTEM
# ============================================================

def evaluate_system(
    threshold=DEFAULT_THRESHOLD
):
    """
    Evaluate the complete resume screening system.

    Returns:
        results
        metrics
    """

    if not 0 <= threshold <= 100:

        raise ValueError(
            "Threshold must be between 0 and 100."
        )

    print("\n" + "=" * 80)
    print(
        "STARTING RESUME SCREENING EVALUATION"
    )
    print("=" * 80)

    # --------------------------------------------------------
    # LOAD LABELS
    # --------------------------------------------------------

    print("\nLoading evaluation labels...")

    labels = load_labels()

    print(
        f"Loaded {len(labels)} labeled resumes."
    )

    # --------------------------------------------------------
    # LOAD JOB DESCRIPTION
    # --------------------------------------------------------

    print("\nLoading job description...")

    if not os.path.exists(JD_PATH):

        raise FileNotFoundError(
            f"Job description not found: "
            f"{JD_PATH}"
        )

    with open(
        JD_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        jd_text = file.read()

    if not jd_text.strip():

        raise ValueError(
            "Job description is empty."
        )

    # --------------------------------------------------------
    # LOAD SEMANTIC MODEL
    # --------------------------------------------------------

    print("\nLoading semantic model...")

    semantic_model = load_semantic_model()

    # --------------------------------------------------------
    # EVALUATE CANDIDATES
    # --------------------------------------------------------

    results = []

    print("\nEvaluating candidates...")

    for resume_name, actual_label in labels.items():

        print(
            f"Processing: {resume_name}"
        )

        resume_path = os.path.join(
            RESUME_DIR,
            resume_name
        )

        # ----------------------------------------------------
        # Check resume exists
        # ----------------------------------------------------

        if not os.path.exists(
            resume_path
        ):

            print(
                f"WARNING: File not found: "
                f"{resume_name}"
            )

            continue

        # ----------------------------------------------------
        # Extract resume text
        # ----------------------------------------------------

        resume_text = extract_pdf_text(
            resume_path
        )

        if not resume_text.strip():

            print(
                f"WARNING: No text extracted from "
                f"{resume_name}"
            )

            continue

        # ----------------------------------------------------
        # Screen candidate
        # ----------------------------------------------------

        result = screen_candidate(

            candidate_name=
                resume_name,

            candidate_text=
                resume_text,

            jd_text=
                jd_text,

            semantic_model=
                semantic_model,

            weights=
                DEFAULT_WEIGHTS,

            threshold=
                threshold
        )

        # ----------------------------------------------------
        # Store evaluation result
        # ----------------------------------------------------

        results.append(
            {

                "resume":
                    resume_name,

                "score":
                    float(
                        result["score"]
                    ),

                "actual":
                    actual_label,

                "predicted":
                    (
                        1
                        if result["score"] >= threshold
                        else 0
                    )
            }
        )

    # --------------------------------------------------------
    # Ensure candidates were evaluated
    # --------------------------------------------------------

    if not results:

        raise RuntimeError(
            "No resumes were successfully evaluated."
        )

    # --------------------------------------------------------
    # Build actual/predicted arrays
    # --------------------------------------------------------

    actual = [
        result["actual"]
        for result in results
    ]

    predicted = [
        result["predicted"]
        for result in results
    ]

    # --------------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------------

    metrics = calculate_metrics(
        actual,
        predicted
    )

    return (
        results,
        metrics
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(
    results,
    metrics,
    threshold
):
    """
    Display evaluation results in the terminal.
    """

    print("\n" + "=" * 80)
    print(
        "RESUME SCREENING EVALUATION"
    )
    print("=" * 80)

    print(
        f"\nThreshold: {threshold:.1f}%"
    )

    print(
        f"Evaluated Candidates: {len(results)}"
    )

    print(
        "\n--- CANDIDATE PREDICTIONS ---"
    )

    for result in results:

        prediction = result["predicted"]

        status = (

            "SHORTLISTED"

            if prediction == 1

            else

            "NOT SHORTLISTED"
        )

        print(
            f"{result['resume']}: "
            f"Score={result['score']:.2f}% | "
            f"Actual={result['actual']} | "
            f"Predicted={prediction} | "
            f"{status}"
        )

    # --------------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------------

    print(
        "\n--- CONFUSION MATRIX ---"
    )

    print(
        f"True Positives  (TP): "
        f"{metrics['tp']}"
    )

    print(
        f"True Negatives  (TN): "
        f"{metrics['tn']}"
    )

    print(
        f"False Positives (FP): "
        f"{metrics['fp']}"
    )

    print(
        f"False Negatives (FN): "
        f"{metrics['fn']}"
    )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    print(
        "\n--- PERFORMANCE METRICS ---"
    )

    print(
        f"Accuracy:  "
        f"{metrics['accuracy']:.2f}%"
    )

    print(
        f"Precision: "
        f"{metrics['precision']:.2f}%"
    )

    print(
        f"Recall:    "
        f"{metrics['recall']:.2f}%"
    )

    print(
        f"F1-Score:  "
        f"{metrics['f1']:.2f}%"
    )

    # --------------------------------------------------------
    # Dataset warning
    # --------------------------------------------------------

    if len(results) < 30:

        print("\n--- EVALUATION NOTE ---")

        print(
            "This evaluation uses a small labeled "
            f"dataset of {len(results)} resumes."
        )

        print(
            "The metrics describe performance on "
            "this test set and should not be "
            "interpreted as real-world accuracy."
        )

    print("=" * 80)


# ============================================================
# THRESHOLD ANALYSIS
# ============================================================

def threshold_analysis(
    results,
    thresholds=None
):
    """
    Evaluate system performance across
    multiple shortlisting thresholds.
    """

    print("\n")
    print("=" * 80)
    print(
        "THRESHOLD ANALYSIS"
    )
    print("=" * 80)

    print(
        "\nTesting multiple shortlisting thresholds..."
    )

    if thresholds is None:

        thresholds = THRESHOLDS_TO_TEST

    actual = [
        result["actual"]
        for result in results
    ]

    analysis_results = []

    print()

    print(
        f"{'Threshold':<12}"
        f"{'Accuracy':<12}"
        f"{'Precision':<12}"
        f"{'Recall':<12}"
        f"{'F1':<12}"
        f"{'TP':<6}"
        f"{'FP':<6}"
        f"{'FN':<6}"
    )

    print("-" * 80)

    for threshold in thresholds:

        predicted = generate_predictions(
            results,
            threshold
        )

        metrics = calculate_metrics(
            actual,
            predicted
        )

        row = {

            "threshold":
                threshold,

            **metrics
        }

        analysis_results.append(
            row
        )

        print(
            f"{threshold:<12.0f}"
            f"{metrics['accuracy']:<12.2f}"
            f"{metrics['precision']:<12.2f}"
            f"{metrics['recall']:<12.2f}"
            f"{metrics['f1']:<12.2f}"
            f"{metrics['tp']:<6}"
            f"{metrics['fp']:<6}"
            f"{metrics['fn']:<6}"
        )

    print("-" * 80)

    return analysis_results


# ============================================================
# EVALUATION SUMMARY
# ============================================================

def display_evaluation_summary(
    results,
    metrics,
    threshold
):
    """
    Display a concise final summary.
    """

    shortlisted = sum(
        1
        for result in results
        if result["predicted"] == 1
    )

    not_shortlisted = (
        len(results)
        - shortlisted
    )

    print("\n" + "=" * 80)
    print(
        "EVALUATION SUMMARY"
    )
    print("=" * 80)

    print(
        f"Candidates Evaluated: "
        f"{len(results)}"
    )

    print(
        f"Threshold: "
        f"{threshold:.1f}%"
    )

    print(
        f"Shortlisted: "
        f"{shortlisted}"
    )

    print(
        f"Not Shortlisted: "
        f"{not_shortlisted}"
    )

    print(
        f"Accuracy: "
        f"{metrics['accuracy']:.2f}%"
    )

    print(
        f"Precision: "
        f"{metrics['precision']:.2f}%"
    )

    print(
        f"Recall: "
        f"{metrics['recall']:.2f}%"
    )

    print(
        f"F1-Score: "
        f"{metrics['f1']:.2f}%"
    )

    print("=" * 80)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    THRESHOLD = DEFAULT_THRESHOLD

    # --------------------------------------------------------
    # Run evaluation
    # --------------------------------------------------------

    results, metrics = evaluate_system(
        threshold=THRESHOLD
    )

    # --------------------------------------------------------
    # Display detailed results
    # --------------------------------------------------------

    display_results(
        results,
        metrics,
        THRESHOLD
    )

    # --------------------------------------------------------
    # Threshold analysis
    # --------------------------------------------------------

    threshold_analysis(
        results
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    display_evaluation_summary(
        results,
        metrics,
        THRESHOLD
    )