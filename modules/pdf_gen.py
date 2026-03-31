from fpdf import FPDF
import os

class PDFGenerator:
    """Generate ATS-friendly PDF resume"""
    
    def generate(self, optimized_data, filename="optimized_resume.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Set fonts
        pdf.set_font("Helvetica", "B", 16)
        
        # Title
        pdf.cell(0, 10, "OPTIMIZED RESUME", ln=True, align='C')
        pdf.ln(5)
        
        # Helper function for safe text encoding
        def safe_text(text):
            if not text:
                return ""
            # Encode to latin-1 (FPDF compatible) and replace unsupported chars
            return str(text).encode('latin-1', 'replace').decode('latin-1')
        
        # Professional Summary
        if optimized_data.get('summary'):
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "PROFESSIONAL SUMMARY", ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 6, safe_text(optimized_data['summary']))
            pdf.ln(5)
        
        # Experience
        if optimized_data.get('experience'):
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "WORK EXPERIENCE", ln=True)
            pdf.set_font("Helvetica", "", 10)
            exp_text = safe_text(str(optimized_data['experience'])[:2000])
            pdf.multi_cell(0, 6, exp_text)
            pdf.ln(5)
        
        # Skills
        if optimized_data.get('skills'):
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "SKILLS", ln=True)
            pdf.set_font("Helvetica", "", 10)
            skills_str = ", ".join(optimized_data['skills'][:20])
            pdf.multi_cell(0, 6, safe_text(skills_str))
            pdf.ln(5)
        
        # Education
        if optimized_data.get('education'):
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "EDUCATION", ln=True)
            pdf.set_font("Helvetica", "", 10)
            edu_text = safe_text(str(optimized_data['education'])[:1000])
            pdf.multi_cell(0, 6, edu_text)
            pdf.ln(5)
        
        # Projects
        if optimized_data.get('projects'):
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "PROJECTS", ln=True)
            pdf.set_font("Helvetica", "", 10)
            proj_text = safe_text(str(optimized_data['projects'])[:1500])
            pdf.multi_cell(0, 6, proj_text)
        
        # Save PDF
        pdf.output(filename)
        return filename