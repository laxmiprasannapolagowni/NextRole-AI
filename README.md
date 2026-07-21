# 🚀 NextRole AI

<p align="center">
  <b>AI-powered Resume Matcher • ATS Analyzer • Career Guidance • Interview Preparation</b>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?logo=streamlit)
![Google Gemini](https://img.shields.io/badge/Google-Gemini-blue?logo=google)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

# 🌐 Live Demo

🔗 https://nextrole-ai.streamlit.app/

---

# 📖 Overview

NextRole AI is an AI-powered career assistant that helps students and job seekers evaluate how well their resumes match a job description.

The application analyzes resumes, estimates an ATS-style score, identifies missing skills, provides AI-powered career guidance using Google Gemini, generates personalized interview questions, and creates downloadable PDF reports.

---

# ✨ Features

- 📄 Upload Resume (PDF, DOCX, TXT)
- 🎯 ATS Resume Score
- 📊 Job Match Percentage
- ✅ Skill Matching
- ❌ Missing Skill Detection
- 🤖 Google Gemini Career Guidance
- 🎤 Technical, HR & Project Interview Questions
- 📈 Interactive Dashboard
- 📑 Downloadable PDF Report
- 🕒 Analysis History

---

# 📸 Screenshots

## 🏠 Home

<p align="center">
<img src="assets/home.png" width="900">
</p>

---

## 📄 Resume Upload

<p align="center">
<img src="assets/upload.png" width="900">
</p>

---

## 📊 Skills Analysis

<p align="center">
<img src="assets/analysis.png" width="900">
</p>

---

## 📈 Dashboard

<p align="center">
<img src="assets/dashboard.png" width="900">
</p>

---

## 🤖 AI Career Guidance

<p align="center">
<img src="assets/report.png" width="900">
</p>

---

## 🎤 Personalized Interview Questions

<p align="center">
<img src="assets/history.png" width="900">
</p>

---

# 🛠️ Tech Stack

### Programming Language
- Python

### Framework
- Streamlit

### AI
- Google Gemini API

### Libraries
- google-generativeai
- PyPDF2
- python-docx
- pandas
- matplotlib
- ReportLab

### Storage
- JSON

---

# 📂 Project Structure

```text
NextRole-AI/
│
├── assets/
│   ├── home.png
│   ├── upload.png
│   ├── analysis.png
│   ├── dashboard.png
│   ├── report.png
│   └── history.png
│
├── data/
│   └── history.json
│
├── app.py
├── ai_analyzer.py
├── ats_calculator.py
├── history_manager.py
├── interview_generator.py
├── pdf_report.py
├── resume_parser.py
├── skill_matcher.py
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

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

# 🔑 Environment Variables

Create a `.env` file and add:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

---

# 💡 Future Enhancements

- AI Resume Builder
- Cover Letter Generator
- Resume Ranking
- Company-wise ATS Analysis
- Voice Mock Interviews
- Recruiter Dashboard
- Multi-language Support

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

Fork the repository and submit a pull request.

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

---

# 👩‍💻 Author

**Polagowni Laxmiprasanna**

- GitHub: https://github.com/laxmiprasannapolagowni
- LinkedIn: https://www.linkedin.com/in/laxmiprasannapolagowni/
