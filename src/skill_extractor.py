import re
import os
import pymupdf


SKILLS = [
    "python",
    "machine learning",
    "pandas",
    "numpy",
    "scikit-learn",
    "sql",
    "data analysis",
    "statistics",
    "deep learning",
    "tensorflow",
    "pytorch",
    "natural language processing",
    "git",
    "docker"
]
def extract_candidate_name(text):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    if len(lines) > 0:
        return lines[0]

    return "Unknown Candidate"

def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found_skills.append(skill)

    return found_skills


def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


def calculate_skill_match(required_skills, candidate_skills):

    matched_skills = set(required_skills) & set(candidate_skills)

    if len(required_skills) == 0:
        score = 0
    else:
        score = (len(matched_skills) / len(required_skills)) * 100

    return list(matched_skills), score


def screen_resume(resume_path, required_skills):

    resume_text = extract_text_from_pdf(resume_path)

    candidate_name = extract_candidate_name(resume_text)
    candidate_skills = extract_skills(resume_text)

    matched_skills, score = calculate_skill_match(
        required_skills,
        candidate_skills
    )

    return {
        "resume": os.path.basename(resume_path),
        "candidate_name": candidate_name,
        "candidate_skills": candidate_skills,
        "matched_skills": matched_skills,
        "score": score
    }

# -----------------------------
# Main Program
# -----------------------------

jd_path = "data/job_descriptions/ml_engineer.txt"

with open(jd_path, "r", encoding="utf-8") as file:
    jd_text = file.read()

required_skills = extract_skills(jd_text)

resume_folder = "data/resumes"

results = []

for filename in os.listdir(resume_folder):

    if filename.lower().endswith(".pdf"):

        resume_path = os.path.join(resume_folder, filename)

        result = screen_resume(
            resume_path,
            required_skills
        )

        results.append(result)


# Sort candidates by skill score
results.sort(
    key=lambda x: x["score"],
    reverse=True
)


# Display ranking
print("\n" + "=" * 40)
print("CANDIDATE RANKING")
print("=" * 40)

SHORTLIST_THRESHOLD = 60

for rank, result in enumerate(results, start=1):

    print(f"Rank {rank}: {result['candidate_name']}")
    print(f"Resume: {result['resume']}")
    print(f"Candidate Skills: {', '.join(result['candidate_skills'])}")
    print(f"Matched Skills: {', '.join(result['matched_skills'])}")
    print(f"Skill Match Score: {result['score']:.2f}%")
    
    if result["score"] >= SHORTLIST_THRESHOLD:
       status = "SHORTLISTED"
    else:
       status = "NOT SHORTLISTED"

    print(f"Status: {status}")