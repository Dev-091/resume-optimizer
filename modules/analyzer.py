import json

def analyze_jd(job_description, client):
    """Analyze Job Description and extract requirements"""
    prompt = f"""
    You are an expert technical recruiter. Analyze the following Job Description to identify technical requirements, soft skills, and ATS optimization keywords.
    
    Required JSON Response Structure:
    {{
        "job_title": "Primary title for the position",
        "required_skills": ["Critical hard skill 1", "Critical hard skill 2"],
        "preferred_skills": ["Nice to have skill 1"],
        "tools_and_frameworks": ["Specific tool/library 1", "Specific tool/library 2"],
        "responsibilities": ["Key duty 1", "Key duty 2"],
        "ats_keywords": ["ATS optimized keyword 1", "Industry term 2"],
        "soft_skills": ["Interpersonal skill 1"],
        "implicit_requirements": ["Unofficial but likely requirement based on JD context"]
    }}
    
    CRITICAL INSTRUCTIONS:
    1. Distinguish clearly between required and preferred skills.
    2. Extract specific technical tools mentioned (e.g., "Docker", "React", "Kibana").
    3. Identify "Implicit Requirements": For example, if the JD mentions "scaling systems", "System Design" is an implicit requirement.
    
    Job Description:
    {job_description[:8000]}
    
    Return ONLY valid JSON. No markdown, no explanations, no preamble.
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