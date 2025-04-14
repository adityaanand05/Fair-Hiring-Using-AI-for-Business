import ollama
import pdfplumber
from docx import Document

# Function to read resume based on file type
def read_resume(file_path):
    file_path = file_path.replace("\\", "/")
    try:
        if file_path.lower().endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                print("📄 Text has been Extrected from REsume or CV:", text[:100])  # Debug
                return text
        elif file_path.lower().endswith('.docx'):
            doc = Document(file_path)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            print("📄 Text has been Extrected from REsume or CV:", text[:100])
            return text
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            print("📄 Text has been Extrected from REsume or CV:", text[:100])
            return text
        else:
            return "❌ Error: Unsupported file format. Use .txt, .pdf, or .docx"
    except Exception as e:
        return f"⚠️ Error reading resume: {e}"
    
'''Input:
- Resume PDF Text: {{resume_text}}
- Job Description: {{job_description}}'''

# Optimized Prompt (Concise for Speed)
def generate_prompt(resume, job_desc):
    return f"""
📄 **Resume:** {resume}
💼 **Job Description:** {job_desc}

🧠 *AI Judgement Time!*

You are an experienced HR professional with over 15 years of expertise in AI, NLP, and ethical hiring practices. You are reviewing a candidate’s resume and a job description. Your goal is to:

1. **Assess candidate eligibility** for the role based on relevant experience, skills, and project alignment.
2. **Detect any potential biases** in evaluation based on name, gender, school, or non-job-related attributes. Explain whether such elements influence traditional hiring but shouldn't in an ethical AI review.
3. If the candidate is **not eligible**, give a clear explanation with missing skills or experience, and suggest specific ways to improve.
4. If the candidate **is eligible**, provide a rationale, highlight strengths, and suggest areas to further polish.
5. Provide **skill recommendations** in three tiers:
   - **Immediate fixes** (1–2 weeks of effort)
   - **Mid-term improvements** (1–3 months)
   - **Long-term growth** (over 6 months)
6. Use a fair, encouraging, and inclusive tone throughout your analysis.



Output:
- ✅  Eligibility: Yes/No
- 🧠  Bias Detected: Yes/No + Analysis
- 🔍  Rationale: (3–5 bullet points)
- 📚  Skill Improvement Plan: (with tiered suggestions)
- 💡  Final HR Advice: (as if guiding a mentee)

Be accurate, kind, and focused on growth.

"""

# Dummy Job Description (AI/ML role)
job_desc = "Requires: Python 🐍, Machine Learning 🤖, 2 years AI/ML experience 👨‍💻"

# Resume Upload ka Logic
print("📂 Paste Your File Path Here (Like 'C:/path/to/resume.pdf' ya '.docx'):")
resume_file_path = input("📝 Resume file path: ")
resume = read_resume(resume_file_path)

if "Error" not in resume:
    # Generate Prompt
    prompt = generate_prompt(resume, job_desc)
    print("⚙️  Taking result from Model... 🤖")

    # Call Ollama Directly
    try:
        response = ollama.generate(
            model="mistral",  # Chhota model for speed
            prompt=prompt,
            options={
                "temperature": 0.5,
                "max_tokens": 300,  # Kam tokens = fast output
                "num_ctx": 1024    # Kam context = fast processing
            }
        )
        print("🧾 Result:\n", response['response'])
    except Exception as e:
        print(f"❗ Error: {e}")
else:
    print(resume)
