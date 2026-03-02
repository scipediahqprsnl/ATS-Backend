def score_candidate(skills, experience_years, jd):
    """
    Generic scoring engine.
    Works for any JD parsed dynamically.
    """

    # ==============================
    # 1️⃣ Extract JD Data (No Defaults)
    # ==============================

    min_exp = jd["min_exp"]
    max_exp = jd["max_exp"]

    primary_required = jd["primary_skills"]
    secondary_required = jd.get("secondary_skills", [])

    # ==============================
    # 2️⃣ Skill Matching
    # ==============================

    primary_matched = [
        skill for skill in primary_required if skill in skills
    ]

    secondary_matched = [
        skill for skill in secondary_required if skill in skills
    ]

    # Skill score calculation
    if len(primary_required) > 0:
        primary_score = len(primary_matched) / len(primary_required)
    else:
        primary_score = 0

    if len(secondary_required) > 0:
        secondary_score = len(secondary_matched) / len(secondary_required)
    else:
        secondary_score = 0

    # Weighted skill score
    skill_score = (0.7 * primary_score) + (0.3 * secondary_score)

 # ==============================
# 3️⃣ Experience Scoring
# ==============================

    if min_exp <= experience_years <= max_exp:
        experience_score = 1.0

    elif experience_years > max_exp:
        gap = experience_years - max_exp

        if gap <= 2:
            experience_score = 0.6
        elif gap <= 5:
            experience_score = 0.4
        else:
            experience_score = 0.1   # heavy overqualification penalty
    else:
        # Underqualified
        if max_exp > 0:
            experience_score = experience_years / max_exp
        else:
            experience_score = 0

# ==============================
# 4️⃣ Final Score (Rebalanced Weights)
# ==============================

    final_score = (0.65 * skill_score) + (0.35 * experience_score)

# Hard suppression for extreme overqualification
    if experience_years > max_exp + 5:
        final_score *= 0.7

    # ==============================
    # 5️⃣ Status Assignment
    # ==============================

    if final_score >= 0.7:
        status = "SHORTLIST"
    elif final_score >= 0.45:
        status = "REVIEW"
    else:
        status = "TALENT_POOL"

    return {
        "primary_matched": primary_matched,
        "secondary_matched": secondary_matched,
        "skill_score": round(skill_score, 3),
        "experience_score": round(experience_score, 3),
        "final_score": round(final_score, 3),
        "experience_years": experience_years,
        "status": status
    }