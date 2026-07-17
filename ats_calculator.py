import re

from skill_matcher import extract_skills


IMPORTANT_SECTIONS = {
    "education": [
        "education",
        "academic qualification",
        "academic qualifications"
    ],
    "skills": [
        "skills",
        "technical skills",
        "core skills"
    ],
    "projects": [
        "projects",
        "academic projects",
        "personal projects"
    ],
    "experience": [
        "experience",
        "internship",
        "internships",
        "work experience"
    ],
    "certifications": [
        "certifications",
        "certificates",
        "licenses and certifications"
    ]
}


ACTION_VERBS = [
    "developed",
    "built",
    "implemented",
    "designed",
    "created",
    "deployed",
    "integrated",
    "improved",
    "analyzed",
    "trained",
    "achieved",
    "optimized",
    "automated",
    "managed",
    "collaborated"
]


def calculate_keyword_score(job_description, resume_text):
    """
    Calculate how many required job skills
    are present in the resume.
    """

    required_skills = extract_skills(job_description)

    resume_skills = extract_skills(resume_text)

    if not required_skills:
        return 0, 0, 0, [], []

    matched_keywords = []

    missing_keywords = []

    for skill in required_skills:
        if skill in resume_skills:
            matched_keywords.append(skill)
        else:
            missing_keywords.append(skill)

    keyword_score = round(
        len(matched_keywords)
        / len(required_skills)
        * 100
    )

    return (
        keyword_score,
        len(matched_keywords),
        len(required_skills),
        matched_keywords,
        missing_keywords
    )


def calculate_section_score(resume_text):
    """
    Check whether important resume sections exist.
    """

    resume_lower = resume_text.lower()

    found_sections = []

    missing_sections = []

    for section_name, aliases in IMPORTANT_SECTIONS.items():
        section_found = False

        for alias in aliases:
            if alias in resume_lower:
                section_found = True
                break

        if section_found:
            found_sections.append(section_name)
        else:
            missing_sections.append(section_name)

    section_score = round(
        len(found_sections)
        / len(IMPORTANT_SECTIONS)
        * 100
    )

    return (
        section_score,
        found_sections,
        missing_sections
    )


def calculate_contact_score(resume_text):
    """
    Check for email, phone number and LinkedIn/GitHub.
    """

    email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"

    phone_pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    resume_lower = resume_text.lower()

    has_email = bool(
        re.search(
            email_pattern,
            resume_text
        )
    )

    has_phone = bool(
        re.search(
            phone_pattern,
            resume_text.replace(" ", "")
        )
    )

    has_linkedin = "linkedin.com" in resume_lower

    has_github = "github.com" in resume_lower

    contact_items = {
        "Email": has_email,
        "Phone number": has_phone,
        "LinkedIn": has_linkedin,
        "GitHub": has_github
    }

    found_contact_items = [
        name
        for name, found in contact_items.items()
        if found
    ]

    missing_contact_items = [
        name
        for name, found in contact_items.items()
        if not found
    ]

    contact_score = round(
        len(found_contact_items)
        / len(contact_items)
        * 100
    )

    return (
        contact_score,
        found_contact_items,
        missing_contact_items
    )


def calculate_achievement_score(resume_text):
    """
    Check whether the resume uses action verbs
    and measurable achievements.
    """

    resume_lower = resume_text.lower()

    found_action_verbs = []

    for verb in ACTION_VERBS:
        if verb in resume_lower:
            found_action_verbs.append(verb)

    number_patterns = [
        r"\b\d+%",
        r"\b\d+\+",
        r"\b\d+\.\d+\b",
        r"\b\d+\s*(users|students|records|samples|projects|badges|weeks|hours)"
    ]

    measurable_results = []

    for pattern in number_patterns:
        matches = re.findall(
            pattern,
            resume_lower
        )

        if matches:
            measurable_results.extend(
                matches
            )

    action_verb_score = min(
        len(found_action_verbs) * 8,
        60
    )

    measurement_score = 40 if measurable_results else 0

    achievement_score = min(
        action_verb_score + measurement_score,
        100
    )

    return (
        achievement_score,
        found_action_verbs,
        measurable_results
    )


def calculate_length_score(resume_text):
    """
    Give a score based on resume word count.
    """

    word_count = len(
        resume_text.split()
    )

    if 300 <= word_count <= 900:
        length_score = 100

    elif 200 <= word_count < 300:
        length_score = 80

    elif 900 < word_count <= 1200:
        length_score = 75

    elif 100 <= word_count < 200:
        length_score = 55

    else:
        length_score = 35

    return (
        length_score,
        word_count
    )


def calculate_ats_score(job_description, resume_text):
    """
    Calculate the final ATS-style resume score.
    """

    (
        keyword_score,
        matched_keyword_count,
        total_keyword_count,
        matched_keywords,
        missing_keywords
    ) = calculate_keyword_score(
        job_description,
        resume_text
    )

    (
        section_score,
        found_sections,
        missing_sections
    ) = calculate_section_score(
        resume_text
    )

    (
        contact_score,
        found_contact_items,
        missing_contact_items
    ) = calculate_contact_score(
        resume_text
    )

    (
        achievement_score,
        found_action_verbs,
        measurable_results
    ) = calculate_achievement_score(
        resume_text
    )

    (
        length_score,
        word_count
    ) = calculate_length_score(
        resume_text
    )

    final_score = round(
        keyword_score * 0.45
        + section_score * 0.20
        + contact_score * 0.15
        + achievement_score * 0.10
        + length_score * 0.10
    )

    return {
        "ats_score": final_score,

        "keyword_score": keyword_score,
        "matched_keyword_count": matched_keyword_count,
        "total_keyword_count": total_keyword_count,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,

        "section_score": section_score,
        "found_sections": found_sections,
        "missing_sections": missing_sections,

        "contact_score": contact_score,
        "found_contact_items": found_contact_items,
        "missing_contact_items": missing_contact_items,

        "achievement_score": achievement_score,
        "found_action_verbs": found_action_verbs,
        "measurable_results": measurable_results,

        "length_score": length_score,
        "word_count": word_count
    }