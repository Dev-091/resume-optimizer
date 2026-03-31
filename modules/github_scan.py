import json
from github import Github

def scan_github(username, token, client):
    """Scan GitHub profile and extract verified skills"""
    try:
        if token and token.strip():
            g = Github(token)
        else:
            g = Github()  # Unauthenticated (lower rate limit)
        
        user = g.get_user(username)
        repos = user.get_repos(sort='updated', direction='desc')[:5]
        
        repo_data = []
        for repo in repos:
            readme = ""
            try:
                readme_content = repo.get_readme()
                readme = readme_content.decoded_content.decode()[:1500]
            except:
                pass
            
            languages = repo.get_languages()
            
            repo_data.append({
                "name": repo.name,
                "description": repo.description or "",
                "languages": list(languages.keys()),
                "readme": readme
            })
        
        # Use Groq to infer skills from repo data
        prompt = f"""
        Based on these GitHub repositories, extract verified technical skills.
        Only include skills that are clearly demonstrated in the code or README.
        
        Repository Data:
        {str(repo_data)[:8000]}
        
        Return JSON with:
        - verified_skills: List of skills proven by repositories
        - project_highlights: List of notable project achievements
        
        Return ONLY valid JSON. No markdown.
        """
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a technical analyst reviewing GitHub profiles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content.strip()
        content = content.replace('```json', '').replace('```', '').strip()
        
        return json.loads(content)
        
    except Exception as e:
        return {
            "error": str(e),
            "verified_skills": [],
            "project_highlights": []
        }