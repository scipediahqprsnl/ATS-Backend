import re
from utils.skill_list import SKILLS


def normalize_text(text):
    text = text.lower()
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


def extract_experience_range(text):
    """
    Extract min and max experience from JD text.
    Handles:
    - 0–3 years
    - 1 – 3 years
    - Fresher / 6 months – 1 year
    - Fresher
    """

    text = text.lower()

    # Pattern: 0–3 years OR 1 - 3 years
    match = re.search(r"(\d+)\s*[–-]\s*(\d+)\s*years", text)
    if match:
        return int(match.group(1)), int(match.group(2))

    # Pattern: 6 months – 1 year
    match = re.search(r"(\d+)\s*months?\s*[–-]\s*(\d+)\s*year", text)
    if match:
        min_exp = int(match.group(1)) / 12
        max_exp = int(match.group(2))
        return round(min_exp, 2), max_exp

    # Fresher
    if "fresher" in text:
        return 0, 1

    return 0, 3  # safe default


def extract_skills_from_jd(text):
    """
    Detect relevant skills from JD using global SKILLS list.
    """
    detected = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            detected.append(skill)

    return detected


def extract_role_name(text):
    """
    Extract first role title (simple heuristic).
    """
    lines = text.split("\n")
    for line in lines:
        if len(line.strip()) > 3 and len(line.strip()) < 60:
            return line.strip()
    return "Unknown Role"


def parse_jd(raw_text):
    clean_text = normalize_text(raw_text)

    role = extract_role_name(raw_text)
    min_exp, max_exp = extract_experience_range(clean_text)
    skills = extract_skills_from_jd(clean_text)

    return {
        "role": role,
        "primary_skills": skills,
        "secondary_skills": [],
        "min_exp": min_exp,
        "max_exp": max_exp
    }