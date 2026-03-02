import json
from scoring.generic_scorer import score_candidate

TALENT_POOL_FILE = "data/talent_pool.json"


def quick_overlap(candidate_skills, jd):
    """
    Fast pre-filter using skill overlap.
    """

    jd_primary = set(jd.get("primary_skills", []))
    jd_secondary = set(jd.get("secondary_skills", []))

    candidate_set = set(candidate_skills)

    primary_overlap = len(candidate_set & jd_primary)
    total_overlap = len(candidate_set & (jd_primary | jd_secondary))

    # Hybrid filter rule
    return primary_overlap >= 1 or total_overlap >= 2


def rerank_registry(jd, min_results=5):
    """
    Hybrid reranking pipeline:
    1. Prefilter by skill overlap
    2. If too few candidates → fallback to full registry
    3. Score and rank
    """

    try:
        with open(TALENT_POOL_FILE, "r") as f:
            registry = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No candidate registry found.")
        return []

    # ---------- Stage 1: Prefilter ----------
    filtered = [
        candidate
        for candidate in registry
        if quick_overlap(candidate["skills"], jd)
    ]

    # ---------- Stage 2: Hybrid fallback ----------
    if len(filtered) < min_results:
        filtered = registry  # fallback to full registry

    # ---------- Stage 3: Full scoring ----------
    scored_results = []

    for candidate in filtered:
        score_data = score_candidate(
            candidate["skills"],
            candidate["experience"],
            jd
        )

        scored_results.append({
            "email": candidate["email"],
            "score": score_data["final_score"],
            "details": score_data
        })

    # ---------- Stage 4: Rank ----------
    ranked = sorted(
        scored_results,
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked