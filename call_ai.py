from AI_code import analyze_resume

job_desc = input("Enter the job description: ")
resume_path = input("Enter the path to the resume (PDF, DOCX, or TXT): ")
print("📄 Reading resume...")
print("📝 Generating analysis...")
result = analyze_resume(resume_path, job_desc)
print("🧾 Analysis Result:\n", result)



