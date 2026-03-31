import json

def analyze_jd(job_description, client):
    """Analyze Job Description and extract requirements"""
    prompt = f"""
    Analyze this Job Description and extract the following into JSON:
    - required_skills: Must-have technical skills
    - preferred_skills: Nice-to-have skills
    - tools_and_frameworks: Specific tools mentioned
    - responsibilities: Key job responsibilities
    - ats_keywords: Important keywords for ATS systems
    - soft_skills: Required soft skills
    
    Job Description:
    {job_description[:8000]}
    
    Return ONLY valid JSON. No markdown, no explanations.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a technical recruiter analyzing job descriptions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        return {
            "error": str(e),
            "required_skills": [],
            "preferred_skills": [],
            "tools_and_frameworks": [],
            "responsibilities": [],
            "ats_keywords": [],
            "soft_skills": []
        }