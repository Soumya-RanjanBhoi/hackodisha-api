
import pdfplumber
import docx
import regex as re

def extract_text_from_pdf(file):

    text=""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_all_skills(text):
    pattern = r"(?:TECHNICAL SKILLS|SKILLS|TOOLS|TECHNOLOGIES|SOFT SKILLS|DOMAINS)\s*[:\-]?\s*(.*?)(?:\n[A-Z][A-Za-z\s]*[:\-]|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    
    if not match:
        return None

    skills_text = match.group(1)

    skills_text = re.sub(r"\n\s*", " ", skills_text)

    skills = re.split(r"[,;:/]", skills_text)
    
    skills = [s.strip() for s in skills if s.strip()]

    return skills if skills else None
