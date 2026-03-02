import os
from parser.resume_parser import parse_resume
from scoring.generic_scorer import score_candidate
from jd.jd_parser import parse_jd

RESUME_FOLDER = "data/resumes"
JD_FILE = "jd/new_jd.txt"


def rank_candidates():

    # ==============================
    # STEP 1 — Load & Parse JD
    # ==============================

    with open(JD_FILE, "r", encoding="utf-8") as f:
        jd_text = f.read()

    JD = parse_jd(jd_text)

    print("\n=========== CURRENT JD INFO ===========")
    print("Role:", JD["role"])
    print("Experience Range:", JD["min_exp"], "-", JD["max_exp"])
    print("Detected Skills:", JD["primary_skills"])
    print("=======================================\n")

    # ==============================
    # STEP 2 — Process Resumes
    # ==============================

    all_results = []

    files = [f for f in os.listdir(RESUME_FOLDER) if f.endswith(".pdf")]

    for file in files:
        path = os.path.join(RESUME_FOLDER, file)

        try:
            resume_data = parse_resume(path)

            score_data = score_candidate(
                resume_data["skills"],
                resume_data["experience"],
                JD
            )

            all_results.append({
                "file": file,
                "email": resume_data.get("email"),
                "score": score_data["final_score"],
                "details": score_data
            })

        except Exception as e:
            print(f"Error processing {file}: {e}")

    # ==============================
    # STEP 3 — Sort by Score
    # ==============================

    sorted_results = sorted(
        all_results,
        key=lambda x: x["score"],
        reverse=True
    )

    # ==============================
    # STEP 4 — Display Results
    # ==============================

    print("\n=========== RANKING RESULTS ===========\n")

    for r in sorted_results:

        print("File:", r["file"])
        print("Email:", r["email"])
        print("Experience (years):", r["details"]["experience_years"])
        print("Primary Matched:", r["details"]["primary_matched"])
        print("Secondary Matched:", r["details"]["secondary_matched"])
        print("Skill Score:", round(r["details"]["skill_score"], 3))
        print("Experience Score:", round(r["details"]["experience_score"], 3))
        print("Final Score:", round(r["score"], 3))
        print("Status:", r["details"]["status"])
        print("-" * 50)

    return sorted_results


if __name__ == "__main__":
    rank_candidates()