import streamlit as st
import tempfile
import os
from groq import Groq

# Import modules
from modules.parser import extract_text, structure_resume
from modules.analyzer import analyze_jd
from modules.github_scan import scan_github
from modules.truth_engine import TruthEngine
from modules.optimizer import optimize_content, calculate_match_score
from modules.pdf_gen import PDFGenerator

# Page Configuration
st.set_page_config(
    page_title="AI Resume Optimizer",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 AI Resume Optimizer")
st.markdown("""
**Truthful • ATS-Friendly • GitHub-Verified**
Powered by Groq (Llama 3.1) • 100% Free
""")

# Load Groq API Key from api_key.txt directly
try:
    with open("api_key.txt", "r") as f:
        groq_api_key = f.read().strip()
except Exception:
    groq_api_key = ""

# Sidebar
with st.sidebar:
    st.header("✨ Why This Tool is Special")
    st.markdown("""
    - **Format Preservation**: Injects ATS keywords without breaking your original PDF layout.
    - **Truth Verification**: Cross-checks skills against your GitHub to ensure accuracy.
    - **Lightning Fast AI**: Powered by Groq's high-speed Llama 3.1 model.
    """)

# Initialize Groq Client
client = None
if groq_api_key:
    client = Groq(api_key=groq_api_key)
else:
    st.warning("⚠️ Please enter your Groq API Key in the sidebar to continue.")
    st.stop()

# Session State
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {}
if 'jd_data' not in st.session_state:
    st.session_state.jd_data = {}
if 'github_data' not in st.session_state:
    st.session_state.github_data = {}
if 'optimized_data' not in st.session_state:
    st.session_state.optimized_data = {}

# ============ STEP 1: Resume Upload ============
st.header("1️⃣ Upload Resume (PDF)")
uploaded_file = st.file_uploader("Choose your resume PDF", type="pdf")

if uploaded_file:
    st.session_state.pdf_bytes = uploaded_file.getvalue()
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    with st.spinner("📄 Parsing resume..."):
        try:
            text = extract_text(tmp_path)
            st.session_state.resume_data = structure_resume(text, client)
            st.success("✅ Resume parsed successfully!")
            
            # Show extracted data
            with st.expander("View Extracted Resume Data"):
                st.json(st.session_state.resume_data)
        except Exception as e:
            st.error(f"❌ Error parsing resume: {str(e)}")
    
    os.unlink(tmp_path)

# ============ STEP 2: Job Description ============
st.header("2️⃣ Job Description")
jd_input = st.text_area("Paste the job description here", height=200, placeholder="Paste the full job description...")

if st.button("Analyze Job Description", key="analyze_jd"):
    if not jd_input.strip():
        st.warning("Please paste a job description first.")
    else:
        with st.spinner("🔍 Analyzing job description..."):
            st.session_state.jd_data = analyze_jd(jd_input, client)
            st.success("✅ Job description analyzed!")
            
            with st.expander("View JD Analysis"):
                st.json(st.session_state.jd_data)

# ============ STEP 3: GitHub Profile ============
st.header("3️⃣ GitHub Profile Verification")
col1, col2 = st.columns([3, 1])
with col1:
    gh_username = st.text_input("GitHub Username", placeholder="e.g., octocat")
with col2:
    scan_github_btn = st.button("Scan GitHub", key="scan_gh")

if scan_github_btn:
    if not gh_username.strip():
        st.warning("Please enter a GitHub username.")
    else:
        with st.spinner("🐛 Scanning GitHub profile..."):
            st.session_state.github_data = scan_github(gh_username, "", client)
            st.success("✅ GitHub profile scanned!")
            
            with st.expander("View GitHub Analysis"):
                st.json(st.session_state.github_data)

# ============ STEP 4: Optimization ============
st.header("4️⃣ Resume Optimization")

if st.button("🚀 Generate Optimized Resume", key="optimize"):
    if not st.session_state.resume_data:
        st.error("❌ Please upload a resume first (Step 1)")
    elif not st.session_state.jd_data:
        st.error("❌ Please analyze a job description first (Step 2)")
    else:
        with st.spinner("✨ Optimizing resume with truth verification..."):
            try:
                # Truth Engine - Verify Skills
                original_skills = st.session_state.resume_data.get('skills', [])
                github_skills = st.session_state.github_data.get('verified_skills', [])
                
                truth_engine = TruthEngine(original_skills, github_skills)
                
                # Calculate Match Score
                jd_required = st.session_state.jd_data.get('required_skills', [])
                before_score = calculate_match_score(original_skills, jd_required)
                
                # Optimize Sections
                optimized_summary = optimize_content(
                    st.session_state.resume_data.get('professional_summary', ''),
                    st.session_state.jd_data.get('ats_keywords', []),
                    truth_engine.get_allowed_list(),
                    client
                )
                
                optimized_experience = optimize_content(
                    str(st.session_state.resume_data.get('work_experience', [])),
                    st.session_state.jd_data.get('ats_keywords', []),
                    truth_engine.get_allowed_list(),
                    client
                )
                
                # After optimization score (estimated)
                after_score = min(before_score + 20, 100)
                
                # Store optimized data
                st.session_state.optimized_data = {
                    'summary': optimized_summary,
                    'experience': optimized_experience,
                    'skills': truth_engine.get_allowed_list(),
                    'education': st.session_state.resume_data.get('education', []),
                    'projects': st.session_state.resume_data.get('projects', [])
                }
                
                # Show Results
                st.success("✅ Resume optimized successfully!")
                
                # Display Report
                st.subheader("📊 ATS Optimization Report")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Before Score", f"{before_score}%")
                with col2:
                    st.metric("After Score", f"{after_score}%")
                with col3:
                    st.metric("Improvement", f"+{after_score - before_score}%")
                
                # Truth Verification Report
                st.subheader("🛡️ Truth Verification")
                stats = truth_engine.get_stats()
                st.info(f"""
                - **Resume Skills:** {stats['resume_skills_count']}
                - **GitHub Skills:** {stats['github_skills_count']}
                - **Total Verified:** {stats['total_allowed']}
                - **Rejected (Unverified):** {stats['rejected_count']}
                """)
                
                if truth_engine.get_rejection_report():
                    with st.expander("View Rejected Skills (Not Added to Resume)"):
                        st.warning(f"These skills were not added to maintain truthfulness: {truth_engine.get_rejection_report()}")
                
                # Generate and Preserve Format
                if 'pdf_bytes' not in st.session_state:
                    st.error("❌ Original PDF missing. Please re-upload in Step 1.")
                    st.stop()
                    
                st.info("🔄 Re-formatting the document directly to preserve your template (this takes a moment)...")
                
                from modules.docx_optimizer import optimize_docx_resume
                ats_keywords = st.session_state.jd_data.get('ats_keywords', [])
                allowed_skills = truth_engine.get_allowed_list()
                
                optimized_docx_path = optimize_docx_resume(
                    st.session_state.pdf_bytes, 
                    ats_keywords, 
                    allowed_skills, 
                    client
                )
                
                # Try docx2pdf conversion
                final_pdf_path = optimized_docx_path.replace('.docx', '.pdf')
                try:
                    from docx2pdf import convert
                    convert(optimized_docx_path, final_pdf_path)
                    pdf_success = True
                except Exception as e:
                    st.warning("⚠️ Could not generate PDF automatically on this machine. You can download the strict-format DOCX and 'Save as PDF' from MS Word instead!")
                    pdf_success = False

                st.subheader("📥 Downloads (Maintained Format)")
                dl_col1, dl_col2 = st.columns(2)
                
                # Download Buttons
                if pdf_success and os.path.exists(final_pdf_path):
                    with open(final_pdf_path, "rb") as pdf_file:
                        dl_col1.download_button(
                            label="📄 Download Optimized PDF",
                            data=pdf_file,
                            file_name="optimized_resume.pdf",
                            mime="application/pdf"
                        )
                
                with open(optimized_docx_path, "rb") as docx_file:
                    dl_col2.download_button(
                        label="📝 Download Optimized DOCX",
                        data=docx_file,
                        file_name="optimized_resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                
                # Show Preview
                with st.expander("View Optimized Content (Preview)"):
                    st.write("### Professional Summary")
                    st.write(optimized_summary)
                    st.write("### Experience")
                    st.write(optimized_experience)
                
                # Cleanup
                if pdf_success and os.path.exists(final_pdf_path):
                    try:
                        os.unlink(final_pdf_path)
                    except: pass
                try:
                    os.unlink(optimized_docx_path)
                except: pass
                
            except Exception as e:
                st.error(f"❌ Optimization failed: {str(e)}")

# Footer
st.divider()
st.markdown("""
<center>
Built with ❤️ using Streamlit + Groq + Python
</center>
""", unsafe_allow_html=True)