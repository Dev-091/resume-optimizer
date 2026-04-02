def optimize_content(section_text, jd_keywords, allowed_skills, client):
    """
    Optimize resume content while maintaining truthfulness.
    """
    if not section_text or len(section_text.strip()) < 10:
        return section_text
    
    allowed_skills_str = ", ".join(allowed_skills) if allowed_skills else "none"
    keywords_str = ", ".join(jd_keywords[:15]) if jd_keywords else "none"
    
    prompt = f"""
    You are a professional resume writer and ATS specialist. Your task is to rewrite the provided resume section to align perfectly with the target Job Description while remaining 100% truthful.
    
    CRITICAL CONSTRAINTS:
    1. EXCLUSIVITY: Use ONLY these verified skills: {allowed_skills_str}
    2. HONESTY: Do NOT invent new jobs, companies, titles, or certifications.
    3. ATS OPTIMIZATION: Naturalistically incorporate these high-impact keywords: {keywords_str}
    4. ACTION ORIENTATION: Start each bullet point with strong, varied action verbs (e.g., 'Spearheaded', 'Optimized', 'Architected').
    5. QUANTIFICATION: Include metrics and results where possible (e.g., 'Reduced latency by 30%', 'Managed team of 10').
    6. LENGTH PRESERVATION: Maintain a similar word count to the original to prevent layout disruption.
    7. TONE: Maintain a professional, executive-level tone.
    
    Original Content:
    {section_text[:5000]}
    
    RESPONSE FORMAT:
    Return ONLY the optimized content. No explanations, no introductory text, no markdown headers.
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