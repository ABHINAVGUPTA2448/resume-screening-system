# app/streamlit_app.py

import json
import requests
import streamlit as st


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="ResumeAI | Candidate Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = "http://127.0.0.1:8000"


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(
                    circle at 10% 0%,
                    rgba(99, 102, 241, 0.10),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 90% 10%,
                    rgba(168, 85, 247, 0.08),
                    transparent 25%
                ),
                #09090f;
        }

        [data-testid="stSidebar"] {
            background: #0d0d15;
        }

        .block-container {
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, h4 {
            color: #ffffff !important;
        }

        .hero-box {
            padding: 2rem;
            border-radius: 24px;
            background:
                linear-gradient(
                    135deg,
                    rgba(99, 102, 241, 0.20),
                    rgba(168, 85, 247, 0.10),
                    rgba(15, 15, 25, 0.90)
                );
            border: 1px solid rgba(139, 92, 246, 0.25);
            margin-bottom: 1.5rem;
        }

        .hero-label {
            color: #a5b4fc;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            margin-bottom: 0.7rem;
        }

        .hero-heading {
            color: white;
            font-size: 2.8rem;
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -0.04em;
            margin-bottom: 0.8rem;
        }

        .hero-text {
            color: #b8b8c7;
            font-size: 1rem;
            line-height: 1.6;
            max-width: 850px;
        }

        .metric-box {
            padding: 1rem;
            border-radius: 16px;
            background: rgba(20, 20, 31, 0.80);
            border: 1px solid rgba(255,255,255,0.07);
            min-height: 120px;
        }

        .candidate-box {
            padding: 1.3rem;
            border-radius: 20px;
            background: rgba(18,18,28,0.88);
            border: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 1rem;
        }

        .small-muted {
            color: #888899;
            font-size: 0.82rem;
        }

        .score-large {
            font-size: 2rem;
            font-weight: 800;
        }

        .stButton > button {
            border-radius: 12px;
            min-height: 2.8rem;
            font-weight: 700;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# GENERIC HELPERS
# ============================================================

def safe_float(value, default=0.0):
    try:
        if value is None:
            return default

        if isinstance(value, str):
            value = value.replace("%", "").strip()

        return float(value)

    except (ValueError, TypeError):
        return default


def safe_int(value, default=0):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


def clean_text(value):
    if value is None:
        return ""

    return str(value).strip()


def normalize_list(value):
    """
    Convert API values into a clean list.

    Supports:
    - list
    - tuple
    - set
    - string
    - dictionaries
    - JSON strings
    """

    if value is None:
        return []

    if isinstance(value, (list, tuple, set)):
        return list(value)

    if isinstance(value, dict):
        possible_keys = [
            "skills",
            "matched",
            "missing",
            "matched_skills",
            "missing_skills",
            "items",
            "results",
            "projects",
        ]

        for key in possible_keys:
            if key in value:
                return normalize_list(value[key])

        return list(value.values())

    if isinstance(value, str):
        text = value.strip()

        if not text:
            return []

        if text.startswith("[") and text.endswith("]"):
            try:
                parsed = json.loads(text)
                return normalize_list(parsed)
            except Exception:
                pass

        return [text]

    return [value]


def clean_list(value):
    result = []

    for item in normalize_list(value):

        if item is None:
            continue

        if isinstance(item, dict):

            item_text = (
                item.get("name")
                or item.get("skill")
                or item.get("title")
                or item.get("project")
                or item.get("text")
            )

            if item_text:
                item = item_text

        text = str(item).strip()

        if text:
            result.append(text)

    # remove duplicates
    final = []
    seen = set()

    for item in result:

        key = item.lower()

        if key not in seen:
            seen.add(key)
            final.append(item)

    return final


# ============================================================
# SCORE HELPERS
# ============================================================

def get_scores(candidate):

    scores = candidate.get("scores")

    if not isinstance(scores, dict):
        scores = {}

    similarity = candidate.get("similarity")

    if not isinstance(similarity, dict):
        similarity = {}

    return {
        "skills": safe_float(scores.get("skills")),
        "experience": safe_float(scores.get("experience")),
        "education": safe_float(scores.get("education")),
        "role": safe_float(scores.get("role")),
        "projects": safe_float(scores.get("projects")),

        "tfidf": safe_float(
            scores.get(
                "tfidf",
                similarity.get("tfidf_score", 0)
            )
        ),

        "semantic": safe_float(
            scores.get(
                "semantic",
                similarity.get("semantic_score", 0)
            )
        ),
    }


# ============================================================
# SKILL EXTRACTION
# ============================================================

def get_skill_data(candidate):

    skills = candidate.get("skills")

    if not isinstance(skills, dict):
        skills = {}

    matched_required = (
        skills.get("matched_required")
        or skills.get("matched_required_skills")
        or skills.get("matched")
        or []
    )

    missing_required = (
        skills.get("missing_required")
        or skills.get("missing_required_skills")
        or skills.get("missing")
        or []
    )

    matched_preferred = (
        skills.get("matched_preferred")
        or skills.get("matched_preferred_skills")
        or []
    )

    missing_preferred = (
        skills.get("missing_preferred")
        or skills.get("missing_preferred_skills")
        or []
    )

    # Extra fallbacks
    if not matched_required:
        matched_required = candidate.get("matched_required", [])

    if not missing_required:
        missing_required = candidate.get("missing_required", [])

    if not matched_preferred:
        matched_preferred = candidate.get("matched_preferred", [])

    if not missing_preferred:
        missing_preferred = candidate.get("missing_preferred", [])

    return {
        "matched_required": clean_list(matched_required),
        "missing_required": clean_list(missing_required),
        "matched_preferred": clean_list(matched_preferred),
        "missing_preferred": clean_list(missing_preferred),
    }


# ============================================================
# HISTORY PARSING
# ============================================================

def extract_history_sessions(data):

    if isinstance(data, list):
        return data

    if not isinstance(data, dict):
        return []

    # Most common structures
    for key in [
        "sessions",
        "history",
        "data",
        "results",
    ]:
        value = data.get(key)

        if isinstance(value, list):
            return value

    # Sometimes backend returns:
    # {"status": "success", "history": {...}}
    history = data.get("history")

    if isinstance(history, dict):

        for key in [
            "sessions",
            "data",
            "results",
        ]:
            value = history.get(key)

            if isinstance(value, list):
                return value

    return []


def get_history():

    try:

        response = requests.get(
            f"{BACKEND_URL}/history",
            timeout=10,
        )

        if response.status_code != 200:
            return []

        data = response.json()

        return extract_history_sessions(data)

    except Exception:
        return []


def extract_session_candidates(session):

    if not isinstance(session, dict):
        return []

    for key in [
        "candidates",
        "results",
        "ranked_candidates",
        "candidate_results",
    ]:

        value = session.get(key)

        if isinstance(value, list):
            return value

    return []


def session_candidate_count(session):

    candidates = extract_session_candidates(session)

    if candidates:
        return len(candidates)

    for key in [
        "total_candidates",
        "candidate_count",
        "candidates_count",
    ]:

        if key in session:
            return safe_int(session[key])

    return 0


def session_shortlisted_count(session):

    candidates = extract_session_candidates(session)

    if candidates:

        return sum(
            1
            for candidate in candidates
            if str(
                candidate.get("status", "")
            ).upper() == "SHORTLISTED"
        )

    for key in [
        "total_shortlisted",
        "shortlisted_count",
        "shortlisted",
    ]:

        if key in session:
            return safe_int(session[key])

    return 0


def session_average_score(session):

    candidates = extract_session_candidates(session)

    if candidates:

        scores = [
            safe_float(candidate.get("score"))
            for candidate in candidates
            if candidate.get("score") is not None
        ]

        if scores:
            return sum(scores) / len(scores)

    for key in [
        "average_score",
        "avg_score",
        "average",
        "mean_score",
    ]:

        if key in session:
            return safe_float(session[key])

    return 0.0


def calculate_history_stats(history):

    total_sessions = len(history)

    total_candidates = 0
    total_shortlisted = 0
    session_averages = []

    for session in history:

        if not isinstance(session, dict):
            continue

        count = session_candidate_count(session)

        shortlisted = session_shortlisted_count(session)

        average = session_average_score(session)

        total_candidates += count
        total_shortlisted += shortlisted

        if count > 0:
            session_averages.append(average)

    average_score = (
        sum(session_averages) / len(session_averages)
        if session_averages
        else 0
    )

    shortlist_rate = (
        total_shortlisted / total_candidates * 100
        if total_candidates
        else 0
    )

    return {
        "sessions": total_sessions,
        "candidates": total_candidates,
        "shortlisted": total_shortlisted,
        "average": average_score,
        "shortlist_rate": shortlist_rate,
    }


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("✦ ResumeAI")

    st.caption("Candidate Intelligence Platform")

    st.success("● BACKEND ONLINE")

    st.divider()

    st.subheader("Workspace")

    st.write("✦ AI Engine")
    st.write("✦ Skill Matching")
    st.write("✦ Education Matching")
    st.write("✦ Role Intelligence")
    st.write("✦ Project Analysis")
    st.write("✦ TF-IDF Similarity")
    st.write("✦ Semantic Similarity")
    st.write("✦ Explainable AI")

    st.divider()

    st.subheader("System")

    st.write("Python + FastAPI")
    st.write("Streamlit Interface")
    st.write("SQLite History")
    st.write("ML + NLP Pipeline")

    st.divider()

    st.caption("ResumeAI v1.0.0")
    st.caption("AI-Based Resume Screening System")


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-label">● AI ENGINE ONLINE</div>
        <div class="hero-heading">
            Candidate intelligence,<br>
            powered by AI.
        </div>
        <div class="hero-text">
            Analyze resumes against job requirements using skill matching,
            education intelligence, role relevance, project analysis,
            TF-IDF similarity, semantic similarity and explainable AI.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HISTORY
# ============================================================

history = get_history()

stats = calculate_history_stats(history)


# ============================================================
# SYSTEM OVERVIEW
# ============================================================

st.caption("SYSTEM OVERVIEW")

st.header("Live screening system statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "TOTAL SESSIONS",
        stats["sessions"],
        "Screening runs",
    )

with col2:
    st.metric(
        "CANDIDATES SCREENED",
        stats["candidates"],
        "Resume evaluations",
    )

with col3:
    st.metric(
        "TOTAL SHORTLISTED",
        stats["shortlisted"],
        "Above threshold",
    )

with col4:
    st.metric(
        "AVERAGE SCORE",
        f"{stats['average']:.1f}%",
        "Across screenings",
    )


# ============================================================
# ANALYTICS
# ============================================================

st.divider()

st.caption("SCREENING ANALYTICS")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "SHORTLIST RATE",
        f"{stats['shortlist_rate']:.1f}%",
    )

    st.caption(
        f"{stats['shortlisted']} shortlisted out of "
        f"{stats['candidates']} screened"
    )

with col2:

    st.metric(
        "AVERAGE CANDIDATE SCORE",
        f"{stats['average']:.2f}%",
    )

    st.caption("AI-generated composite score")


# ============================================================
# RECENT SESSIONS
# ============================================================

st.divider()

st.caption("RECENT SESSIONS")

st.subheader("Screening History")

if not history:

    st.info("No previous screening sessions found.")

else:

    for index, session in enumerate(history[:8]):

        if not isinstance(session, dict):
            continue

        session_id = (
            session.get("session_id")
            or session.get("id")
            or index + 1
        )

        count = session_candidate_count(session)

        shortlisted = session_shortlisted_count(session)

        average = session_average_score(session)

        st.write(
            f"**#{session_id}**  "
            f"`{count} candidates` • "
            f"`{shortlisted} shortlisted` • "
            f"`avg {average:.2f}%`"
        )


# ============================================================
# SCREEN CANDIDATES
# ============================================================

st.divider()

st.caption("SCREEN CANDIDATES")

st.header("Upload resumes and job description")

st.write(
    "Upload candidate resumes and one job description to run "
    "the complete AI screening pipeline."
)

resume_files = st.file_uploader(
    "Candidate Resumes",
    type=["pdf"],
    accept_multiple_files=True,
    key="resume_uploader",
)

jd_file = st.file_uploader(
    "Job Description",
    type=["txt", "pdf"],
    accept_multiple_files=False,
    key="jd_uploader",
)


# ============================================================
# UPLOAD STATUS
# ============================================================

if resume_files:

    st.success(
        f"✓ {len(resume_files)} resumes ready"
    )

    with st.expander(
        "View uploaded resumes",
        expanded=False,
    ):

        for resume in resume_files:

            size_kb = len(resume.getvalue()) / 1024

            st.write(
                f"📄 **{resume.name}** — "
                f"{size_kb:.1f} KB"
            )


if jd_file:

    st.success(
        f"✓ {jd_file.name} loaded"
    )


# ============================================================
# RUN BUTTON
# ============================================================

run_screening = st.button(
    "✦ RUN AI SCREENING",
    type="primary",
    use_container_width=True,
)


if run_screening:

    if not resume_files:

        st.error(
            "Please upload at least one resume PDF."
        )

    elif not jd_file:

        st.error(
            "Please upload one job description."
        )

    else:

        files = []

        for resume in resume_files:

            files.append(
                (
                    "resumes",
                    (
                        resume.name,
                        resume.getvalue(),
                        "application/pdf",
                    ),
                )
            )

        if jd_file.name.lower().endswith(".txt"):
            content_type = "text/plain"
        else:
            content_type = "application/pdf"

        files.append(
            (
                "job_description",
                (
                    jd_file.name,
                    jd_file.getvalue(),
                    content_type,
                ),
            )
        )

        try:

            with st.spinner(
                "AI engine is analyzing candidates..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/rank",
                    files=files,
                    timeout=180,
                )

            if response.status_code != 200:

                st.error(
                    f"Backend returned HTTP "
                    f"{response.status_code}"
                )

                try:

                    st.json(
                        response.json()
                    )

                except Exception:

                    st.code(
                        response.text
                    )

            else:

                data = response.json()

                st.session_state[
                    "screening_results"
                ] = data

                st.success(
                    "AI screening completed successfully."
                )

        except requests.RequestException as error:

            st.error(
                "Could not connect to the FastAPI backend."
            )

            st.code(str(error))


# ============================================================
# RESULTS
# ============================================================

results = st.session_state.get(
    "screening_results"
)


if results:

    candidates = (
        results.get("candidates")
        or results.get("results")
        or []
    )

    if not isinstance(candidates, list):
        candidates = []

    # Sort by rank
    candidates = sorted(
        candidates,
        key=lambda x: safe_int(
            x.get("rank", 9999),
            9999,
        ),
    )

    total_candidates = len(candidates)

    shortlisted_candidates = [
        candidate
        for candidate in candidates
        if str(
            candidate.get("status", "")
        ).upper() == "SHORTLISTED"
    ]

    total_shortlisted = len(
        shortlisted_candidates
    )

    result_scores = [
        safe_float(candidate.get("score"))
        for candidate in candidates
        if candidate.get("score") is not None
    ]

    average_result_score = (
        sum(result_scores) / len(result_scores)
        if result_scores
        else 0
    )

    result_shortlist_rate = (
        total_shortlisted /
        total_candidates *
        100
        if total_candidates
        else 0
    )

    # ========================================================
    # RESULT HEADER
    # ========================================================

    st.divider()

    st.caption("SCREENING RESULTS")

    st.header("AI Candidate Ranking")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "CANDIDATES",
            total_candidates,
            "Resumes analyzed",
        )

    with col2:

        st.metric(
            "SHORTLISTED",
            total_shortlisted,
            "Candidates above threshold",
        )

    with col3:

        st.metric(
            "SHORTLIST RATE",
            f"{result_shortlist_rate:.1f}%",
            "Current screening run",
        )

    st.caption(
        f"Average candidate score: "
        f"{average_result_score:.2f}%"
    )

    # ========================================================
    # CANDIDATE CARDS
    # ========================================================

    for candidate in candidates:

        name = (
            candidate.get("candidate_name")
            or candidate.get("filename")
            or "Unknown Candidate"
        )

        rank = candidate.get("rank", "-")

        score = safe_float(
            candidate.get("score")
        )

        status = str(
            candidate.get(
                "status",
                "NOT SHORTLISTED",
            )
        ).upper()

        scores = get_scores(candidate)

        st.divider()

        # Candidate title
        col1, col2 = st.columns([3, 1])

        with col1:

            st.caption(
                f"RANK #{rank}"
            )

            st.subheader(
                str(name)
            )

            if status == "SHORTLISTED":

                st.success(
                    "● SHORTLISTED"
                )

            else:

                st.error(
                    "● NOT SHORTLISTED"
                )

        with col2:

            st.metric(
                "AI SCORE",
                f"{score:.2f}%",
            )

        st.progress(
            max(
                0.0,
                min(100.0, score)
            ) / 100
        )

        # ====================================================
        # SCORE BREAKDOWN
        # ====================================================

        st.markdown("#### Score Breakdown")

        score_columns = st.columns(6)

        breakdown = [
            ("Skills", scores["skills"]),
            ("Education", scores["education"]),
            ("Role", scores["role"]),
            ("Projects", scores["projects"]),
            ("TF-IDF", scores["tfidf"]),
            ("Semantic", scores["semantic"]),
        ]

        for column, item in zip(
            score_columns,
            breakdown,
        ):

            label, value = item

            with column:

                st.metric(
                    label,
                    f"{value:.2f}%",
                )

        # ====================================================
        # ANALYSIS
        # ====================================================

        with st.expander(
            "View Candidate Analysis",
            expanded=False,
        ):

            skills = get_skill_data(
                candidate
            )

            education = candidate.get(
                "education"
            )

            role = candidate.get(
                "role"
            )

            experience = candidate.get(
                "experience"
            )

            projects = candidate.get(
                "projects"
            )

            similarity = candidate.get(
                "similarity"
            )

            if not isinstance(
                education,
                dict,
            ):
                education = {}

            if not isinstance(
                role,
                dict,
            ):
                role = {}

            if not isinstance(
                experience,
                dict,
            ):
                experience = {}

            if not isinstance(
                projects,
                dict,
            ):
                projects = {}

            if not isinstance(
                similarity,
                dict,
            ):
                similarity = {}

            # =================================================
            # TABS
            # =================================================

            tab1, tab2, tab3, tab4 = st.tabs(
                [
                    "Skills",
                    "Education & Role",
                    "Projects & Similarity",
                    "AI Explanation",
                ]
            )

            # =================================================
            # SKILLS
            # =================================================

            with tab1:

                st.subheader(
                    "Skill Intelligence"
                )

                st.markdown(
                    "#### Matched Required"
                )

                if skills[
                    "matched_required"
                ]:

                    for skill in skills[
                        "matched_required"
                    ]:

                        st.write(
                            f"✅ `{skill}`"
                        )

                else:

                    st.caption(
                        "No required skills matched."
                    )

                st.markdown(
                    "#### Missing Required"
                )

                if skills[
                    "missing_required"
                ]:

                    for skill in skills[
                        "missing_required"
                    ]:

                        st.write(
                            f"❌ `{skill}`"
                        )

                else:

                    st.success(
                        "All required skills matched."
                    )

                st.divider()

                st.markdown(
                    "#### Matched Preferred"
                )

                if skills[
                    "matched_preferred"
                ]:

                    for skill in skills[
                        "matched_preferred"
                    ]:

                        st.write(
                            f"🟣 `{skill}`"
                        )

                else:

                    st.caption(
                        "No preferred skills matched."
                    )

                st.markdown(
                    "#### Missing Preferred"
                )

                if skills[
                    "missing_preferred"
                ]:

                    for skill in skills[
                        "missing_preferred"
                    ]:

                        st.write(
                            f"⚪ `{skill}`"
                        )

                else:

                    st.caption(
                        "No preferred skills missing."
                    )

                st.divider()

                st.subheader(
                    "Overall Skill Score"
                )

                st.metric(
                    "Skill Match",
                    f"{scores['skills']:.2f}%",
                )

                st.progress(
                    max(
                        0,
                        min(
                            100,
                            scores["skills"]
                        )
                    ) / 100
                )

            # =================================================
            # EDUCATION + ROLE
            # =================================================

            with tab2:

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader(
                        "Education"
                    )

                    education_satisfied = (
                        education.get(
                            "satisfied"
                        )
                    )

                    if education_satisfied is True:

                        st.success(
                            "Education requirement satisfied."
                        )

                    elif education_satisfied is False:

                        st.warning(
                            "Education requirement not satisfied."
                        )

                    else:

                        st.info(
                            "Education requirement evaluated."
                        )

                    degree = (
                        education.get("degree")
                        or education.get(
                            "highest_degree"
                        )
                    )

                    field = (
                        education.get("field")
                        or education.get(
                            "degree_field"
                        )
                        or education.get(
                            "major"
                        )
                    )

                    if degree:

                        st.write(
                            f"**Degree:** {degree}"
                        )

                    if field:

                        st.write(
                            f"**Field:** {field}"
                        )

                    st.metric(
                        "Education Score",
                        f"{scores['education']:.2f}%",
                    )

                with col2:

                    st.subheader(
                        "Role Intelligence"
                    )

                    candidate_role = (
                        role.get(
                            "candidate_role"
                        )
                        or role.get(
                            "detected_role"
                        )
                        or role.get(
                            "role"
                        )
                    )

                    target_role = (
                        role.get(
                            "target_role"
                        )
                        or role.get(
                            "required_role"
                        )
                    )

                    if candidate_role:

                        st.write(
                            f"**Candidate Role:** "
                            f"{candidate_role}"
                        )

                    if target_role:

                        st.write(
                            f"**Target Role:** "
                            f"{target_role}"
                        )

                    st.metric(
                        "Role Relevance",
                        f"{scores['role']:.2f}%",
                    )

                st.divider()

                st.subheader(
                    "Experience"
                )

                years = (
                    experience.get(
                        "years"
                    )
                    or experience.get(
                        "years_of_experience"
                    )
                    or experience.get(
                        "candidate_years"
                    )
                )

                required_years = (
                    experience.get(
                        "required_years"
                    )
                    or experience.get(
                        "minimum_years"
                    )
                )

                if years is not None:

                    st.write(
                        f"**Candidate Experience:** "
                        f"{safe_float(years):g} years"
                    )

                if required_years is not None:

                    st.write(
                        f"**Required Experience:** "
                        f"{safe_float(required_years):g} years"
                    )

                if (
                    years is None
                    and required_years is None
                ):

                    st.caption(
                        "No explicit experience requirement was specified."
                    )

                st.metric(
                    "Experience Score",
                    f"{scores['experience']:.2f}%",
                )

            # =================================================
            # PROJECTS + SIMILARITY
            # =================================================

            with tab3:

                st.subheader(
                    "Project Analysis"
                )

                total_projects = (
                    projects.get("total")
                    or projects.get(
                        "total_projects"
                    )
                    or projects.get(
                        "count"
                    )
                    or 0
                )

                relevant_projects = (
                    projects.get("relevant")
                    or projects.get(
                        "relevant_projects"
                    )
                    or projects.get(
                        "relevant_count"
                    )
                    or 0
                )

                st.write(
                    f"**Total Projects:** "
                    f"{total_projects}"
                )

                st.write(
                    f"**Relevant Projects:** "
                    f"{relevant_projects}"
                )

                best_skill_overlap = (
                    projects.get(
                        "best_skill_overlap"
                    )
                )

                if best_skill_overlap is not None:

                    st.write(
                        f"**Best Skill Overlap:** "
                        f"{safe_float(best_skill_overlap):.2f}"
                    )

                best_keyword_overlap = (
                    projects.get(
                        "best_keyword_overlap"
                    )
                )

                if best_keyword_overlap is not None:

                    st.write(
                        f"**Best Keyword Overlap:** "
                        f"{safe_float(best_keyword_overlap):.2f}"
                    )

                category_score = (
                    projects.get(
                        "category_score"
                    )
                )

                if category_score is not None:

                    st.write(
                        f"**Category Score:** "
                        f"{safe_float(category_score):.2f}%"
                    )

                st.metric(
                    "Project Score",
                    f"{scores['projects']:.2f}%",
                )

                st.divider()

                st.subheader(
                    "Similarity Analysis"
                )

                tfidf = (
                    similarity.get(
                        "tfidf_score"
                    )
                    if similarity.get(
                        "tfidf_score"
                    ) is not None
                    else scores["tfidf"]
                )

                semantic = (
                    similarity.get(
                        "semantic_score"
                    )
                    if similarity.get(
                        "semantic_score"
                    ) is not None
                    else scores["semantic"]
                )

                st.metric(
                    "TF-IDF Similarity",
                    f"{safe_float(tfidf):.2f}%",
                )

                st.progress(
                    max(
                        0,
                        min(
                            100,
                            safe_float(tfidf)
                        )
                    ) / 100
                )

                st.metric(
                    "Semantic Similarity",
                    f"{safe_float(semantic):.2f}%",
                )

                st.progress(
                    max(
                        0,
                        min(
                            100,
                            safe_float(semantic)
                        )
                    ) / 100
                )

                st.caption(
                    "TF-IDF measures textual similarity. "
                    "Semantic similarity measures contextual similarity."
                )

            # =================================================
            # EXPLANATION
            # =================================================

            with tab4:

                st.subheader(
                    "AI Explanation"
                )

                explanation = candidate.get(
                    "explanation"
                )

                if isinstance(
                    explanation,
                    list,
                ):

                    for item in explanation:

                        st.write(
                            f"• {item}"
                        )

                elif isinstance(
                    explanation,
                    dict,
                ):

                    for key, value in explanation.items():

                        readable_key = (
                            str(key)
                            .replace(
                                "_",
                                " ",
                            )
                            .title()
                        )

                        st.markdown(
                            f"**{readable_key}**"
                        )

                        if isinstance(
                            value,
                            list,
                        ):

                            for item in value:

                                st.write(
                                    f"• {item}"
                                )

                        else:

                            st.write(
                                str(value)
                            )

                elif explanation:

                    st.write(
                        str(explanation)
                    )

                else:

                    # Fallback explanation
                    if scores["skills"] >= 80:

                        st.success(
                            "Strong alignment with the required technical skills."
                        )

                    elif scores["skills"] >= 60:

                        st.info(
                            "Moderate alignment with the required technical skills."
                        )

                    else:

                        st.warning(
                            "Several required technical skills are missing."
                        )

                    if scores["education"] >= 80:

                        st.write(
                            "Education requirements are substantially satisfied."
                        )

                    if scores["role"] >= 80:

                        st.write(
                            "The candidate role is strongly aligned "
                            "with the target role."
                        )

                    elif scores["role"] < 50:

                        st.write(
                            "The candidate role has limited alignment "
                            "with the target role."
                        )

                    if scores["projects"] >= 50:

                        st.write(
                            "Projects show meaningful relevance "
                            "to the target position."
                        )

                    else:

                        st.write(
                            "Project relevance to the target position "
                            "is limited."
                        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ResumeAI v1.0.0 • AI-Based Resume Screening & Candidate Shortlisting System"
)