import re


# Each main skill has alternative names that may appear
# in resumes and job descriptions.
SKILL_ALIASES = {
    "python": [
        "python"
    ],

    "java": [
        "java"
    ],

    "c": [
        "c programming",
        "c language"
    ],

    "c++": [
        "c++",
        "cpp"
    ],

    "machine learning": [
        "machine learning",
        "ml"
    ],

    "deep learning": [
        "deep learning",
        "dl"
    ],

    "natural language processing": [
        "natural language processing",
        "nlp"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "ai"
    ],

    "large language models": [
        "large language models",
        "large language model",
        "llms",
        "llm"
    ],

    "generative ai": [
        "generative ai",
        "gen ai",
        "genai"
    ],

    "prompt engineering": [
        "prompt engineering"
    ],

    "git": [
        "git"
    ],

    "github": [
        "github"
    ],

    "streamlit": [
        "streamlit"
    ],

    "fastapi": [
        "fastapi",
        "fast api"
    ],

    "flask": [
        "flask"
    ],

    "docker": [
        "docker",
        "containerization",
        "containers"
    ],

    "kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "google cloud platform": [
        "google cloud platform",
        "google cloud",
        "gcp"
    ],

    "amazon web services": [
        "amazon web services",
        "aws"
    ],

    "microsoft azure": [
        "microsoft azure",
        "azure"
    ],

    "rest api": [
        "rest api",
        "rest APIs",
        "restful api",
        "restful APIs"
    ],

    "sql": [
        "sql"
    ],

    "mysql": [
        "mysql"
    ],

    "postgresql": [
        "postgresql",
        "postgres"
    ],

    "mongodb": [
        "mongodb"
    ],

    "pandas": [
        "pandas"
    ],

    "numpy": [
        "numpy"
    ],

    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],

    "tensorflow": [
        "tensorflow"
    ],

    "pytorch": [
        "pytorch"
    ],

    "matplotlib": [
        "matplotlib"
    ],

    "data analysis": [
        "data analysis",
        "data analytics"
    ],

    "communication": [
        "communication",
        "communication skills"
    ],

    "problem solving": [
        "problem solving",
        "problem-solving"
    ],

    "teamwork": [
        "teamwork",
        "team collaboration",
        "collaboration"
    ]
}


def contains_alias(text, alias):
    """
    Check whether a skill alias exists as a complete word or phrase.

    This prevents short aliases such as AI, ML or Git from matching
    accidentally inside unrelated words.
    """

    pattern = rf"(?<!\w){re.escape(alias.lower())}(?!\w)"

    return re.search(
        pattern,
        text.lower()
    ) is not None


def extract_skills(text):
    """
    Extract recognized skills from resume text,
    manually entered skills or a job description.
    """

    if not text:
        return []

    found_skills = []

    for main_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if contains_alias(text, alias):
                found_skills.append(main_skill)
                break

    return found_skills


def analyze_skills(job_description, candidate_profile):
    """
    Compare skills required by a job with the skills
    found in the candidate's resume or manual input.
    """

    required_skills = extract_skills(
        job_description
    )

    candidate_skills = extract_skills(
        candidate_profile
    )

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill in candidate_skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    if not required_skills:
        match_score = 0

    else:
        match_score = round(
            len(matched_skills)
            / len(required_skills)
            * 100
        )

    return (
        match_score,
        required_skills,
        matched_skills,
        missing_skills
    )