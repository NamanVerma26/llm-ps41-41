
import os
import json
import streamlit as st

from io import BytesIO
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai
from google.genai import types


# ---------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# ---------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            attempts=4,
            initial_delay=1.0,
            max_delay=8.0,
            exp_base=2.0,
            http_status_codes=[408, 429, 500, 502, 503, 504]
        )
    )
)

MODEL_NAME = "gemini-3.5-flash-lite"


# ---------------------------------
# 2. EXTRACT TEXT FROM RESUME PDF
# ---------------------------------

def extract_resume_text(pdf_file):

    try:
        pdf_reader = PdfReader(BytesIO(pdf_file.getvalue()))

        extracted_text = ""

        for page in pdf_reader.pages:
            extracted_text += page.extract_text() or ""
            extracted_text += "\n"

        if not extracted_text.strip():
            raise ValueError(
                "No readable text found in this PDF. "
                "It may be a scanned document."
            )

        return extracted_text

    except Exception as e:
        raise ValueError(f"PDF extraction failed: {e}")


# ---------------------------------
# 3. ANALYZE RESUME USING GEMINI
# ---------------------------------

def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an expert resume analyzer and career assistant.

Compare the candidate's resume with the given job description.

Analyze only the information provided.

Return valid JSON using exactly this structure:

{{
    "match_score": 75,
    "matched_skills": [
        "Python",
        "SQL"
    ],
    "missing_skills": [
        "Power BI",
        "Tableau"
    ],
    "improvement_tips": [
        "Tip 1",
        "Tip 2",
        "Tip 3"
    ]
}}

Rules:

1. Match score must be an integer from 0 to 100.
2. Identify skills genuinely present in the resume.
3. Identify important job requirements missing from the resume.
4. Give exactly three practical improvement tips.
5. Never invent qualifications or experience.
6. Do not treat missing information as proof that
   the candidate lacks a skill.
7. Return JSON only, without Markdown formatting.

RESUME:
{resume_text[:20000]}

JOB DESCRIPTION:
{job_description[:10000]}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        result = json.loads(response.text)

        # Validate the returned data
        score = result["match_score"]

        if not isinstance(score, int) or not 0 <= score <= 100:
            raise ValueError("Invalid match score returned by Gemini.")

        if len(result["improvement_tips"]) != 3:
            raise ValueError("Gemini did not return exactly three tips.")

        return result

    except Exception as e:
        raise RuntimeError(f"Resume analysis failed: {e}")


# ---------------------------------
# 4. STREAMLIT USER INTERFACE
# ---------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and paste a job description "
    "to analyze how well your resume matches the job."
)

st.divider()

# Resume upload
uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

# Job description input
job_description = st.text_area(
    "Paste Job Description",
    height=200,
    placeholder="Paste the complete job description here..."
)

# Analyze button
if st.button("Analyze My Resume", type="primary"):

    if uploaded_file is None:
        st.warning("Please upload your resume PDF.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:

        try:
            with st.spinner("Extracting resume and analyzing..."):

                resume_text = extract_resume_text(uploaded_file)
                with st.expander("View Extracted Resume Text"):
                     st.write(resume_text)

                     st.caption(
                        f"Total characters extracted: {len(resume_text)}"
                        )
                result = analyze_resume(
                    resume_text,
                    job_description
                )

            st.success("Resume analysis completed!")

            st.divider()

            # Match score
            st.subheader("Resume Match Score")

            score = result["match_score"]

            st.progress(score / 100)

            st.metric("Match Score", f"{score}%")

            # Matched skills
            st.subheader("✅ Matched Skills")

            if result["matched_skills"]:
                for skill in result["matched_skills"]:
                    st.write(f"• {skill}")
            else:
                st.write("No matched skills identified.")

            # Missing skills
            st.subheader("❌ Missing Skills")

            if result["missing_skills"]:
                for skill in result["missing_skills"]:
                    st.write(f"• {skill}")
            else:
                st.write("No missing skills identified.")

            # Improvement tips
            st.subheader("💡 Three Improvement Tips")

            for index, tip in enumerate(
                result["improvement_tips"], start=1
            ):
                st.write(f"{index}. {tip}")

            # Download analysis
            st.download_button(
                label="Download Analysis (JSON)",
                data=json.dumps(result, indent=4),
                file_name="resume_analysis.json",
                mime="application/json"
            )

        except Exception as e:
            error_message = str(e)

            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                st.error(
                    "Gemini API daily quota has been exhausted. "
                    "Please check your API usage or try again after the quota resets."
                )

            elif "503" in error_message or "UNAVAILABLE" in error_message:
                st.error(
                    "Gemini is temporarily experiencing high demand. "
                    "Please try again later."
                )

            else:
                st.error(f"An error occurred: {error_message}")
