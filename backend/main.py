import os
import sys
import tempfile
from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SRC_DIR = os.path.join(
    BASE_DIR,
    "src"
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)


# ============================================================
# PYTHON PATH
# ============================================================

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

if DATABASE_DIR not in sys.path:
    sys.path.insert(0, DATABASE_DIR)


# ============================================================
# PROJECT IMPORTS
# ============================================================

from screening_engine import (
    screen_candidate,
    DEFAULT_WEIGHTS,
)

from candidate_features import (
    extract_pdf_text,
)

from semantic_similarity import (
    load_semantic_model,
)

from database import (
    get_connection,
    initialize_database,
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

initialize_database()


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Resume Screening System",
    version="1.0.0",
    description=(
        "Backend API for AI-based resume screening, "
        "candidate scoring, ranking, shortlisting, "
        "screening history, and explainable results."
    ),
)


# ============================================================
# CUSTOM OPENAPI
# ============================================================

def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    schemas = (
        openapi_schema
        .get("components", {})
        .get("schemas", {})
    )

    # --------------------------------------------------------
    # /rank schema
    # --------------------------------------------------------

    rank_schema = schemas.get(
        "Body_rank_resumes_rank_post"
    )

    if rank_schema:

        properties = rank_schema.get(
            "properties",
            {}
        )

        if "resumes" in properties:

            properties["resumes"] = {
                "type": "array",
                "items": {
                    "type": "string",
                    "format": "binary",
                },
                "title": "Resumes",
                "description": (
                    "Upload multiple resume PDF files."
                ),
            }

        if "job_description" in properties:

            properties["job_description"] = {
                "type": "string",
                "format": "binary",
                "title": "Job Description",
                "description": (
                    "Upload one job description TXT file."
                ),
            }

    # --------------------------------------------------------
    # /screen schema
    # --------------------------------------------------------

    screen_schema = schemas.get(
        "Body_screen_resume_screen_post"
    )

    if screen_schema:

        properties = screen_schema.get(
            "properties",
            {}
        )

        if "resume" in properties:

            properties["resume"] = {
                "type": "string",
                "format": "binary",
                "title": "Resume",
                "description": (
                    "Upload one resume PDF."
                ),
            }

        if "job_description" in properties:

            properties["job_description"] = {
                "type": "string",
                "format": "binary",
                "title": "Job Description",
                "description": (
                    "Upload one job description TXT file."
                ),
            }

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi


# ============================================================
# RESULT CLEANING
# ============================================================

def build_clean_result(result):
    """
    Convert internal screening-engine output into a clean,
    frontend-friendly API response.

    The scoring algorithm itself is not modified here.
    """

    features = result.get(
        "features",
        {}
    )

    score_details = result.get(
        "score_details",
        {}
    )

    skills = features.get(
        "skills",
        {}
    )

    experience = features.get(
        "experience",
        {}
    )

    education = features.get(
        "education",
        {}
    )

    role = features.get(
        "role",
        {}
    )

    projects = features.get(
        "projects",
        {}
    )

    similarity = features.get(
        "similarity",
        {}
    )

    feature_scores = score_details.get(
        "feature_scores",
        {}
    )

    contributions = score_details.get(
        "contributions",
        {}
    )

    used_weights = score_details.get(
        "used_weights",
        {}
    )

    return {

        # ----------------------------------------------------
        # BASIC INFORMATION
        # ----------------------------------------------------

        "candidate_name": result.get(
            "candidate_name"
        ),

        "score": result.get(
            "score"
        ),

        "status": result.get(
            "status"
        ),

        # ----------------------------------------------------
        # SCORE BREAKDOWN
        # ----------------------------------------------------

        "scores": {

            "skills": feature_scores.get(
                "skills"
            ),

            "experience": feature_scores.get(
                "experience"
            ),

            "education": feature_scores.get(
                "education"
            ),

            "role": feature_scores.get(
                "role"
            ),

            "projects": feature_scores.get(
                "projects"
            ),

            "tfidf": feature_scores.get(
                "tfidf"
            ),

            "semantic": feature_scores.get(
                "semantic"
            ),
        },

        # ----------------------------------------------------
        # SCORE CONTRIBUTIONS
        # ----------------------------------------------------

        "contributions": {

            "skills": contributions.get(
                "skills"
            ),

            "experience": contributions.get(
                "experience"
            ),

            "education": contributions.get(
                "education"
            ),

            "role": contributions.get(
                "role"
            ),

            "projects": contributions.get(
                "projects"
            ),

            "tfidf": contributions.get(
                "tfidf"
            ),

            "semantic": contributions.get(
                "semantic"
            ),
        },

        # ----------------------------------------------------
        # WEIGHTS
        # ----------------------------------------------------

        "used_weights": {

            "skills": used_weights.get(
                "skills"
            ),

            "experience": used_weights.get(
                "experience"
            ),

            "education": used_weights.get(
                "education"
            ),

            "role": used_weights.get(
                "role"
            ),

            "projects": used_weights.get(
                "projects"
            ),

            "tfidf": used_weights.get(
                "tfidf"
            ),

            "semantic": used_weights.get(
                "semantic"
            ),
        },

        # ----------------------------------------------------
        # SKILLS
        # ----------------------------------------------------

        "skills": {

            "matched_required": skills.get(
                "matched_required",
                []
            ),

            "missing_required": skills.get(
                "missing_required",
                []
            ),

            "matched_preferred": skills.get(
                "matched_preferred",
                []
            ),

            "missing_preferred": skills.get(
                "missing_preferred",
                []
            ),

            "overall_score": skills.get(
                "overall_score"
            ),
        },

        # ----------------------------------------------------
        # EDUCATION
        # ----------------------------------------------------

        "education": {

            "score": education.get(
                "score"
            ),

            "status": education.get(
                "status"
            ),

            "degree_match": education.get(
                "degree_match",
                {}
            ),

            "field_match": education.get(
                "field_match",
                {}
            ),
        },

        # ----------------------------------------------------
        # EXPERIENCE
        # ----------------------------------------------------

        "experience": {

            "score": experience.get(
                "score"
            ),

            "status": experience.get(
                "status"
            ),

            "candidate_years": experience.get(
                "candidate_years"
            ),

            "required_years": experience.get(
                "required_years"
            ),
        },

        # ----------------------------------------------------
        # ROLE
        # ----------------------------------------------------

        "role": {

            "candidate_role": role.get(
                "candidate_primary_role"
            ),

            "job_role": role.get(
                "job_primary_role"
            ),

            "score": role.get(
                "score"
            ),
        },

        # ----------------------------------------------------
        # PROJECTS
        # ----------------------------------------------------

        "projects": {

            "project_count": projects.get(
                "project_count",
                0
            ),

            "relevant_project_count": projects.get(
                "relevant_project_count",
                0
            ),

            "score": projects.get(
                "score"
            ),

            "best_skill_overlap": projects.get(
                "best_skill_overlap"
            ),

            "best_keyword_overlap": projects.get(
                "best_keyword_overlap"
            ),

            "best_category_match": projects.get(
                "best_category_match"
            ),
        },

        # ----------------------------------------------------
        # TEXT SIMILARITY
        # ----------------------------------------------------

        "similarity": {

            "tfidf_score": similarity.get(
                "tfidf_score"
            ),

            "semantic_score": similarity.get(
                "semantic_score"
            ),
        },

        # ----------------------------------------------------
        # EXPLANATION
        # ----------------------------------------------------

        "explanation": result.get(
            "explanation",
            []
        ),
    }


# ============================================================
# DATABASE SAVE
# ============================================================

def save_screening_session(
    job_description,
    candidates,
):
    """
    Save one complete screening session and its candidates.

    Returns:
        session_id on success
        None on database failure
    """

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        # ----------------------------------------------------
        # Calculate session statistics
        # ----------------------------------------------------

        total_candidates = len(
            candidates
        )

        shortlisted = sum(
            1
            for candidate in candidates
            if candidate.get("status")
            == "SHORTLISTED"
        )

        not_shortlisted = sum(
            1
            for candidate in candidates
            if candidate.get("status")
            == "NOT SHORTLISTED"
        )

        scores = [
            candidate.get("score")
            for candidate in candidates
            if isinstance(
                candidate.get("score"),
                (int, float)
            )
        ]

        average_score = (
            sum(scores) / len(scores)
            if scores
            else 0.0
        )

        # ----------------------------------------------------
        # Insert screening session
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO screening_sessions
            (
                job_description,
                total_candidates,
                shortlisted,
                not_shortlisted,
                average_score
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                job_description,
                total_candidates,
                shortlisted,
                not_shortlisted,
                average_score,
            ),
        )

        session_id = cursor.lastrowid

        # ----------------------------------------------------
        # Insert candidates
        # ----------------------------------------------------

        for candidate in candidates:

            scores_data = candidate.get(
                "scores",
                {}
            )

            cursor.execute(
                """
                INSERT INTO candidates
                (
                    session_id,
                    candidate_name,
                    score,
                    status,
                    skills_score,
                    education_score,
                    role_score,
                    project_score,
                    tfidf_score,
                    semantic_score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,

                    candidate.get(
                        "candidate_name"
                    ),

                    candidate.get(
                        "score"
                    ),

                    candidate.get(
                        "status"
                    ),

                    scores_data.get(
                        "skills"
                    ),

                    scores_data.get(
                        "education"
                    ),

                    scores_data.get(
                        "role"
                    ),

                    scores_data.get(
                        "projects"
                    ),

                    scores_data.get(
                        "tfidf"
                    ),

                    scores_data.get(
                        "semantic"
                    ),
                ),
            )

        connection.commit()

        print(
            f"[DATABASE] Screening session "
            f"{session_id} saved successfully."
        )

        return session_id

    except Exception as e:

        if connection:

            try:
                connection.rollback()
            except Exception:
                pass

        print(
            "[DATABASE] Save error:",
            str(e)
        )

        return None

    finally:

        if connection:

            try:
                connection.close()
            except Exception:
                pass


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "status": "success",
        "message": (
            "AI Resume Screening System API is running."
        ),
        "version": app.version,
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# SCREENING HISTORY
# ============================================================

@app.get("/history")
def get_screening_history():
    """
    Return all previous screening sessions.

    Newest sessions are returned first.
    """

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                job_description,
                total_candidates,
                shortlisted,
                not_shortlisted,
                average_score,
                created_at
            FROM screening_sessions
            ORDER BY created_at DESC, id DESC
            """
        )

        rows = cursor.fetchall()

        history = []

        for row in rows:

            history.append({

                "session_id": row["id"],

                "job_description": (
                    row["job_description"]
                ),

                "total_candidates": (
                    row["total_candidates"]
                ),

                "shortlisted": (
                    row["shortlisted"]
                ),

                "not_shortlisted": (
                    row["not_shortlisted"]
                ),

                "average_score": (
                    row["average_score"]
                ),

                "created_at": (
                    row["created_at"]
                ),
            })

        return {

            "status": "success",

            "total_sessions": len(
                history
            ),

            "history": history,
        }

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
            },
        )

    finally:

        if connection:

            try:
                connection.close()
            except Exception:
                pass


# ============================================================
# SINGLE SCREENING SESSION DETAILS
# ============================================================

@app.get("/history/{session_id}")
def get_screening_session(
    session_id: int
):
    """
    Return complete details of one screening session,
    including all candidates belonging to it.
    """

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        # ----------------------------------------------------
        # Get session
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                job_description,
                total_candidates,
                shortlisted,
                not_shortlisted,
                average_score,
                created_at
            FROM screening_sessions
            WHERE id = ?
            """,
            (session_id,),
        )

        session = cursor.fetchone()

        if session is None:

            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": (
                        f"Screening session "
                        f"{session_id} was not found."
                    ),
                },
            )

        # ----------------------------------------------------
        # Get candidates
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                candidate_name,
                score,
                status,
                skills_score,
                education_score,
                role_score,
                project_score,
                tfidf_score,
                semantic_score
            FROM candidates
            WHERE session_id = ?
            ORDER BY score DESC, id ASC
            """,
            (session_id,),
        )

        candidate_rows = cursor.fetchall()

        candidates = []

        for rank, candidate in enumerate(
            candidate_rows,
            start=1,
        ):

            candidates.append({

                "candidate_id": candidate["id"],

                "rank": rank,

                "candidate_name": (
                    candidate["candidate_name"]
                ),

                "score": candidate["score"],

                "status": candidate["status"],

                "scores": {

                    "skills": (
                        candidate["skills_score"]
                    ),

                    "education": (
                        candidate["education_score"]
                    ),

                    "role": (
                        candidate["role_score"]
                    ),

                    "projects": (
                        candidate["project_score"]
                    ),

                    "tfidf": (
                        candidate["tfidf_score"]
                    ),

                    "semantic": (
                        candidate["semantic_score"]
                    ),
                },
            })

        return {

            "status": "success",

            "session": {

                "session_id": session["id"],

                "job_description": (
                    session["job_description"]
                ),

                "total_candidates": (
                    session["total_candidates"]
                ),

                "shortlisted": (
                    session["shortlisted"]
                ),

                "not_shortlisted": (
                    session["not_shortlisted"]
                ),

                "average_score": (
                    session["average_score"]
                ),

                "created_at": (
                    session["created_at"]
                ),
            },

            "candidates": candidates,
        }

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
            },
        )

    finally:

        if connection:

            try:
                connection.close()
            except Exception:
                pass


# ============================================================
# SCREEN ONE RESUME
# ============================================================

@app.post("/screen")
async def screen_resume(

    resume: Annotated[
        UploadFile,
        File(
            description=(
                "Upload one resume PDF"
            )
        ),
    ],

    job_description: Annotated[
        UploadFile,
        File(
            description=(
                "Upload job description TXT file"
            )
        ),
    ],
):

    temp_path = None

    try:

        # ----------------------------------------------------
        # Validate resume
        # ----------------------------------------------------

        if not resume.filename:

            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": (
                        "Resume filename is missing."
                    ),
                },
            )

        if not resume.filename.lower().endswith(
            ".pdf"
        ):

            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": (
                        "Resume must be a PDF file."
                    ),
                },
            )

        # ----------------------------------------------------
        # Validate job description
        # ----------------------------------------------------

        if not job_description.filename:

            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": (
                        "Job description filename is missing."
                    ),
                },
            )

        if not job_description.filename.lower().endswith(
            ".txt"
        ):

            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": (
                        "Job description must be a TXT file."
                    ),
                },
            )

        # ----------------------------------------------------
        # Read uploaded files
        # ----------------------------------------------------

        resume_bytes = await resume.read()

        jd_bytes = await job_description.read()

        if not resume_bytes:

            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": (
                        "Uploaded resume is empty."
                    ),
                },
            )

        if not jd_bytes:

            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": (
                        "Uploaded job description is empty."
                    ),
                },
            )

        # ----------------------------------------------------
        # Decode job description
        # ----------------------------------------------------

        jd_text = jd_bytes.decode(
            "utf-8",
            errors="ignore",
        )

        # ----------------------------------------------------
        # Create temporary PDF
        # ----------------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as temp_file:

            temp_file.write(
                resume_bytes
            )

            temp_path = temp_file.name

        # ----------------------------------------------------
        # Extract resume text
        # ----------------------------------------------------

        resume_text = extract_pdf_text(
            temp_path
        )

        if not resume_text.strip():

            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": (
                        "No readable text was found "
                        "in the uploaded resume."
                    ),
                },
            )

        # ----------------------------------------------------
        # Load semantic model
        # ----------------------------------------------------

        semantic_model = load_semantic_model()

        # ----------------------------------------------------
        # Screen candidate
        # ----------------------------------------------------

        result = screen_candidate(

            candidate_name=resume.filename,

            candidate_text=resume_text,

            jd_text=jd_text,

            semantic_model=semantic_model,

            weights=DEFAULT_WEIGHTS,

            threshold=60.0,
        )

        # ----------------------------------------------------
        # Clean result
        # ----------------------------------------------------

        clean_result = build_clean_result(
            result
        )

        # ----------------------------------------------------
        # Save to database
        # ----------------------------------------------------

        session_id = save_screening_session(

            job_description=(
                job_description.filename
            ),

            candidates=[
                clean_result
            ],
        )

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return {

            "status": "success",

            "session_id": session_id,

            "result": clean_result,
        }

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
            },
        )

    finally:

        if (
            temp_path
            and os.path.exists(temp_path)
        ):

            try:
                os.remove(temp_path)
            except Exception:
                pass


# ============================================================
# RANK MULTIPLE RESUMES
# ============================================================

@app.post("/rank")
async def rank_resumes(

    resumes: Annotated[
        list[UploadFile],
        File(
            description=(
                "Upload multiple resume PDF files."
            )
        ),
    ],

    job_description: Annotated[
        UploadFile,
        File(
            description=(
                "Upload one job description TXT file."
            )
        ),
    ],
):

    temp_paths = []

    candidates = []

    skipped_files = []

    try:

        # ----------------------------------------------------
        # Validate job description
        # ----------------------------------------------------

        if not job_description.filename:

            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": (
                        "Job description filename is missing."
                    ),
                },
            )

        if not job_description.filename.lower().endswith(
            ".txt"
        ):

            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": (
                        "Job description must be a TXT file."
                    ),
                },
            )

        # ----------------------------------------------------
        # Read job description
        # ----------------------------------------------------

        jd_bytes = await job_description.read()

        if not jd_bytes:

            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": (
                        "Uploaded job description is empty."
                    ),
                },
            )

        jd_text = jd_bytes.decode(
            "utf-8",
            errors="ignore",
        )

        # ----------------------------------------------------
        # Validate resumes
        # ----------------------------------------------------

        if not resumes:

            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": (
                        "Please upload at least "
                        "one resume PDF."
                    ),
                },
            )

        # ----------------------------------------------------
        # Load semantic model ONCE
        # ----------------------------------------------------

        semantic_model = load_semantic_model()

        # ====================================================
        # PROCESS RESUMES
        # ====================================================

        for resume in resumes:

            temp_path = None

            try:

                # ------------------------------------------------
                # Filename
                # ------------------------------------------------

                if not resume.filename:

                    skipped_files.append({
                        "filename": "unknown",
                        "reason": (
                            "Resume filename is missing."
                        ),
                    })

                    continue

                # ------------------------------------------------
                # PDF validation
                # ------------------------------------------------

                if not resume.filename.lower().endswith(
                    ".pdf"
                ):

                    skipped_files.append({
                        "filename": resume.filename,
                        "reason": (
                            "File is not a PDF."
                        ),
                    })

                    continue

                # ------------------------------------------------
                # Read PDF
                # ------------------------------------------------

                resume_bytes = await resume.read()

                if not resume_bytes:

                    skipped_files.append({
                        "filename": resume.filename,
                        "reason": (
                            "File is empty."
                        ),
                    })

                    continue

                # ------------------------------------------------
                # Temporary PDF
                # ------------------------------------------------

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf",
                ) as temp_file:

                    temp_file.write(
                        resume_bytes
                    )

                    temp_path = temp_file.name

                temp_paths.append(
                    temp_path
                )

                # ------------------------------------------------
                # Extract text
                # ------------------------------------------------

                resume_text = extract_pdf_text(
                    temp_path
                )

                if not resume_text.strip():

                    skipped_files.append({
                        "filename": resume.filename,
                        "reason": (
                            "No readable text was found "
                            "in the PDF."
                        ),
                    })

                    continue

                # ------------------------------------------------
                # Screen candidate
                # ------------------------------------------------

                result = screen_candidate(

                    candidate_name=resume.filename,

                    candidate_text=resume_text,

                    jd_text=jd_text,

                    semantic_model=semantic_model,

                    weights=DEFAULT_WEIGHTS,

                    threshold=60.0,
                )

                # ------------------------------------------------
                # Clean result
                # ------------------------------------------------

                clean_result = build_clean_result(
                    result
                )

                candidates.append(
                    clean_result
                )

            except Exception as e:

                skipped_files.append({
                    "filename": resume.filename,
                    "reason": str(e),
                })

            finally:

                if (
                    temp_path
                    and os.path.exists(temp_path)
                ):

                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass

        # ====================================================
        # SORT CANDIDATES
        # ====================================================

        candidates.sort(
            key=lambda candidate: (
                candidate.get("score")
                or 0
            ),
            reverse=True,
        )

        # ====================================================
        # ASSIGN RANK
        # ====================================================

        for rank, candidate in enumerate(
            candidates,
            start=1,
        ):

            candidate["rank"] = rank

        # ====================================================
        # SAVE SESSION
        # ====================================================

        session_id = save_screening_session(

            job_description=(
                job_description.filename
            ),

            candidates=candidates,
        )

        # ====================================================
        # RESPONSE
        # ====================================================

        return {

            "status": "success",

            "message": (
                "Candidates ranked successfully."
            ),

            "session_id": session_id,

            "total_candidates": len(
                candidates
            ),

            "skipped_files": skipped_files,

            "candidates": candidates,
        }

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
            },
        )

    finally:

        for temp_path in temp_paths:

            if os.path.exists(
                temp_path
            ):

                try:
                    os.remove(temp_path)
                except Exception:
                    pass