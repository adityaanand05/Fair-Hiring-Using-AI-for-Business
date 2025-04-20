import ollama
import pdfplumber
from docx import Document

def read_resume(file_path):
    file_path = file_path.replace("\\", "/")
    try:
        if file_path.lower().endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        elif file_path.lower().endswith('.docx'):
            doc = Document(file_path)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            return "❌ Error: Unsupported file format. Use .txt, .pdf, or .docx"
    except Exception as e:
        return f"⚠️ Error reading resume or cv: {e}"

def generate_prompt(resume, job_desc):
    return f"""
📄 **Resume:** {resume}
💼 **Job Description:** {job_desc}

🧠 *AI Judgement Time!*
... You are an experienced HR professional with over 15 years of expertise in ethical hiring practices. Be relevant in your work, first think then answer your points. You are reviewing a candidate’s resume and a job description. Your goal is to:

Output:
- ✅  Eligibility: Yes/No
- 🧠  Bias Detected: Yes/No + Analysis(in terms of age, gender, religion, caste, etc)
- 🔍  Rationale: (3–5 bullet points)
- 📚  Skill Improvement Plan: (point 1,2,3...)
- 💡  Final HR Advice: (as if guiding a mentee)

Be accurate, kind, and focused on growth.
"""

def analyze_resume(file_path, job_desc):
    resume = read_resume(file_path)
    if "Error" not in resume:
        prompt = generate_prompt(resume, job_desc)
        try:
            response = ollama.generate(
                model="mistral",
                prompt=prompt,
                options={
                    "temperature": 0.5,
                    "max_tokens": 300,
                    "num_ctx": 1024
                }
            )
            return response['response']
        except Exception as e:
            return f"❗ Error during model generation: {e}"
    else:
        return resume
