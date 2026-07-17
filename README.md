# 🚀 NextRole AI

NextRole AI is an AI-powered career opportunity assistant that helps students and job seekers analyze how well their resume matches a job description.

The application extracts resume text, detects relevant skills, estimates an ATS-style score, identifies missing skills, generates personalized career advice and interview questions using Google Gemini, and creates downloadable PDF reports.

---

## ✨ Features

- Upload resumes in PDF, DOCX, or TXT format
- Extract resume text automatically
- Analyze job descriptions
- Detect required, matched, and missing skills
- Calculate job-match percentage
- Estimate ATS-style resume score
- Generate personalized AI career advice
- Generate technical, project, missing-skill, and HR interview questions
- Create downloadable PDF career reports
- Save previous analyses in local history
- Display dashboard cards and visual analysis

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- Google Gen AI SDK
- PyPDF
- python-docx
- ReportLab
- JSON
- HTML and CSS

---

## 📂 Project Structure

```text
NextRole-AI/
│
├── data/
│   └── history.json
│
├── .env
├── .gitignore
├── ai_analyzer.py
├── app.py
├── ats_calculator.py
├── history_manager.py
├── interview_generator.py
├── pdf_report.py
├── requirements.txt
├── resume_parser.py
├── skill_matcher.py
└── README.md