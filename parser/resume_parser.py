import re
import pdfplumber
from datetime import datetime
from utils.skill_list import SKILLS

import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)


def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text


def normalize_text(text):
    text = text.lower()
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


def extract_skills(text):
    found_skills = set()

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.add(skill)

    return list(found_skills)


def extract_experience(text):
    text = text.lower()
    current_year = datetime.now().year

    # Focus on work section
    if "work history" in text:
        text = text.split("work history", 1)[1]

        # Stop at education section if it exists
        if "education" in text:
            text = text.split("education", 1)[0]

    # Extract years from filtered text
    years = re.findall(r"20\d{2}", text)
    years = sorted(set(int(y) for y in years))

    if not years:
        return 0.0

    start_year = min(years)

    if "current" in text or "present" in text:
        end_year = current_year
    else:
        end_year = max(years)

    duration = end_year - start_year

    if 0 < duration <= 25:
        return duration

    # fallback explicit years
    explicit = re.findall(r"(\d+(\.\d+)?)\+?\s*(years|year|yrs)", text)
    if explicit:
        return float(explicit[0][0])

    return 0.0

def parse_resume(path):
    raw_text = extract_text_from_pdf(path)
    clean_text = normalize_text(raw_text)

    skills = extract_skills(clean_text)
    experience = extract_experience(clean_text)
    email = extract_email(clean_text)

    return {
        "email": email,
        "skills": skills,
        "experience": experience,
        "raw_text": clean_text,
        "length": len(clean_text)
    }

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if match:
        return match.group(0)
    return None