def optimize_content(section_text, jd_keywords, allowed_skills, client):
    """
    Optimize resume content while maintaining truthfulness.
    """
    if not section_text or len(section_text.strip()) < 10:
        return section_text
    
    allowed_skills_str = ", ".join(allowed_skills) if allowed_skills else "none"
    keywords_str = ", ".join(jd_keywords[:15]) if jd_keywords else "none"
    
    prompt = f"""
    Rewrite and optimize this resume section to match the job description.
    
    CRITICAL CONSTRAINTS:
    1. Use ONLY these verified skills: {allowed_skills_str}
    2. Do NOT invent new jobs, companies, titles, or certifications
    3. Do NOT add false achievements or metrics
    4. Incorporate these ATS keywords naturally: {keywords_str}
    5. Use strong action verbs (Engineered, Developed, Implemented, etc.)
    6. Make bullet points measurable where possible
    7. Keep all claims truthful and verifiable
    
    Original Content:
    {section_text[:5000]}
    
    Return the optimized content only. No explanations.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert resume writer who prioritizes truthfulness."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Optimization Error: {str(e)}]\n\n{section_text}"

def calculate_match_score(resume_skills, jd_required_skills):
    """Calculate ATS match score"""
    if not jd_required_skills:
        return 0
    
    resume_set = set([s.lower() for s in resume_skills])
    jd_set = set([s.lower() for s in jd_required_skills])
    
    matched = resume_set.intersection(jd_set)
    score = int((len(matched) / len(jd_set)) * 100)
    
    return min(score, 100)  # Cap at 100