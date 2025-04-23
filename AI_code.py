import ollama
import pdfplumber
from docx import Document
from typing import Optional

def extract_resume_text(file_path: str) -> str:
    """
    📂 Extract text from resume files (PDF/DOCX/TXT)
    
    Args:
        file_path: Path to resume document
        
    Returns:
        str: Extracted text or error message
    """
    try:
        file_path = file_path.replace("\\", "/")
        
        if file_path.lower().endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)
            
        elif file_path.lower().endswith('.docx'):
            doc = Document(file_path)
            return "\n".join(para.text for para in doc.paragraphs)
            
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
                
        else:
            raise ValueError("❌ Unsupported file format. Please use PDF, DOCX, or TXT")
            
    except Exception as e:
        return f"⚠️ File Error: {str(e)}"

def create_analysis_prompt(resume_text: str, job_description: str) -> str:
    """
    🚀 Generate AI analysis prompt with structured format
    
    Args:
        resume_text: Extracted resume content
        job_description: Target job requirements
        
    Returns:
        str: Formatted prompt for AI analysis
    """
    return f"""
    📋 **Resume Analysis Request** 📋
    ----------------------------------
    
    📄 **Candidate Profile**:
    {resume_text[:2000]}... [truncated]
    
    💼 **Job Description**:
    {job_description}
    
    🔍 **Analysis Requirements**:
    1️⃣  Eligibility Verification (Technical/Experience Match, No Experience Match needed For Freshers)
    2️⃣  Bias Identification (Non-relevant Factors)
    3️⃣  Skill Development Roadmap (Tiered Recommendations)
    4️⃣  Final Hiring Recommendation
    
    📊 **Output Format**:
    ✅  Eligibility: [Yes/No]
    🚩  Bias Detected: [Yes/No] + Explanation
    📌  Key Qualifications: 3-5 bullet points
    📈  Development Plan:
      • Immediate (1-2 weeks) 🚀
      • Mid-term (1-3 months) 📅
      • Long-term (6+ months) 🎯
    💡  Final Recommendation: Detailed assessment
    """

def generate_ai_analysis(prompt: str) -> Optional[str]:
    """
    🤖 Process analysis through AI model
    
    Args:
        prompt: Formatted analysis prompt
        
    Returns:
        str: AI-generated analysis or None
    """
    try:
        response = ollama.generate(
            model="mistral",
            prompt=prompt,
            options={
                "temperature": 0.5,
                "max_tokens": 500,
                "num_ctx": 2048
            }
        )
        return response['response']
    except Exception as e:
        print(f"⚠️ Analysis Error: {str(e)}")
        return None

def main():
    """
    📊 Main execution flow for Resume Analyzer
    """
    print("\n🔍 Resume Analysis System v1.2 🔍")
    print("-------------------------------\n")
    
    # Sample job description 
    job_description = (
        "🌐 **Position Requirements**:\n"
        "- Python programming (3+ years) 🐍\n"
        "- Machine Learning frameworks (TensorFlow/PyTorch) 🤖\n"
        "- Cloud platform experience (AWS/Azure) ☁️\n"
    )
    
    file_path = input("📁 Enter resume file path: ").strip()
    resume_text = extract_resume_text(file_path)
    
    if resume_text.startswith("⚠️"):
        print(f"\n{resume_text}")
        return
    
    print("\n🔎 Parsing resume contents...")
    analysis_prompt = create_analysis_prompt(resume_text, job_description)
    
    print("\n🚀 Generating professional assessment...")
    analysis = generate_ai_analysis(analysis_prompt)
    
    if analysis:
        print("\n📊 Analysis Results:")
        print("--------------------")
        print(analysis)
    else:
        print("⛔ Failed to generate analysis")

if __name__ == "__main__":
    main()