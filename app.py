"""
SkillBridge - AI-Powered Career Gap Analyzer
Production-ready Streamlit application with Google Gemini AI
"""

import os
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import json
import time

# ===================== CONFIGURATION =====================

# Load Gemini API Key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ Gemini API key not found. Please set GEMINI_API_KEY as an environment variable.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# Page Configuration
st.set_page_config(
    page_title="SkillBridge - Career Gap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== CUSTOM CSS =====================
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #ffffff;
    }

    h1, h2, h3 {
        color: #ffffff !important;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }

    .stButton button {
        background: linear-gradient(to right, #3b82f6, #10b981) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }

    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
    }

    .timeline-item {
        background-color: #1e293b;
        border-left: 3px solid #3b82f6;
        padding: 16px;
        margin: 12px 0;
        border-radius: 8px;
    }

    .timeline-item:hover {
        background-color: #334155;
        border-left-color: #10b981;
    }
</style>
""", unsafe_allow_html=True)

# ===================== SESSION STATE =====================
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "results" not in st.session_state:
    st.session_state.results = None

# ===================== UTILITY FUNCTIONS =====================

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF"""
    reader = PdfReader(pdf_file)
    return " ".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_image(image_file):
    """Extract text from uploaded image using OCR"""
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)

def analyze_with_gemini(resume_text, target_role):
    """Analyze resume using Google Gemini AI"""
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
Analyze this resume for the role: "{target_role}"

Resume:
{resume_text[:5000]}

Return ONLY valid JSON with:
match_score, current_level, target_level,
market_insights, strengths, critical_gaps, roadmap (4 weeks).
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end])

# ===================== UI COMPONENTS =====================

def display_hero():
    st.markdown(
        "<h1 style='text-align:center; font-size:56px; background:linear-gradient(to right,#3b82f6,#10b981); -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>Don't Guess Your Career Path. Engineer It.</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center; font-size:20px; color:#94a3b8;'>Upload your resume, choose a role, and get a 4-week action plan.</p>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        target_role = st.text_input("Target Role", placeholder="e.g. ML Engineer")

        uploaded_file = st.file_uploader(
            "Upload Resume (PDF / Image / TXT)",
            type=["pdf", "png", "jpg", "jpeg", "txt"]
        )

        resume_text = ""
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            elif "image" in uploaded_file.type:
                resume_text = extract_text_from_image(uploaded_file)
            else:
                resume_text = uploaded_file.read().decode("utf-8")

            st.success("Resume text extracted successfully.")

        if st.button("🚀 Analyze Now", use_container_width=True):
            if not target_role or not resume_text:
                st.error("Please provide both resume and target role.")
            else:
                with st.spinner("Analyzing career gap..."):
                    time.sleep(1)
                    st.session_state.results = analyze_with_gemini(resume_text, target_role)
                    st.session_state.analyzed = True
                    st.rerun()

def display_results(results):
    st.markdown("<h2 style='text-align:center;'>🎯 Career Intelligence Report</h2>", unsafe_allow_html=True)

    if st.button("← New Analysis"):
        st.session_state.analyzed = False
        st.session_state.results = None
        st.rerun()

    col1, col2, col3 = st.columns([1, 1, 1.5])

    with col1:
        st.metric("Match Score", f"{results['match_score']}%")
        st.write("**Current Level:**", results["current_level"])
        st.write("**Target Level:**", results["target_level"])

    with col2:
        st.subheader("Strengths")
        for s in results["strengths"]:
            st.write("•", s)

        st.subheader("Critical Gaps")
        for g in results["critical_gaps"]:
            st.write("•", g)

    with col3:
        st.subheader("4-Week Roadmap")
        for week in results["roadmap"]:
            st.markdown(
                f"""
                <div class="timeline-item">
                    <strong>Week {week['week']}:</strong> {week['title']}<br>
                    • {week['focus']}<br>
                    <em>Priority: {week['priority']}</em>
                </div>
                """,
                unsafe_allow_html=True
            )

# ===================== MAIN =====================

def main():
    if st.session_state.analyzed:
        display_results(st.session_state.results)
    else:
        display_hero()

if __name__ == "__main__":
    main()
