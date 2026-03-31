import pdfplumber
import json

def extract_text(pdf_path):
    """Extract text from PDF file"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def structure_resume(text, client):
    """Use Groq to structure resume into JSON"""
    prompt = f"""
    Extract resume data into valid JSON format.
    Required keys: professional_summary, work_experience, skills, education, projects, certifications
    
    work_experience should be a list of objects with: title, company, duration, bullets
    projects should be a list of objects with: name, description, tech_stack
    skills should be a simple list of strings
    
    Resume Text:
    {text[:12000]}
    
    Return ONLY valid JSON. No markdown, no explanations.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a resume data extraction expert. Return only JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content.strip()
        # Clean markdown if present
        content = content.replace('```json', '').replace('```', '').strip()
        
        return json.loads(content)
    except Exception as e:
        return {
            "error": str(e),
            "professional_summary": "",
            "work_experience": [],
            "skills": [],
            "education": [],
            "projects": [],
            "certifications": []
        }