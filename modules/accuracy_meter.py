import json

class AccuracyMeter:
    """
    Measures the quality and accuracy of the optimized resume.
    Dimensions:
    - JD Alignment (Keywords & Skills)
    - Truth Integrity (Verification against sources)
    - Structural Integrity (Format preservation)
    - Professional Excellence (LLM-based Audit)
    """

    def __init__(self, client):
        self.client = client

    def calculate_jd_match(self, resume_skills, jd_required_skills):
        """Quantitatively measure skill overlap"""
        if not jd_required_skills:
            return 100
        
        resume_set = set([s.lower() for s in resume_skills if s])
        jd_set = set([s.lower() for s in jd_required_skills if s])
        
        matched = resume_set.intersection(jd_set)
        return int((len(matched) / len(jd_set)) * 100) if jd_set else 0

    def calculate_truth_score(self, optimized_skills, verified_skills):
        """Measure what percentage of current skills are verified"""
        if not optimized_skills:
            return 100
            
        opt_set = set([s.lower() for s in optimized_skills if s])
        ver_set = set([s.lower() for s in verified_skills if s])
        
        # All skills in optimized resume SHOULD be in verified_skills
        unverified = opt_set - ver_set
        score = 100 - (len(unverified) * 10) # Heavy penalty for unverified claims
        return max(0, min(100, score))

    def perform_ai_audit(self, resume_data, jd_text):
        """Use LLM to perform a deep qualitative audit of the resume's alignment"""
        prompt = f"""
        You are a Senior Technical Recruiter. Evaluate the following optimized resume against the Job Description.
        
        Resume Content:
        {str(resume_data)[:5000]}
        
        Job Description:
        {jd_text[:3000]}
        
        Provide a quality score (0-100) for these categories in JSON:
        1. alignment_score: How well the resume matches the JD requirements.
        2. professional_tone: Quality of writing and professional impact.
        3. relevance: Percentage of content directly relevant to the role.
        
        Return ONLY valid JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a critical hiring manager evaluating a candidate."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content.strip())
        except Exception:
            return {"alignment_score": 70, "professional_tone": 70, "relevance": 70}

    def get_comprehensive_score(self, resume_data, jd_data, verified_skills, jd_text):
        """Calculate weighted final accuracy score"""
        jd_match = self.calculate_jd_match(resume_data.get('skills', []), jd_data.get('required_skills', []))
        truth_score = self.calculate_truth_score(resume_data.get('skills', []), verified_skills)
        ai_audit = self.perform_ai_audit(resume_data, jd_text)
        
        # Weighted average
        # 30% JD Match, 30% Truthfulness, 40% AI Audit (Alignment + Tone + Relevance)
        audit_avg = (ai_audit['alignment_score'] + ai_audit['professional_tone'] + ai_audit['relevance']) / 3
        
        final_score = (jd_match * 0.3) + (truth_score * 0.3) + (audit_avg * 0.4)
        
        return {
            "overall_accuracy": round(final_score, 1),
            "jd_match_score": jd_match,
            "truth_integrity_score": truth_score,
            "ai_audit": ai_audit,
            "breakdown": {
                "JD Alignment": ai_audit['alignment_score'],
                "Professional Tone": ai_audit['professional_tone'],
                "Relevant Content": ai_audit['relevance']
            }
        }
