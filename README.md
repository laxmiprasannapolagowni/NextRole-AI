# 🚀 NextRole AI

An AI-powered career opportunity assistant that helps students and job seekers evaluate how well their resumes match job descriptions.

NextRole AI analyzes resumes, estimates an ATS-style score, identifies missing skills, generates AI-powered career guidance and interview questions using Google Gemini, and creates downloadable PDF reports.

---

## 🌐 Live Demo

🔗 https://nextrole-ai.streamlit.app/

---

## ✨ Features

- 📄 Upload resumes in PDF, DOCX, or TXT format
- 🤖 AI-powered resume analysis using Google Gemini
- 🎯 Job-match percentage calculation
- 📊 ATS-style resume score estimation
- ✅ Skill matching and missing skill detection
- 💡 Personalized career advice
- 🎤 Technical, HR, and project-based interview questions
- 📑 Downloadable PDF reports
- 🕒 Analysis history
- 📈 Interactive dashboard

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
- HTML & CSS

---

## 📂 Project Structure

```text
NextRole-AI/
│
├── data/
│   └── history.json
├── ai_analyzer.py
├── app.py
├── ats_calculator.py
├── history_manager.py
├── interview_generator.py
├── pdf_report.py
├── resume_parser.py
├── skill_matcher.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Installation

```bash
git clone https://github.com/laxmiprasannapolagowni/NextRole-AI.git

cd NextRole-AI

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

---

## 🔑 Environment Variables

Create a `.env` file and add:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## 👩‍💻 Author

**Polagowni Laxmiprasanna**

- GitHub: https://github.com/laxmiprasannapolagowni
- LinkedIn: https://www.linkedin.com/in/laxmiprasannapolagowni/

---

## ⭐ If you like this project

Please consider giving it a ⭐ on GitHub.
