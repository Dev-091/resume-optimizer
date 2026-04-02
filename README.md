# 📄 AI Resume Optimizer

**Truthful • ATS-Friendly • GitHub-Verified**  
Powered by Groq (Llama 3.1) • 100% Free

AI Resume Optimizer is a Streamlit-based web application that re-writes and optimizes your resume for Applicant Tracking Systems (ATS) while ensuring **complete truthfulness** by verifying your skills against your GitHub profile. 

Unlike other resume builders, it **preserves your original formatting** by using a sophisticated PDF-to-Word conversion pipeline, ensuring your carefully crafted layout remains intact.

## ✨ Why This Tool is Special

- **Format Preservation**: Injects ATS keywords into your resume without breaking your original PDF layout and aesthetics.
- **Truth Verification Engine**: Cross-checks your claimed skills against your public GitHub profile repositories and languages to ensure accuracy. Prevents AI from hallucinating skills you don't possess.
- **Agent Accuracy Meter**: Provides a comprehensive score of the optimization quality, grading the JD alignment, truth integrity, and overall AI quality audit.
- **Lightning Fast AI**: Powered by Groq's high-speed Llama 3.1 model to generate optimized summaries, experiences, and targeted skills in seconds.

## 🚀 How It Works

1. **Upload Resume**: Upload your current PDF resume. The system parses and structures the text.
2. **Job Description**: Paste the target Job Description (JD). The AI analyzes exactly what the employer is looking for.
3. **GitHub Verification**: Provide your GitHub username. The agent scans your public commits and repositories to compile a verified list of skills.
4. **Optimization**: The agent rewrites your summary and experience to align with the JD, but *only* uses skills that pass the Truth Verification Engine.
5. **Download**: The system repackages the optimized content directly into your original layout, giving you a fresh PDF and an editable DOCX file.

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- A [Groq API Key](https://console.groq.com/) 

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dev-091/resume-optimizer.git
   cd resume-optimizer
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows:
   .\venv\Scripts\activate
   
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your Groq API Key:**
   - You can enter it directly in the app sidebar.
   - Alternatively, create a file named `api_key.txt` in the root directory and paste your Groq API key inside it.
   - For Streamlit Cloud deployment, add `GROQ_API_KEY` to your Streamlit secrets.

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 📦 Tech Stack
- Frontend: [Streamlit](https://streamlit.io/)
- LLM Inference: [Groq](https://groq.com/)
- PDF Processing: `pdfplumber`, `fpdf2`
- Document Conversion: `python-docx`, `pdf2docx`, `docx2pdf`
- APIs: GitHub REST API

## 📝 License
This project is open-source and available to use free of charge. Built By Dev Sharma❤️ 