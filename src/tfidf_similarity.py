import os
import pymupdf

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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


def calculate_tfidf_similarity(jd_text, resume_texts):
    """
    Calculate TF-IDF cosine similarity between
    the job description and multiple resumes.

    Parameters:
        jd_text: Job description text
        resume_texts: List of resume texts

    Returns:
        List of similarity scores in the same order
        as resume_texts.
    """

    if not resume_texts:
        return []

    documents = [jd_text] + resume_texts

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        documents
    )

    job_vector = tfidf_matrix[0]

    resume_vectors = tfidf_matrix[1:]

    similarity_scores = cosine_similarity(
        job_vector,
        resume_vectors
    )[0]

    return similarity_scores.tolist()


def calculate_tfidf_score(jd_text, resume_text):
    """
    Calculate TF-IDF similarity for one resume.

    Returns:
        Score from 0 to 100.
    """

    scores = calculate_tfidf_similarity(
        jd_text,
        [resume_text]
    )

    if not scores:
        return 0.0

    return scores[0] * 100


def rank_resumes_by_tfidf(jd_text, resume_texts, resume_names):
    """
    Rank resumes according to TF-IDF similarity.
    """

    scores = calculate_tfidf_similarity(
        jd_text,
        resume_texts
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
    Standalone test for TF-IDF similarity.
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

    results = rank_resumes_by_tfidf(
        job_description,
        resume_texts,
        resume_names
    )

    print("\n" + "=" * 60)
    print("TF-IDF CANDIDATE RANKING")
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
            f"TF-IDF Similarity: "
            f"{result['similarity']:.2f}%"
        )

        print("-" * 40)


if __name__ == "__main__":
    main()