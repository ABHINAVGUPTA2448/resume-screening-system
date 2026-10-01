\# AI-Based Resume Screening and Candidate Shortlisting System



\## HCL Project P\_204



An AI-powered resume screening and candidate shortlisting system that automatically extracts information from resumes, compares candidates against a job description, calculates explainable suitability scores, ranks candidates, and identifies candidates who meet a configurable shortlist threshold.



The system combines structured feature extraction, TF-IDF similarity, and Sentence-Transformer semantic similarity to provide a comprehensive candidate evaluation pipeline.



\---



\# 1. Project Overview



Recruitment teams may need to process a large number of resumes for a single job opening. Manual resume screening can be time-consuming and can make candidate comparison difficult when many resumes need to be evaluated against the same requirements.



This project provides an automated resume screening pipeline that:



1\. Accepts candidate resumes in PDF format.

2\. Extracts text from resumes.

3\. Identifies relevant candidate information.

4\. Extracts skills, education, experience, role, and project information.

5\. Processes a job description.

6\. Compares candidate resumes with the job requirements.

7\. Calculates lexical similarity using TF-IDF.

8\. Calculates semantic similarity using Sentence Transformers.

9\. Calculates feature-level scores.

10\. Combines the scores using weighted scoring.

11\. Generates an explainable candidate result.

12\. Ranks multiple candidates.

13\. Applies a configurable shortlisting threshold.

14\. Exposes the screening functionality through a FastAPI backend.

15\. Provides an interactive Streamlit interface.



\---



\# 2. Problem Statement



Traditional resume screening often depends on manual review or simple keyword matching.



These approaches can have several limitations:



\* Large numbers of resumes require significant manual effort.

\* Keyword matching may miss semantically similar skills.

\* Candidates may describe the same technology using different terminology.

\* Candidate comparison can become inconsistent.

\* Manual screening can be difficult to scale.

\* A single keyword match does not necessarily indicate meaningful relevance.

\* Recruiters may need to consider multiple factors such as skills, education, experience, role relevance, and projects.



The proposed system automates the initial screening process by combining structured candidate analysis with lexical and semantic similarity.



The system is intended as a decision-support tool for initial screening rather than an autonomous replacement for human recruitment decisions.



\---



\# 3. Objectives



The main objectives of the project are:



\* Automate resume text extraction.

\* Extract important candidate information.

\* Identify candidate skills.

\* Analyze education.

\* Analyze experience.

\* Analyze role relevance.

\* Analyze project relevance.

\* Compare resumes with job descriptions.

\* Implement TF-IDF similarity.

\* Implement semantic similarity using Sentence Transformers.

\* Combine multiple signals into a weighted score.

\* Rank multiple candidates.

\* Automatically identify candidates meeting the configured threshold.

\* Provide score explanations.

\* Provide REST API access.

\* Provide a user-friendly demonstration interface.

\* Provide an evaluation framework.

\* Create a modular architecture that can be extended in the future.



\---



\# 4. Key Features



\## 4.1 Resume PDF Upload



The system accepts resume files in PDF format.



The uploaded PDF is processed automatically and converted into text for further analysis.



\---



\## 4.2 PDF Text Extraction



The project uses PyMuPDF for extracting text from PDF resumes.



```text

Resume PDF

&#x20;   â†“

PDF Parser

&#x20;   â†“

Extracted Text

```



The extracted text becomes the input for feature extraction and similarity analysis.



\---



\## 4.3 Candidate Feature Extraction



The system analyzes candidate resumes for multiple categories.



\### Skills



Examples:



```text

Python

Java

Machine Learning

Deep Learning

NLP

SQL

TensorFlow

Scikit-learn

FastAPI

Git

```



\### Education



Examples:



```text

B.Tech

B.E.

BCA

M.Tech

MCA

Bachelor's Degree

Master's Degree

```



\### Experience



The system attempts to identify relevant professional or practical experience.



\### Role



The system analyzes role-related information and compares it with the target position.



\### Projects



Projects are considered as an additional indicator of practical technical exposure.



\---



\# 5. System Architecture



```text

&#x20;                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                        â”‚   Recruiter / User    â”‚

&#x20;                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                        â”‚    Streamlit UI      â”‚

&#x20;                        â”‚ Dashboard / Upload   â”‚

&#x20;                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â”‚ HTTP

&#x20;                                   â–¼

&#x20;                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                        â”‚   FastAPI Backend    â”‚

&#x20;                        â”‚    backend/main.py   â”‚

&#x20;                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                        â”‚ Resume Processing    â”‚

&#x20;                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                        â”‚ PDF Text Extraction  â”‚

&#x20;                        â”‚      PyMuPDF         â”‚

&#x20;                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                   â”‚       Feature Extraction       â”‚

&#x20;                   â”‚                                â”‚

&#x20;                   â”‚ Skills                         â”‚

&#x20;                   â”‚ Education                      â”‚

&#x20;                   â”‚ Experience                     â”‚

&#x20;                   â”‚ Role                           â”‚

&#x20;                   â”‚ Projects                       â”‚

&#x20;                   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                   â”‚      Similarity Analysis       â”‚

&#x20;                   â”‚                                â”‚

&#x20;                   â”‚ TF-IDF Similarity              â”‚

&#x20;                   â”‚ Sentence-Transformer Semantic â”‚

&#x20;                   â”‚ Similarity                      â”‚

&#x20;                   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                   â”‚       Weighted Scoring         â”‚

&#x20;                   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                   â”‚      Explainability Layer      â”‚

&#x20;                   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                   â”‚      Ranking \& Shortlisting    â”‚

&#x20;                   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                   â”‚        API / UI Results        â”‚

&#x20;                   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

```



\---



\# 6. End-to-End Workflow



```text

&#x20;                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                â”‚ Resume PDF(s)  â”‚

&#x20;                â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                        â”‚

&#x20;                        â–¼

&#x20;               â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;               â”‚ PDF Text Extract  â”‚

&#x20;               â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                        â”‚

&#x20;                        â–¼

&#x20;             â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;             â”‚ Text Preprocessing     â”‚

&#x20;             â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                         â”‚

&#x20;                         â–¼

&#x20;             â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;             â”‚ Candidate Feature      â”‚

&#x20;             â”‚ Extraction             â”‚

&#x20;             â”‚                        â”‚

&#x20;             â”‚ Skills                 â”‚

&#x20;             â”‚ Education              â”‚

&#x20;             â”‚ Experience             â”‚

&#x20;             â”‚ Role                   â”‚

&#x20;             â”‚ Projects               â”‚

&#x20;             â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                         â”‚

&#x20;                         â–¼

&#x20;             â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;             â”‚ Job Description        â”‚

&#x20;             â”‚ Processing             â”‚

&#x20;             â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                         â”‚

&#x20;                         â–¼

&#x20;            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;            â”‚ Similarity Calculation   â”‚

&#x20;            â”‚                          â”‚

&#x20;            â”‚ TF-IDF                   â”‚

&#x20;            â”‚ Semantic Similarity      â”‚

&#x20;            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                         â”‚

&#x20;                         â–¼

&#x20;            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;            â”‚ Weighted Score           â”‚

&#x20;            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                         â”‚

&#x20;                         â–¼

&#x20;            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;            â”‚ Explainable Result       â”‚

&#x20;            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                         â”‚

&#x20;                         â–¼

&#x20;            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;            â”‚ Candidate Ranking        â”‚

&#x20;            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                         â”‚

&#x20;                         â–¼

&#x20;            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;            â”‚ Shortlisting             â”‚

&#x20;            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

```



\---



\# 7. Similarity Analysis



The project uses two major text similarity techniques.



\## 7.1 TF-IDF Similarity



TF-IDF stands for:



```text

Term Frequency - Inverse Document Frequency

```



TF-IDF converts textual content into numerical vectors based on the importance of words.



The resume and job description are converted into vectors and compared using cosine similarity.



```text

Resume

&#x20;  â”‚

&#x20;  â–¼

TF-IDF Vectorizer

&#x20;  â”‚

&#x20;  â–¼

Resume Vector

&#x20;  â”‚

&#x20;  â”‚

&#x20;  â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–º Cosine Similarity

&#x20;  â”‚

&#x20;  â”‚

Job Description

&#x20;  â”‚

&#x20;  â–¼

TF-IDF Vectorizer

&#x20;  â”‚

&#x20;  â–¼

Job Description Vector

```



\### Advantages



\* Easy to understand.

\* Computationally efficient.

\* Useful for keyword and terminology overlap.

\* Good baseline for text matching.

\* Relatively easy to explain.



\### Limitations



\* Primarily based on lexical overlap.

\* Can struggle with synonyms.

\* Does not fully understand contextual meaning.

\* Different wording may result in lower similarity even when the concepts are related.



\---



\# 8. Semantic Similarity



The project also uses Sentence-Transformer embeddings.



A Sentence Transformer converts text into numerical vectors called embeddings.



Conceptually:



```text

Resume

&#x20;  â†“

Sentence Transformer

&#x20;  â†“

Resume Embedding

&#x20;  â”‚

&#x20;  â”‚

&#x20;  â”œâ”€â”€â”€â”€â”€â”€ Similarity â”€â”€â”€â”€â”€â”€â”

&#x20;  â”‚                        â”‚

&#x20;  â†“                        â†“

Job Description       Job Embedding

&#x20;  â†“

Sentence Transformer

```



Semantic similarity helps identify relationships between text even when the exact words are different.



For example:



```text

Resume:

"Built predictive models using Python and scikit-learn."



Job Description:

"Experience developing machine learning models in Python."

```



The exact wording differs, but the concepts are closely related.



\---



\# 9. Why Use Both TF-IDF and Semantic Similarity?



Using only keyword matching can miss semantic relationships.



Using only semantic similarity may not provide enough direct lexical evidence.



Therefore, this project combines both approaches.



| Method               | Main Strength                  |

| -------------------- | ------------------------------ |

| TF-IDF               | Direct lexical overlap         |

| Sentence Transformer | Semantic/contextual similarity |



The combined approach provides two complementary signals:



```text

&#x20;               Resume

&#x20;                 â”‚

&#x20;       â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;       â–¼                   â–¼

&#x20;    TF-IDF             Semantic

&#x20;    Matching            Matching

&#x20;       â”‚                   â”‚

&#x20;       â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                 â–¼

&#x20;         Combined Scoring

```



\---



\# 10. Weighted Scoring Model



The current scoring configuration uses the following weights:



| Component           |   Weight |

| ------------------- | -------: |

| Skills              |      30% |

| Experience          |      10% |

| Education           |      10% |

| Role                |      10% |

| Projects            |      10% |

| TF-IDF Similarity   |      10% |

| Semantic Similarity |      20% |

| \*\*Total\*\*           | \*\*100%\*\* |



The conceptual formula is:



```text

Final Score =

&#x20;   Skills Ã— 0.30

&#x20; + Experience Ã— 0.10

&#x20; + Education Ã— 0.10

&#x20; + Role Ã— 0.10

&#x20; + Projects Ã— 0.10

&#x20; + TF-IDF Ã— 0.10

&#x20; + Semantic Ã— 0.20

```



The implementation can also handle unavailable feature values by redistributing applicable weight rather than automatically treating missing extraction as a complete negative signal.



\---



\# 11. Shortlisting



The current configured shortlist threshold is:



```text

60%

```



Candidates with a final score at or above the configured threshold are marked:



```text

SHORTLISTED

```



Candidates below the threshold are marked:



```text

NOT SHORTLISTED

```



The threshold can be changed according to project requirements.



\---



\# 12. Explainability



The system is designed to show not only the final score but also the individual contributing components.



Example:



```text

Candidate:

KAVYA GUPTA



Final Score:

80.54%



Status:

SHORTLISTED



Score Components:



Skills              â†’ Component score

Experience          â†’ Component score

Education           â†’ Component score

Role                â†’ Component score

Projects            â†’ Component score

TF-IDF              â†’ Component score

Semantic Similarity â†’ Component score

```



This makes the output easier to inspect than a single unexplained number.



\---



\# 13. Candidate Ranking



For multiple resumes, the system processes each candidate independently.



```text

Resume 1 â”€â”€â–º Score

Resume 2 â”€â”€â–º Score

Resume 3 â”€â”€â–º Score

Resume 4 â”€â”€â–º Score

Resume 5 â”€â”€â–º Score

&#x20;                 â”‚

&#x20;                 â–¼

&#x20;            Sort by Score

&#x20;                 â”‚

&#x20;                 â–¼

&#x20;            Ranked Results

```



The ranking is based on the final calculated score.



\---



\# 14. Current Five-Resume Test



The project has been tested using:



```text

5 sample resumes

\+

1 ML Engineer job description

```



The observed current test results include:



| Rank | Candidate / Resume          |           Score | Status          |

| ---: | --------------------------- | --------------: | --------------- |

|    1 | KAVYA GUPTA / resume\_5.pdf  |          80.54% | SHORTLISTED     |

|    2 | RAHUL SHARMA / resume\_2.pdf |          71.13% | SHORTLISTED     |

|    3 | resume\_4.pdf                |          50.68% | NOT SHORTLISTED |

|    4 | resume\_3.pdf                |          34.81% | NOT SHORTLISTED |

|    5 | resume\_1.pdf                |          30.76% | NOT SHORTLISTED |



These values are project test outputs for the sample dataset and current implementation. They should not be interpreted as universal assessments of the individuals represented by the sample resumes.



\---



\# 15. API



The backend is implemented using FastAPI.



The default local server is:



```text

http://127.0.0.1:8000

```



\---



\## 15.1 Swagger UI



FastAPI automatically provides interactive API documentation at:



```text

http://127.0.0.1:8000/docs

```



\---



\## 15.2 OpenAPI Specification



The OpenAPI JSON specification is available at:



```text

http://127.0.0.1:8000/openapi.json

```



\---



\# 16. API Endpoints



\## GET `/health`



Used to verify whether the backend is running.



Example:



```text

GET /health

```



Possible response:



```json

{

&#x20; "status": "ok"

}

```



\---



\# 17. POST `/screen`



The `/screen` endpoint is used to screen an individual resume against a job description.



Typical input:



```text

Resume PDF

\+

Job Description

```



Typical output:



```text

Candidate

Component Scores

Final Score

Shortlist Status

Explanation

```



Example:



```json

{

&#x20; "candidate": "KAVYA GUPTA",

&#x20; "score": 80.54,

&#x20; "status": "SHORTLISTED"

}

```



The exact response fields depend on the current implementation.



\---



\# 18. POST `/rank`



The `/rank` endpoint is used for batch candidate screening.



Typical input:



```text

Multiple Resume PDFs

\+

Job Description

```



Workflow:



```text

Multiple Resumes

&#x20;      â”‚

&#x20;      â–¼

Individual Screening

&#x20;      â”‚

&#x20;      â–¼

Score Calculation

&#x20;      â”‚

&#x20;      â–¼

Candidate Ranking

&#x20;      â”‚

&#x20;      â–¼

Shortlist Status

```



Typical output:



```text

Rank

Candidate

Score

Status

Component Scores

Explanation

```



\---



\# 19. Project Structure



The project is organized approximately as follows:



```text

resume-screening-system/

â”‚

â”œâ”€â”€ app/

â”‚   â””â”€â”€ ...

â”‚

â”œâ”€â”€ backend/

â”‚   â””â”€â”€ main.py

â”‚

â”œâ”€â”€ src/

â”‚   â”œâ”€â”€ screening\_engine.py

â”‚   â”œâ”€â”€ candidate\_features.py

â”‚   â”œâ”€â”€ semantic\_similarity.py

â”‚   â”œâ”€â”€ evaluation.py

â”‚   â””â”€â”€ ...

â”‚

â”œâ”€â”€ data/

â”‚   â”œâ”€â”€ resumes/

â”‚   â”‚   â”œâ”€â”€ resume\_1.pdf

â”‚   â”‚   â”œâ”€â”€ resume\_2.pdf

â”‚   â”‚   â”œâ”€â”€ resume\_3.pdf

â”‚   â”‚   â”œâ”€â”€ resume\_4.pdf

â”‚   â”‚   â””â”€â”€ resume\_5.pdf

â”‚   â”‚

â”‚   â”œâ”€â”€ job\_descriptions/

â”‚   â”‚   â””â”€â”€ ml\_engineer.txt

â”‚   â”‚

â”‚   â””â”€â”€ evaluation\_labels/

â”‚       â””â”€â”€ ...

â”‚

â”œâ”€â”€ database/

â”‚   â””â”€â”€ ...

â”‚

â”œâ”€â”€ models/

â”‚   â””â”€â”€ ...

â”‚

â”œâ”€â”€ notebooks/

â”‚   â””â”€â”€ ...

â”‚

â”œâ”€â”€ requirements.txt

â””â”€â”€ README.md

```



File names can change as the project continues to develop.



\---



\# 20. Important Source Files



\## `backend/main.py`



The main FastAPI backend.



Responsibilities include:



\* Creating the FastAPI application.

\* Defining API endpoints.

\* Receiving uploaded resume files.

\* Receiving job descriptions.

\* Calling the screening engine.

\* Returning structured responses.

\* Providing OpenAPI documentation.



\---



\## `src/screening\_engine.py`



The main screening and scoring pipeline.



Responsibilities include:



\* Candidate processing.

\* Feature scoring.

\* Similarity calculation.

\* Weighted score calculation.

\* Shortlisting.

\* Result generation.

\* Explainability.



\---



\## `src/candidate\_features.py`



Responsible for candidate feature extraction.



Potential feature categories include:



```text

Skills

Education

Experience

Role

Projects

```



\---



\## `src/semantic\_similarity.py`



Responsible for semantic similarity using Sentence-Transformer embeddings.



Typical process:



```text

Text

&#x20;â†“

Embedding Model

&#x20;â†“

Vector Representation

&#x20;â†“

Similarity Calculation

```



\---



\## `src/evaluation.py`



Used to evaluate the screening system.



Potential evaluation areas include:



\* Candidate scores.

\* Ranking.

\* Shortlisting.

\* Classification metrics.

\* Evaluation labels.

\* Screening performance.



\---



\# 21. Technology Stack



| Layer                | Technology                 |

| -------------------- | -------------------------- |

| Programming Language | Python                     |

| Backend              | FastAPI                    |

| Server               | Uvicorn                    |

| Frontend / UI        | Streamlit                  |

| PDF Processing       | PyMuPDF                    |

| Machine Learning     | Scikit-learn               |

| Semantic NLP         | Sentence Transformers      |

| Numerical Processing | NumPy                      |

| Data Processing      | Pandas                     |

| Database             | SQLite                     |

| API Documentation    | OpenAPI / Swagger          |

| Environment          | Python Virtual Environment |



\---



\# 22. Installation



\## Step 1 â€” Navigate to the project



Open PowerShell:



```powershell

cd C:\\Users\\abhin\\OneDrive\\Desktop\\resume-screening-system

```



\---



\## Step 2 â€” Create virtual environment



```powershell

python -m venv venv

```



\---



\## Step 3 â€” Activate virtual environment



```powershell

.\\venv\\Scripts\\Activate.ps1

```



After activation:



```text

(venv) PS C:\\Users\\abhin\\OneDrive\\Desktop\\resume-screening-system>

```



\---



\## Step 4 â€” Install dependencies



```powershell

pip install -r requirements.txt

```



\---



\# 23. Running the Backend



From the project root:



```powershell

uvicorn backend.main:app --reload

```



The backend should start at:



```text

http://127.0.0.1:8000

```



Open Swagger:



```text

http://127.0.0.1:8000/docs

```



Open OpenAPI:



```text

http://127.0.0.1:8000/openapi.json

```



\---



\# 24. Running the Streamlit UI



The Streamlit interface can be launched using the project's Streamlit entry file.



For example:



```powershell

streamlit run app/streamlit_app.py

```



If the entry file has a different name in the current project structure, use that file instead.



The intended UI workflow is:



```text

Dashboard

&#x20;   â†“

Resume Screening

&#x20;   â†“

Upload Resume(s)

&#x20;   â†“

Provide Job Description

&#x20;   â†“

Run Screening

&#x20;   â†“

View Scores

&#x20;   â†“

View Ranking

&#x20;   â†“

View Shortlist

&#x20;   â†“

View Explanation

```



\---



\# 25. API Testing



Swagger provides an easy way to test the backend manually.



Open:



```text

http://127.0.0.1:8000/docs

```



Then:



1\. Select the required endpoint.

2\. Click `Try it out`.

3\. Upload the resume file.

4\. Enter or upload the job description if required.

5\. Execute the request.

6\. Inspect the response.

7\. Verify the score and status.



\---



\# 26. Sample Data



The current project testing setup uses:



```text

5 Resume PDFs

\+

1 ML Engineer Job Description

```



Example structure:



```text

data/

â”œâ”€â”€ resumes/

â”‚   â”œâ”€â”€ resume\_1.pdf

â”‚   â”œâ”€â”€ resume\_2.pdf

â”‚   â”œâ”€â”€ resume\_3.pdf

â”‚   â”œâ”€â”€ resume\_4.pdf

â”‚   â””â”€â”€ resume\_5.pdf

â”‚

â””â”€â”€ job\_descriptions/

&#x20;   â””â”€â”€ ml\_engineer.txt

```



The sample data is intended for development, demonstration, and evaluation.



\---



\# 27. Example Job Description



A simplified ML Engineer job description may contain requirements such as:



```text

Python

Machine Learning

Deep Learning

NLP

Data Processing

Model Development

Model Deployment

Scikit-learn

TensorFlow

SQL

```



The system compares these requirements with the candidate resume.



\---



\# 28. Example Processing



Input:



```text

Resume:

Candidate Resume PDF



Job:

ML Engineer Job Description

```



Processing:



```text

PDF Extraction

&#x20;     â†“

Text Preprocessing

&#x20;     â†“

Feature Extraction

&#x20;     â†“

Skill Matching

&#x20;     â†“

Education Matching

&#x20;     â†“

Experience Matching

&#x20;     â†“

Role Matching

&#x20;     â†“

Project Matching

&#x20;     â†“

TF-IDF Similarity

&#x20;     â†“

Semantic Similarity

&#x20;     â†“

Weighted Score

&#x20;     â†“

Explanation

&#x20;     â†“

Shortlist Decision

```



Output:



```text

Candidate:

KAVYA GUPTA



Score:

80.54%



Status:

SHORTLISTED

```



\---



\# 29. Example API Response



A simplified API response can look like:



```json

{

&#x20; "candidate": "KAVYA GUPTA",

&#x20; "score": 80.54,

&#x20; "status": "SHORTLISTED",

&#x20; "components": {

&#x20;   "skills": 0.0,

&#x20;   "experience": 0.0,

&#x20;   "education": 0.0,

&#x20;   "role": 0.0,

&#x20;   "projects": 0.0,

&#x20;   "tfidf": 0.0,

&#x20;   "semantic": 0.0

&#x20; }

}

```



The numerical component values above are placeholders illustrating the response structure. The actual values are generated by the current implementation.



\---



\# 30. Evaluation



Evaluation is an important part of an AI-based screening system.



The system should not be evaluated only on whether the API runs successfully.



It should also be evaluated using appropriate data and labels.



Possible evaluation areas include:



```text

Candidate Classification

Candidate Ranking

Shortlisting

Score Distribution

Similarity Quality

Feature Extraction

```



\---



\# 31. Classification Metrics



If labeled evaluation data is available, standard classification metrics can be calculated.



\## Accuracy



```text

Accuracy =

Correct Predictions / Total Predictions

```



\---



\## Precision



```text

Precision =

True Positives /

(True Positives + False Positives)

```



\---



\## Recall



```text

Recall =

True Positives /

(True Positives + False Negatives)

```



\---



\## F1 Score



```text

F1 =

2 Ã— Precision Ã— Recall /

(Precision + Recall)

```



For a real recruitment system, evaluation should go beyond a single metric and should also consider ranking behavior, false-positive/false-negative patterns, dataset quality, and fairness.



\---



\# 32. Why Explainability Matters



A recruitment screening system should not ideally produce only:



```text

Score = 80%

```



It should provide information about how that score was produced.



For example:



```text

Final Score

&#x20;    â”‚

&#x20;    â”œâ”€â”€ Skills

&#x20;    â”œâ”€â”€ Experience

&#x20;    â”œâ”€â”€ Education

&#x20;    â”œâ”€â”€ Role

&#x20;    â”œâ”€â”€ Projects

&#x20;    â”œâ”€â”€ TF-IDF

&#x20;    â””â”€â”€ Semantic Similarity

```



This allows a recruiter or evaluator to inspect the contributing factors.



\---



\# 33. Human-in-the-Loop Design



The intended workflow is:



```text

AI Screening

&#x20;     â†“

Candidate Ranking

&#x20;     â†“

Score Explanation

&#x20;     â†“

Human Review

&#x20;     â†“

Final Recruitment Decision

```



The system is therefore designed as a decision-support prototype.



Final employment decisions should remain subject to appropriate human review and organizational processes.



\---



\# 34. Bias and Fairness Considerations



Automated screening systems can inherit biases from:



\* Training data.

\* Historical recruitment practices.

\* Resume datasets.

\* Feature definitions.

\* Job descriptions.

\* Model behavior.

\* Evaluation labels.



Potential safeguards include:



\* Avoiding unnecessary sensitive personal attributes.

\* Auditing model behavior.

\* Testing false positives and false negatives.

\* Testing representative evaluation datasets.

\* Monitoring potentially disparate outcomes where legally and ethically appropriate.

\* Keeping human reviewers involved.

\* Reviewing scoring rules regularly.

\* Documenting model limitations.



The current project is an academic/industry prototype and should not be considered a fully validated production recruitment system.



\---



\# 35. Privacy Considerations



Resumes can contain personally identifiable information.



A production implementation should consider:



\* Secure file upload.

\* Access control.

\* Encryption.

\* Secure storage.

\* Data retention policies.

\* Secure deletion.

\* Authentication.

\* Authorization.

\* Input validation.

\* File-size restrictions.

\* Malware scanning.

\* Secure logging.

\* Minimization of stored personal information.



The local development prototype should not automatically be considered production-grade from a privacy or security perspective.



\---



\# 36. Security Considerations



Potential production security improvements include:



```text

Authentication

&#x20;     â†“

Authorization

&#x20;     â†“

Secure File Upload

&#x20;     â†“

File Validation

&#x20;     â†“

Malware Scanning

&#x20;     â†“

Secure Processing

&#x20;     â†“

Controlled Storage

&#x20;     â†“

Audit Logging

```



Additional considerations:



\* Limit uploaded file size.

\* Restrict allowed file types.

\* Validate PDF files.

\* Avoid arbitrary file execution.

\* Protect API endpoints.

\* Add rate limiting.

\* Use secure secrets management.

\* Use HTTPS in production.



\---



\# 37. Advantages



The proposed system provides:



\* Automated resume screening.

\* Faster initial processing.

\* Batch candidate comparison.

\* Structured feature analysis.

\* Lexical similarity.

\* Semantic similarity.

\* Weighted scoring.

\* Candidate ranking.

\* Shortlisting.

\* Explainable component scores.

\* REST API.

\* Swagger documentation.

\* Streamlit interface.

\* Evaluation support.

\* Modular architecture.

\* Potential for future deployment and integration.



\---



\# 38. Limitations



The current prototype has several limitations.



\### 1. Resume Format Variation



Different resumes use different layouts and section names.



This can affect extraction quality.



\### 2. PDF Extraction



Image-based or scanned PDFs may not produce usable text without OCR.



\### 3. Feature Extraction



Rule-based extraction can miss information that is expressed in unusual ways.



\### 4. Terminology



Candidates may use different terms for similar skills.



\### 5. Semantic Model



Semantic similarity depends on the selected pretrained model.



\### 6. Scoring Weights



The weights represent project configuration and should not be interpreted as objective measures of candidate quality.



\### 7. Dataset Size



The current demonstration dataset is small compared with real recruitment datasets.



\### 8. Evaluation Labels



Evaluation quality depends heavily on the quality and representativeness of the labels.



\### 9. Bias



Automated screening can reproduce biases in data, features, or rules.



\### 10. Production Readiness



The current implementation is primarily a project prototype and would require additional security, privacy, scalability, monitoring, and validation work before production use.



\---



\# 39. Future Scope



\## 39.1 Advanced Resume Parsing



Future improvements could include:



\* OCR.

\* Better section detection.

\* Named Entity Recognition.

\* Better experience extraction.

\* Better education extraction.

\* Support for DOCX.

\* Support for additional document formats.

\* Layout-aware document processing.



\---



\## 39.2 Skill Intelligence



Possible improvements:



\* Skill taxonomy.

\* Skill normalization.

\* Skill synonyms.

\* Related-skill detection.

\* Skill proficiency estimation.

\* Skill gap analysis.



Example:



```text

Python

&#x20; â”œâ”€â”€ NumPy

&#x20; â”œâ”€â”€ Pandas

&#x20; â”œâ”€â”€ Scikit-learn

&#x20; â””â”€â”€ FastAPI

```



\---



\## 39.3 Advanced Semantic Matching



Future versions could explore:



\* Better domain-specific embedding models.

\* Fine-tuned transformer models.

\* Cross-encoder reranking.

\* Job-specific embeddings.

\* Section-level semantic matching.



\---



\## 39.4 Explainability Improvements



Future versions could provide:



```text

Matched Skills

Missing Skills

Relevant Resume Sections

Relevant Experience

Relevant Projects

Semantic Match Evidence

Score Breakdown

```



For example:



```text

Matched Skills:

âœ“ Python

âœ“ Machine Learning

âœ“ NLP

âœ“ SQL



Missing / Weak Evidence:

â–³ Docker

â–³ Kubernetes

```



\---



\## 39.5 Dashboard



A future dashboard could include:



```text

Total Candidates

&#x20;       â”‚

&#x20;       â”œâ”€â”€ Shortlisted

&#x20;       â”œâ”€â”€ Not Shortlisted

&#x20;       â”œâ”€â”€ Average Score

&#x20;       â”œâ”€â”€ Skill Distribution

&#x20;       â””â”€â”€ Candidate Ranking

```



\---



\## 39.6 Database Integration



Candidate information can be stored in a structured database.



Possible future schema:



```text

Candidate

&#x20;   â”‚

&#x20;   â”œâ”€â”€ Personal Information

&#x20;   â”œâ”€â”€ Education

&#x20;   â”œâ”€â”€ Skills

&#x20;   â”œâ”€â”€ Experience

&#x20;   â”œâ”€â”€ Projects

&#x20;   â”œâ”€â”€ Scores

&#x20;   â””â”€â”€ Screening History

```



\---



\## 39.7 Production Deployment



Future deployment could include:



```text

Frontend

&#x20;  â†“

API Gateway

&#x20;  â†“

FastAPI

&#x20;  â†“

Screening Engine

&#x20;  â†“

ML Models

&#x20;  â†“

Database

```



Potential deployment environments could include cloud infrastructure and containerized services.



\---



\# 40. Development Environment



The project is currently developed locally on Windows using PowerShell and a Python virtual environment.



Project root:



```text

C:\\Users\\abhin\\OneDrive\\Desktop\\resume-screening-system

```



Typical development workflow:



```powershell

cd C:\\Users\\abhin\\OneDrive\\Desktop\\resume-screening-system



.\\venv\\Scripts\\Activate.ps1



uvicorn backend.main:app --reload

```



Then open:



```text

http://127.0.0.1:8000/docs

```



\---



\# 41. Troubleshooting



\## Backend Does Not Start



Check that the virtual environment is active:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

pip install -r requirements.txt

```



Then run:



```powershell

uvicorn backend.main:app --reload

```



\---



\## Swagger Does Not Open



Verify that FastAPI is running.



Then open:



```text

http://127.0.0.1:8000/docs

```



\---



\## PDF Produces Little or No Text



The PDF may be:



\* Scanned.

\* Image-based.

\* Protected.

\* Poorly structured.



Potential future solution:



```text

PDF

&#x20;â†“

Text Extraction

&#x20;â†“

If insufficient text

&#x20;â†“

OCR

&#x20;â†“

Extracted Text

```



\---



\## Sentence Transformer Error



The semantic model may need to be downloaded the first time it is used.



Ensure:



\* Required Python dependencies are installed.

\* The machine can access the required model resources.

\* The model name configured by the project is valid.



\---



\## Evaluation Script Syntax Error



Python files must contain valid Python syntax.



For example:



Correct:



```python

\_\_file\_\_

```



Incorrect:



```text

\*\*file\*\*

```



Markdown formatting must not accidentally be inserted into Python source files.



\---



\# 42. Project Demonstration



A recommended HCL/project demonstration sequence is:



```text

1\. Start the backend

&#x20;       â†“

2\. Open Swagger

&#x20;       â†“

3\. Test /health

&#x20;       â†“

4\. Demonstrate /screen

&#x20;       â†“

5\. Upload one sample resume

&#x20;       â†“

6\. Provide ML Engineer job description

&#x20;       â†“

7\. Display candidate score

&#x20;       â†“

8\. Display component scores

&#x20;       â†“

9\. Display shortlist status

&#x20;       â†“

10\. Demonstrate /rank

&#x20;       â†“

11\. Upload five resumes

&#x20;       â†“

12\. Generate ranking

&#x20;       â†“

13\. Show shortlisted candidates

&#x20;       â†“

14\. Open Streamlit interface

&#x20;       â†“

15\. Demonstrate complete workflow

```



\---



\# 43. Suggested Presentation Explanation



A simple explanation for the project presentation is:



> The system automates the initial stage of resume screening. It accepts resumes and a job description, extracts candidate information, analyzes skills, education, experience, roles, and projects, and then compares the resume with the job description using both TF-IDF and Sentence-Transformer semantic similarity. These signals are combined using weighted scoring to generate a final candidate score. Candidates can then be ranked and filtered using a configurable shortlist threshold. The system also provides component-level results to improve explainability.



\---



\# 44. Example Candidate Processing



Suppose a candidate's resume contains:



```text

Python

Machine Learning

NLP

Scikit-learn

FastAPI

B.Tech CSE

Machine Learning Project

```



And the job description contains:



```text

Python

Machine Learning

NLP

Data Processing

Model Development

Deployment

```



The system may detect:



```text

Direct Skill Matches

&#x20;       +

Related Semantic Concepts

&#x20;       +

Project Relevance

&#x20;       +

Education

&#x20;       +

Role / Experience

```



These signals are then incorporated into the final score.



\---



\# 45. Complete Screening Pipeline



```text

&#x20;                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                â”‚       Resume PDF(s)        â”‚

&#x20;                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                               â”‚

&#x20;                               â–¼

&#x20;                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                â”‚     PDF Text Extraction    â”‚

&#x20;                â”‚          PyMuPDF           â”‚

&#x20;                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                               â”‚

&#x20;                               â–¼

&#x20;                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                â”‚     Text Preprocessing     â”‚

&#x20;                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                               â”‚

&#x20;                               â–¼

&#x20;            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;            â”‚       Candidate Feature Analysis    â”‚

&#x20;            â”‚                                     â”‚

&#x20;            â”‚  Skills                              â”‚

&#x20;            â”‚  Education                           â”‚

&#x20;            â”‚  Experience                          â”‚

&#x20;            â”‚  Role                                â”‚

&#x20;            â”‚  Projects                            â”‚

&#x20;            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                              â”‚

&#x20;                              â–¼

&#x20;            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;            â”‚        Job Description Analysis      â”‚

&#x20;            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                              â”‚

&#x20;                              â–¼

&#x20;            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;            â”‚         Similarity Analysis          â”‚

&#x20;            â”‚                                     â”‚

&#x20;            â”‚        TF-IDF Similarity             â”‚

&#x20;            â”‚               +                     â”‚

&#x20;            â”‚     Sentence Transformer            â”‚

&#x20;            â”‚       Semantic Similarity            â”‚

&#x20;            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                              â”‚

&#x20;                              â–¼

&#x20;            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;            â”‚          Weighted Scoring            â”‚

&#x20;            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                              â”‚

&#x20;                              â–¼

&#x20;            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;            â”‚          Explainability              â”‚

&#x20;            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                              â”‚

&#x20;                              â–¼

&#x20;            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;            â”‚             Ranking                  â”‚

&#x20;            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                              â”‚

&#x20;                              â–¼

&#x20;            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;            â”‚         Shortlist Threshold          â”‚

&#x20;            â”‚              60%                     â”‚

&#x20;            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                              â”‚

&#x20;                              â–¼

&#x20;            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;            â”‚       FastAPI / Streamlit UI         â”‚

&#x20;            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

```



\---



\# 46. Project Outcomes



The prototype demonstrates an end-to-end AI-assisted resume screening workflow:



```text

Resume

&#x20; â†“

Extraction

&#x20; â†“

Feature Analysis

&#x20; â†“

TF-IDF Matching

&#x20; +

Semantic Matching

&#x20; â†“

Weighted Scoring

&#x20; â†“

Explainability

&#x20; â†“

Ranking

&#x20; â†“

Shortlisting

&#x20; â†“

API / UI Result

```



The current test setup demonstrates batch screening and ranking using five sample resumes against an ML Engineer job description.



\---



\# 47. Key Project Highlights



```text

âœ“ AI-Assisted Resume Screening

âœ“ PDF Resume Extraction

âœ“ Skill Extraction

âœ“ Education Analysis

âœ“ Experience Analysis

âœ“ Role Analysis

âœ“ Project Analysis

âœ“ TF-IDF Similarity

âœ“ Sentence-Transformer Similarity

âœ“ Weighted Candidate Scoring

âœ“ Candidate Ranking

âœ“ Automated Shortlisting

âœ“ Explainable Results

âœ“ FastAPI Backend

âœ“ Swagger/OpenAPI

âœ“ Streamlit Interface

âœ“ Evaluation Framework

âœ“ SQLite Support

âœ“ Modular Architecture

âœ“ Human-in-the-Loop Workflow

```



\---



\# 48. Academic / Industry Relevance



This project demonstrates practical application of:



\* Natural Language Processing.

\* Machine Learning.

\* Information Retrieval.

\* Semantic Search.

\* Text Similarity.

\* Feature Engineering.

\* REST API Development.

\* Backend Development.

\* Frontend/Dashboard Development.

\* Database Concepts.

\* Model Evaluation.

\* Explainable AI.



It therefore combines multiple areas of software engineering and AI/ML into a single end-to-end system.



\---



\# 49. Conclusion



The \*\*AI-Based Resume Screening and Candidate Shortlisting System\*\* provides an end-to-end prototype for automating the initial stage of recruitment screening.



The system combines:



```text

PDF Processing

&#x20;     +

Feature Extraction

&#x20;     +

TF-IDF Similarity

&#x20;     +

Semantic Similarity

&#x20;     +

Weighted Scoring

&#x20;     +

Explainability

&#x20;     +

Ranking

&#x20;     +

Shortlisting

```



The modular architecture allows individual components to be improved independently.



Future versions can incorporate better resume parsing, OCR, advanced semantic models, skill taxonomies, richer explanations, candidate dashboards, database integration, security controls, and production deployment capabilities.



The system is designed to assist with initial candidate screening and comparison while retaining appropriate human review for consequential recruitment decisions.



\---



\# 50. References



\## Python



```text

https://www.python.org/

```



\## FastAPI



```text

https://fastapi.tiangolo.com/

```



\## Uvicorn



```text

https://www.uvicorn.org/

```



\## Streamlit



```text

https://streamlit.io/

```



\## PyMuPDF



```text

https://pymupdf.readthedocs.io/

```



\## Scikit-learn



```text

https://scikit-learn.org/

```



\## Sentence Transformers



```text

https://www.sbert.net/

```



\---



\# 51. Project Information



\*\*Project ID:\*\* P\_204



\*\*Project Title:\*\* AI-Based Resume Screening and Candidate Shortlisting System



\*\*Project Category:\*\* AI / Machine Learning



\*\*Institution:\*\* ABES Engineering College



\*\*Student:\*\* Abhinav Gupta



\*\*Degree:\*\* B.Tech Computer Science and Engineering



\*\*Project Type:\*\* HCL Industry / Academic Project



\---



\# 52. License



This project is an academic and industry-project prototype.



Before public or commercial deployment, review the licenses and usage requirements of:



\* Third-party Python libraries.

\* Pretrained models.

\* Datasets.

\* Sample resumes.

\* External resources.

\* APIs.

\* Other dependencies.



\---



\# 53. Quick Start



The shortest setup process is:



```powershell

cd C:\\Users\\abhin\\OneDrive\\Desktop\\resume-screening-system

```



Activate the environment:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

pip install -r requirements.txt

```



Start FastAPI:



```powershell

uvicorn backend.main:app --reload

```



Open Swagger:



```text

http://127.0.0.1:8000/docs

```



Run Streamlit using the project's current application entry file:



```powershell

streamlit run app/streamlit_app.py

```



\---



\# 54. Final Architecture Summary



```text

&#x20;                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                        â”‚       USER           â”‚

&#x20;                        â”‚     / RECRUITER      â”‚

&#x20;                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                        â”‚     STREAMLIT UI     â”‚

&#x20;                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                        â”‚    FASTAPI API       â”‚

&#x20;                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                        â”‚ RESUME PROCESSOR     â”‚

&#x20;                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                        â”‚   PDF EXTRACTION     â”‚

&#x20;                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                   â”‚   FEATURE EXTRACTION         â”‚

&#x20;                   â”‚                              â”‚

&#x20;                   â”‚ Skills                       â”‚

&#x20;                   â”‚ Education                    â”‚

&#x20;                   â”‚ Experience                   â”‚

&#x20;                   â”‚ Role                         â”‚

&#x20;                   â”‚ Projects                     â”‚

&#x20;                   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                  â”‚

&#x20;                                  â–¼

&#x20;                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                â”‚       SIMILARITY ENGINE             â”‚

&#x20;                â”‚                                    â”‚

&#x20;                â”‚ TF-IDF                             â”‚

&#x20;                â”‚ Sentence Transformers             â”‚

&#x20;                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                 â”‚

&#x20;                                 â–¼

&#x20;                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                â”‚       WEIGHTED SCORING              â”‚

&#x20;                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                 â”‚

&#x20;                                 â–¼

&#x20;                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                â”‚        EXPLAINABILITY               â”‚

&#x20;                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                 â”‚

&#x20;                                 â–¼

&#x20;                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                â”‚          CANDIDATE RANKING           â”‚

&#x20;                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                 â”‚

&#x20;                                 â–¼

&#x20;                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                â”‚       SHORTLISTING â‰¥ 60%             â”‚

&#x20;                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                 â”‚

&#x20;                                 â–¼

&#x20;                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                â”‚       FINAL RESULTS                 â”‚

&#x20;                â”‚                                    â”‚

&#x20;                â”‚ Score                              â”‚

&#x20;                â”‚ Rank                               â”‚

&#x20;                â”‚ Status                             â”‚

&#x20;                â”‚ Component Scores                   â”‚

&#x20;                â”‚ Explanation                        â”‚

&#x20;                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

```



\---



\# End of README



\*\*AI-Based Resume Screening and Candidate Shortlisting System â€” HCL P\_204\*\*




