
# Resume Analyzer – Problem Statement 41

**MIT ADT University**  
**Department of Computer Science and Engineering**

## 1. Project Overview

Resume Analyzer is a Generative AI-based application that compares a candidate's resume with a given job description. It helps job seekers understand how well their resume matches a particular job role and identifies missing skills and areas for improvement.

The application uses Google's Gemini API to analyze resume content and generate structured feedback.

## 2. Features

- Upload a resume in PDF format.
- Extract text from the uploaded PDF.
- Enter a job description.
- Generate an AI-based resume match score (0–100).
- Identify matched skills.
- Identify missing skills.
- Generate three practical improvement tips.
- Display results using an interactive Streamlit interface.
- Download analysis results in JSON format.
- Preview extracted resume text.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | User interface |
| Google Gemini API | AI-powered resume analysis |
| PyPDF | Extracting text from PDF resumes |
| python-dotenv | Managing environment variables |

## 4. Project Workflow

1. The user uploads a resume in PDF format.
2. The application extracts text from the PDF.
3. The user enters a job description.
4. Resume text and job description are sent to the Gemini API.
5. Gemini analyzes the information and returns structured JSON.
6. The application displays the match score, matched skills, missing skills, and improvement tips.
7. The user can download the analysis results.

## 5. Installation and Setup

### Prerequisites

- Python installed on your system.
- A Google Gemini API key.

### Step 1: Clone the repository

```bash
git clone https://github.com/NamanVerma26/llm-ps41-41.git
cd llm-ps41-41
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure the API key

Create a `.env` file in the project directory and add your Gemini API key.

```text
GEMINI_API_KEY=your_api_key_here
```

Use the exact environment variable name expected by `app.py`. Never upload your actual API key to GitHub.

### Step 4: Run the application

```bash
streamlit run app.py
```

The application will open in your web browser.

## 6. Project Structure

```text
llm-ps41-41/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── Screenshots/
    ├── Screenshot 1.png
    ├── Screenshot 2.png
    ├── Screenshot 3.png
    └── Screenshot 4.png
```

## 7. Limitations

- The application supports text-based PDF resumes.
- Scanned PDFs without a readable text layer are not supported.
- Analysis depends on Gemini API availability and usage limits.
- The match score is an AI-generated estimate, not a guarantee of job selection.

## 8. Conclusion

The Resume Analyzer demonstrates how Generative AI can assist job seekers in evaluating resumes against job descriptions. It provides a match score, identifies relevant and missing skills, and offers practical suggestions for improvement.

## 9. GitHub Repository

https://github.com/NamanVerma26/llm-ps41-41
