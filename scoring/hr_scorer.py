PRIMARY_HR_SKILLS = [
    "recruitment",
    "talent acquisition",
    "resume screening",
    "interview scheduling",
    "candidate communication",
    "job posting"
]

SECONDARY_HR_SKILLS = [
    "hr operations",
    "employee engagement",
    "onboarding",
    "compliance",
    "tracking"
]


def compute_experience_score(years):
    """
    Experience scoring for INTERN role
    """

    if years <= 1:
        return 1.0
    elif years <= 2:
        return 0.7
    elif years <= 4:
        return 0.4
    else:
        return 0.2


def score_hr_candidate(matched_skills, experience_years):

    primary_skills = [
        "recruitment",
        "talent acquisition",
        "resume screening",
        "candidate communication",
        "job posting"
    ]

    secondary_skills = [
        "onboarding",
        "employee engagement",
        "hr operations",
        "compliance",
        "tracking",
        "interview scheduling"
    ]

    primary_matched = [s for s in matched_skills if s in primary_skills]
    secondary_matched = [s for s in matched_skills if s in secondary_skills]

    primary_score = len(primary_matched) / len(primary_skills)
    secondary_score = len(secondary_matched) / len(secondary_skills)

    skill_score = (primary_score * 0.7) + (secondary_score * 0.3)

    experience_score = compute_experience_score(experience_years)

    final_score = (skill_score * 0.75) + (experience_score * 0.25)

    # 🔥 Overqualification penalty
    if experience_years > 6:
        final_score *= 0.8

    # 🔥 Decision Layer
    if final_score >= 0.6:
        status = "SHORTLIST"
    elif final_score >= 0.4:
        status = "REVIEW"
    else:
        status = "TALENT_POOL"

    return {
        "primary_matched": primary_matched,
        "secondary_matched": secondary_matched,
        "skill_score": round(skill_score, 3),
        "experience_years": experience_years,
        "experience_score": experience_score,
        "final_score": round(final_score, 3),
        "status": status
    }

def compute_experience_score(years):
    if years == 0:
        return 0.8
    elif years <= 2:
        return 0.7
    elif years <= 4:
        return 0.4
    else:
        return 0.2
