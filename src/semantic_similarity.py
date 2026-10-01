import os
import pymupdf

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_MODEL = "all-MiniLM-L6-v2"


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF resume.
    """

    doc = pymupdf.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


def load_semantic_model(
    model_name=DEFAULT_MODEL
):
    """
    Load the Sentence Transformer model.
    """

    return SentenceTransformer(
        model_name
    )


def calculate_semantic_similarity(
    jd_text,
    resume_texts,
    model=None
):
    """
    Calculate semantic similarity between
    a job description and multiple resumes.

    Returns:
        List of similarity scores in the
        same order as resume_texts.
    """

    if not resume_texts:
        return []

    if model is None:
        model = load_semantic_model()

    job_embedding = model.encode(
        [jd_text]
    )

    resume_embeddings = model.encode(
        resume_texts
    )

    similarity_scores = cosine_similarity(
        job_embedding,
        resume_embeddings
    )[0]

    return similarity_scores.tolist()


def calculate_semantic_score(
    jd_text,
    resume_text,
    model=None
):
    """
    Calculate semantic similarity for
    one resume.

    Returns:
        Score from 0 to 100.
    """

    scores = calculate_semantic_similarity(
        jd_text,
        [resume_text],
        model=model
    )

    if not scores:
        return 0.0

    return scores[0] * 100


def rank_resumes_by_semantic(
    jd_text,
    resume_texts,
    resume_names,
    model=None
):
    """
    Rank resumes according to semantic similarity.
    """

    scores = calculate_semantic_similarity(
        jd_text,
        resume_texts,
        model=model
    )

    results = []

    for name, score in zip(
        resume_names,
        scores
    ):
        results.append({
            "resume": name,
            "similarity": score * 100
        })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results


def main():
    """
    Standalone test for semantic similarity.
    """

    jd_path = "data/job_descriptions/ml_engineer.txt"
    resume_folder = "data/resumes"

    with open(
        jd_path,
        "r",
        encoding="utf-8"
    ) as file:
        job_description = file.read()

    resume_texts = []
    resume_names = []

    for filename in os.listdir(resume_folder):

        if filename.lower().endswith(".pdf"):

            resume_path = os.path.join(
                resume_folder,
                filename
            )

            text = extract_text_from_pdf(
                resume_path
            )

            resume_texts.append(text)
            resume_names.append(filename)

    print("\nLoading Sentence Transformer model...")

    model = load_semantic_model()

    results = rank_resumes_by_semantic(
        job_description,
        resume_texts,
        resume_names,
        model=model
    )

    print("\n" + "=" * 60)
    print("SEMANTIC RESUME SIMILARITY")
    print("=" * 60)

    for rank, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\nRank {rank}: "
            f"{result['resume']}"
        )

        print(
            f"Semantic Similarity: "
            f"{result['similarity']:.2f}%"
        )

        print("-" * 40)


if __name__ == "__main__":
    main()