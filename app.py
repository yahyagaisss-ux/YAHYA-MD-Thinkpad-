import re
import PyPDF2
import streamlit as st

# --- Skill score function ---
def calculate_score(resume_text, skills):
    text = (resume_text or "").lower()
    score = 0
    matched = []
    for skill in skills:
        # word-boundary match, case-insensitive
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text):
            score += 1
            matched.append(skill)
    return round((score / len(skills)) * 100, 2) if skills else 0.0, matched

# --- Extract text from PDF ---
def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    except Exception as e:
        st.error(f"Couldn't read PDF: {e}")
    return text

st.title("Resume Screening Tool")

st.markdown("Upload a **PDF resume**, enter required skills, and get a match score.")

# You can enter skills manually (comma-separated)
skills_input = st.text_input(
    "Required skills (comma-separated):",
    value="python, django, flask, sql, aws, machine learning"
)

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if st.button("Evaluate"):
    if not uploaded_file:
        st.warning("Please upload a PDF resume.")
    else:
        required_skills = [s.strip() for s in skills_input.split(",") if s.strip()]
        resume_text = extract_text_from_pdf(uploaded_file)
        score, matched_skills = calculate_score(resume_text, required_skills)

        st.subheader("Results")
        st.write(f"**Match Score:** {score}%")
        st.write("**Matched Skills:** " + (", ".join(matched_skills) if matched_skills else "None"))

        st.subheader("Resume Preview (first 500 chars)")
        st.write(resume_text[:500] or "_No text extracted_")
