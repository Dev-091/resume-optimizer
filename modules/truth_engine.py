class TruthEngine:
    """
    Ensures all skills in the optimized resume are truthful.
    Only allows skills that exist in original resume OR GitHub profile.
    """
    
    def __init__(self, resume_skills, github_skills):
        # Normalize all skills to lowercase for comparison
        self.resume_skills = set([s.lower().strip() for s in resume_skills if s])
        self.github_skills = set([s.lower().strip() for s in github_skills if s])
        self.allowed_skills = self.resume_skills | self.github_skills
        self.rejected_skills = []
    
    def verify_skill(self, skill):
        """Check if a skill is allowed (truthful)"""
        if skill.lower().strip() in self.allowed_skills:
            return True
        else:
            self.rejected_skills.append(skill)
            return False
    
    def get_allowed_list(self):
        """Return list of verified skills"""
        return list(self.allowed_skills)
    
    def get_rejection_report(self):
        """Return skills that were rejected for truthfulness"""
        return self.rejected_skills
    
    def get_stats(self):
        """Return verification statistics"""
        return {
            "resume_skills_count": len(self.resume_skills),
            "github_skills_count": len(self.github_skills),
            "total_allowed": len(self.allowed_skills),
            "rejected_count": len(self.rejected_skills)
        }