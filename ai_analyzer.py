import os

from dotenv import load_dotenv
from google import genai


# Load variables from the .env file.
load_dotenv()

# Read the Gemini API key.
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. Check your .env file."
    )

# Create the Gemini client.
client = genai.Client(api_key=api_key)

# Store the working model after finding it once.
_working_model = None


def get_available_model_names():
    """
    Return Gemini model names available for this API key.
    """

    model_names = []

    for model in client.models.list():
        model_name = str(model.name).replace("models/", "")

        # Keep only Gemini text-generation models.
        if "gemini" in model_name.lower():
            model_names.append(model_name)

    return model_names


def find_working_model():
    """
    Test available Gemini models and return the first working one.
    """

    global _working_model

    # Reuse the model after finding it successfully.
    if _working_model:
        return _working_model

    available_models = get_available_model_names()

    if not available_models:
        raise RuntimeError(
            "No Gemini models are available for this API key."
        )

    errors = []

    for model_name in available_models:
        try:
            test_response = client.models.generate_content(
                model=model_name,
                contents="Reply with only the word: READY"
            )

            if test_response.text:
                _working_model = model_name
                return model_name

        except Exception as error:
            errors.append(
                f"{model_name}: {str(error)}"
            )

            # Continue testing the remaining models.
            continue

    error_details = "\n\n".join(errors[:5])

    raise RuntimeError(
        "None of the available Gemini models worked.\n\n"
        f"First model errors:\n{error_details}"
    )


def get_career_advice(job_description, user_skills):
    """
    Generate personalized career advice using a working Gemini model.
    """

    model_name = find_working_model()

    prompt = f"""
You are an experienced career mentor helping a student evaluate
a job or internship opportunity.

Job Description:
{job_description}

Candidate Skills:
{user_skills}

Provide the answer using these headings:

## Overall Match
Explain whether the candidate should apply.

## Strong Skills
List the candidate's relevant strengths.

## Missing Skills
List important skills the candidate needs to improve.

## Learning Roadmap
Give a practical step-by-step learning plan.

## Resume Improvements
Suggest improvements relevant to this opportunity.

## Interview Preparation
Give five likely interview questions with short preparation tips.

Keep the response clear, practical, concise, and professional.
"""

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text