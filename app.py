import streamlit as st

from ai_analyzer import get_career_advice
from ats_calculator import calculate_ats_score
from history_manager import clear_history, load_history, save_analysis
from interview_generator import generate_interview_questions
from pdf_report import generate_pdf_report
from resume_parser import extract_resume_text
from skill_matcher import analyze_skills


st.set_page_config(
    page_title="NextRole AI",
    page_icon="🚀",
    layout="wide"
)


# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown(
    """
    <style>
        .main-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 0;
        }

        .subtitle {
            font-size: 18px;
            color: #6b7280;
            margin-bottom: 25px;
        }

        .metric-card {
            padding: 20px;
            border-radius: 14px;
            border: 1px solid #d1d5db;
            background-color: #f9fafb;
            text-align: center;
            margin-bottom: 10px;
        }

        .metric-label {
            font-size: 16px;
            color: #6b7280;
            margin-bottom: 8px;
        }

        .metric-value {
            font-size: 32px;
            font-weight: 700;
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="main-title">🚀 NextRole AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    (
        '<div class="subtitle">'
        'AI-powered resume matching, ATS analysis, career guidance, '
        'interview preparation and downloadable reports.'
        '</div>'
    ),
    unsafe_allow_html=True
)

st.divider()


# -------------------------------------------------
# SIDEBAR HISTORY
# -------------------------------------------------

st.sidebar.title("Analysis History")

history = load_history()

if history:
    for record in history[:10]:
        st.sidebar.markdown(
            f"**{record['job_title']}**"
        )

        st.sidebar.caption(
            f"{record['created_at']} | "
            f"Match: {record['match_score']}% | "
            f"ATS: {record['ats_score']}%"
        )

        st.sidebar.divider()

    if st.sidebar.button(
        "Clear History",
        use_container_width=True
    ):
        clear_history()

        st.sidebar.success(
            "History cleared."
        )

        st.rerun()

else:
    st.sidebar.info(
        "No analyses saved yet."
    )


# -------------------------------------------------
# JOB DETAILS
# -------------------------------------------------

st.subheader("1. Job Details")

job_title = st.text_input(
    label="Job title",
    placeholder="AI Engineer Intern"
)

job_description = st.text_area(
    label="Paste the complete job or internship description",
    height=250,
    placeholder=(
        "Example: We are looking for an AI Intern with "
        "Python, Machine Learning, Git, Docker and GCP skills."
    )
)


# -------------------------------------------------
# RESUME UPLOAD
# -------------------------------------------------

st.subheader("2. Upload Your Resume")

uploaded_resume = st.file_uploader(
    label="Upload a PDF, DOCX or TXT resume",
    type=["pdf", "docx", "txt"]
)


resume_text = ""

if uploaded_resume is not None:
    try:
        resume_text = extract_resume_text(
            uploaded_resume
        )

        if resume_text.strip():
            st.success(
                "Resume uploaded and text extracted successfully."
            )

            with st.expander(
                "View extracted resume text"
            ):
                st.text_area(
                    label="Resume text",
                    value=resume_text,
                    height=300,
                    disabled=True
                )

        else:
            st.warning(
                "No readable text was found in the resume."
            )

    except Exception as error:
        st.error(
            "The resume could not be processed."
        )

        st.code(
            str(error)
        )


# -------------------------------------------------
# MANUAL SKILLS
# -------------------------------------------------

st.subheader("3. Enter Skills Manually - Optional")

manual_skills = st.text_input(
    label=(
        "Use this only when you do not upload a resume, "
        "or when you want to add extra skills"
    ),
    placeholder=(
        "Python, Machine Learning, Git, GCP, Streamlit"
    )
)


candidate_profile = (
    resume_text
    + "\n"
    + manual_skills
).strip()


# -------------------------------------------------
# ANALYZE BUTTON
# -------------------------------------------------

analyze_button = st.button(
    label="Analyze Opportunity",
    type="primary",
    use_container_width=True
)


if analyze_button:

    if not job_title.strip():
        st.error(
            "Please enter the job title."
        )

    elif not job_description.strip():
        st.error(
            "Please paste the job description."
        )

    elif not candidate_profile:
        st.error(
            "Please upload your resume or enter your skills."
        )

    else:
        (
            match_score,
            required_skills,
            matched_skills,
            missing_skills
        ) = analyze_skills(
            job_description,
            candidate_profile
        )

        ats_result = calculate_ats_score(
            job_description,
            candidate_profile
        )

        ats_score = ats_result["ats_score"]

        st.success(
            "Analysis completed successfully!"
        )

        st.divider()


        # -----------------------------------------
        # DASHBOARD CARDS
        # -----------------------------------------

        st.subheader("4. Dashboard")

        card1, card2, card3, card4 = st.columns(4)

        with card1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Job Match</div>
                    <div class="metric-value">{match_score}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with card2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">ATS Score</div>
                    <div class="metric-value">{ats_score}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with card3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Matched Skills</div>
                    <div class="metric-value">{len(matched_skills)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with card4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Missing Skills</div>
                    <div class="metric-value">{len(missing_skills)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


        # -----------------------------------------
        # VISUAL ANALYSIS
        # -----------------------------------------

        st.subheader("5. Visual Analysis")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("### Skill Coverage")

            skill_chart_data = {
                "Matched Skills": len(matched_skills),
                "Missing Skills": len(missing_skills)
            }

            st.bar_chart(
                skill_chart_data
            )

        with chart_col2:
            st.markdown("### ATS Breakdown")

            ats_chart_data = {
                "Keywords": ats_result["keyword_score"],
                "Sections": ats_result["section_score"],
                "Contact": ats_result["contact_score"],
                "Achievements": ats_result["achievement_score"],
                "Length": ats_result["length_score"]
            }

            st.bar_chart(
                ats_chart_data
            )


        # -----------------------------------------
        # RECOMMENDATION
        # -----------------------------------------

        st.subheader("6. Application Recommendation")

        if match_score >= 75:
            st.success(
                "Strong match - you should apply."
            )

        elif match_score >= 50:
            st.warning(
                "Moderate match - you can apply, "
                "but improve the missing skills."
            )

        else:
            st.error(
                "Low match - improve the missing skills "
                "before applying."
            )


        # -----------------------------------------
        # SKILLS ANALYSIS
        # -----------------------------------------

        st.subheader("7. Skills Analysis")

        skills_col1, skills_col2, skills_col3 = st.columns(3)

        with skills_col1:
            st.markdown("### Required Skills")

            if required_skills:
                for skill in required_skills:
                    st.write(
                        f"📌 {skill.title()}"
                    )
            else:
                st.info(
                    "No required skills detected."
                )

        with skills_col2:
            st.markdown("### Matching Skills")

            if matched_skills:
                for skill in matched_skills:
                    st.write(
                        f"✅ {skill.title()}"
                    )
            else:
                st.warning(
                    "No matching skills found."
                )

        with skills_col3:
            st.markdown("### Missing Skills")

            if missing_skills:
                for skill in missing_skills:
                    st.write(
                        f"❌ {skill.title()}"
                    )
            else:
                st.success(
                    "No missing skills detected."
                )


        # -----------------------------------------
        # ATS BREAKDOWN
        # -----------------------------------------

        with st.expander(
            "View Detailed ATS Score Breakdown"
        ):
            st.write(
                f"**Keyword Coverage:** "
                f"{ats_result['keyword_score']}%"
            )

            st.write(
                f"**Matched Keywords:** "
                f"{ats_result['matched_keyword_count']}"
                f"/{ats_result['total_keyword_count']}"
            )

            st.write(
                f"**Resume Sections:** "
                f"{ats_result['section_score']}%"
            )

            st.write(
                f"**Contact Information:** "
                f"{ats_result['contact_score']}%"
            )

            st.write(
                f"**Achievement Quality:** "
                f"{ats_result['achievement_score']}%"
            )

            st.write(
                f"**Resume Length:** "
                f"{ats_result['length_score']}%"
            )

            st.write(
                f"**Resume Word Count:** "
                f"{ats_result['word_count']}"
            )


        # -----------------------------------------
        # AI CAREER ADVICE
        # -----------------------------------------

        st.divider()

        st.subheader("8. AI Career Advice")

        ai_advice = ""

        try:
            with st.spinner(
                "Gemini is analyzing your career fit..."
            ):
                ai_advice = get_career_advice(
                    job_description,
                    candidate_profile
                )

            st.markdown(
                ai_advice
            )

        except Exception as error:
            st.error(
                "Gemini analysis could not be completed."
            )

            st.code(
                str(error)
            )


        # -----------------------------------------
        # INTERVIEW QUESTIONS
        # -----------------------------------------

        st.divider()

        st.subheader("9. Personalized Interview Questions")

        interview_questions = ""

        try:
            with st.spinner(
                "Gemini is preparing interview questions..."
            ):
                interview_questions = generate_interview_questions(
                    job_description,
                    candidate_profile,
                    missing_skills
                )

            st.markdown(
                interview_questions
            )

        except Exception as error:
            st.error(
                "Interview questions could not be generated."
            )

            st.code(
                str(error)
            )


        # -----------------------------------------
        # SAVE HISTORY AND PDF
        # -----------------------------------------

        st.divider()

        st.subheader("10. Save and Download")

        if ai_advice and interview_questions:

            try:
                save_analysis(
                    job_title=job_title,
                    match_score=match_score,
                    ats_score=ats_score,
                    required_skills=required_skills,
                    matched_skills=matched_skills,
                    missing_skills=missing_skills,
                    ai_advice=ai_advice,
                    interview_questions=interview_questions
                )

                st.success(
                    "Analysis saved to history."
                )

            except Exception as error:
                st.error(
                    "Analysis history could not be saved."
                )

                st.code(
                    str(error)
                )


            try:
                pdf_bytes = generate_pdf_report(
                    job_description=job_description,
                    match_score=match_score,
                    ats_result=ats_result,
                    required_skills=required_skills,
                    matched_skills=matched_skills,
                    missing_skills=missing_skills,
                    ai_advice=ai_advice,
                    interview_questions=interview_questions
                )

                safe_job_title = (
                    job_title
                    .strip()
                    .replace(" ", "_")
                    .replace("/", "_")
                    .replace("\\", "_")
                )

                st.download_button(
                    label="Download NextRole AI PDF Report",
                    data=pdf_bytes,
                    file_name=(
                        f"{safe_job_title}_NextRole_Report.pdf"
                    ),
                    mime="application/pdf",
                    use_container_width=True
                )

            except Exception as error:
                st.error(
                    "The PDF report could not be generated."
                )

                st.code(
                    str(error)
                )