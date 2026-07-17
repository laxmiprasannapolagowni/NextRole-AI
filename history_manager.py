import json
from datetime import datetime
from pathlib import Path


HISTORY_FILE = Path("data/history.json")


def ensure_history_file():
    """
    Ensure that the data folder and history.json file exist.
    """

    HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text(
            "[]",
            encoding="utf-8"
        )


def load_history():
    """
    Read all saved analysis records from history.json.
    """

    ensure_history_file()

    try:
        with HISTORY_FILE.open(
            "r",
            encoding="utf-8"
        ) as file:
            history = json.load(file)

            if isinstance(history, list):
                return history

            return []

    except (
        json.JSONDecodeError,
        OSError
    ):
        return []


def save_analysis(
    job_title,
    match_score,
    ats_score,
    required_skills,
    matched_skills,
    missing_skills,
    ai_advice,
    interview_questions
):
    """
    Save one job analysis record to history.json.
    """

    history = load_history()

    current_time = datetime.now()

    record = {
        "id": current_time.strftime(
            "%Y%m%d%H%M%S%f"
        ),
        "created_at": current_time.strftime(
            "%d-%m-%Y %I:%M %p"
        ),
        "job_title": job_title.strip(),
        "match_score": match_score,
        "ats_score": ats_score,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "ai_advice": ai_advice,
        "interview_questions": interview_questions
    }

    history.insert(
        0,
        record
    )

    with HISTORY_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )

    return record


def clear_history():
    """
    Remove all saved records from history.json.
    """

    ensure_history_file()

    with HISTORY_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            [],
            file,
            indent=4,
            ensure_ascii=False
        )


def get_analysis_by_id(record_id):
    """
    Return one saved analysis using its unique ID.
    """

    history = load_history()

    for record in history:
        if record.get("id") == record_id:
            return record

    return None