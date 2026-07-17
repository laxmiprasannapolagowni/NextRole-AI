from ai_analyzer import client, find_working_model


def generate_interview_questions(
    job_description,
    candidate_profile,
    missing_skills
):
    """
    Generate technical, project and HR interview questions.
    """

    model_name = find_working_model()

    missing_skills_text = ", ".join(
        missing_skills
    ) if missing_skills else "None"

    prompt = f"""
You are an experienced technical interviewer.

Create interview questions for this candidate.

Job Description:
{job_description}

Candidate Profile:
{candidate_profile}

Missing Skills:
{missing_skills_text}

Give the response using exactly these sections:

## Technical Questions
Generate 5 technical questions relevant to the job.

## Project Questions
Generate 3 questions based on the candidate's projects and skills.

## Missing-Skill Questions
Generate 3 beginner-friendly questions about the missing skills.

## HR Questions
Generate 4 common HR or behavioral questions.

## Preparation Tips
Give concise preparation advice for this interview.

Keep the questions practical, clear and suitable for an intern or fresher.
"""

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty interview response."
        )

    return response.text
