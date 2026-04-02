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
    You are a professional Resume Data Extractor. Your goal is to parse the following resume text into a highly structured JSON format.
    
    CRITICAL INSTRUCTIONS:
    1. Extract all information accurately. If a section is missing, return an empty list or empty string.
    2. Format dates consistently (e.g., "MM/YYYY" or "Month YYYY").
    3. For `work_experience`, break down the 'bullets' into a clean list of strings.
    4. For `skills`, categorize them where possible but return a flat list for the main 'skills' key.
    
    Required JSON Structure:
    {{
        "professional_summary": "A concise summary of the candidate's career.",
        "work_experience": [
            {{
                "title": "Job Title",
                "company": "Company Name",
                "location": "City, State/Country",
                "duration": "Dates (e.g., Jan 2020 - Present)",
                "bullets": ["Achievement 1", "Achievement 2"]
            }}
        ],
        "skills": ["Skill 1", "Skill 2"],
        "education": [
            {{
                "degree": "Degree Name",
                "school": "University/School Name",
                "year": "Graduation Year"
            }}
        ],
        "projects": [
            {{
                "name": "Project Name",
                "description": "Short description",
                "tech_stack": ["Tech 1", "Tech 2"]
            }}
        ],
        "certifications": ["Cert 1", "Cert 2"]
    }}
    
    Resume Text:
    {text[:12000]}
    
    Return ONLY valid JSON. No markdown, no explanations, no preamble.
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