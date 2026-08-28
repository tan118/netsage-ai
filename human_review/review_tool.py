import csv
import os


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "ai_diagnosis/diagnosis_results.csv"
OUTPUT_FILE = "human_review/responsible_ai_log.csv"


# ============================================================
# CREATE HUMAN REVIEW FILE
# ============================================================

def create_review_file():

    if not os.path.exists(INPUT_FILE):
        print("ERROR: AI diagnosis results were not found.")
        print(f"Expected file: {INPUT_FILE}")
        return

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)
        results = list(reader)


    if not results:
        print("ERROR: diagnosis_results.csv is empty.")
        return


    fieldnames = [
        "case_id",
        "ai_root_cause",
        "ai_osi_layer",
        "ai_confidence",
        "ai_evidence",
        "ai_next_command",
        "ai_fix_steps",
        "expected_fault",

        "human_decision",
        "human_correction",
        "reason_for_correction",
        "final_diagnosis",
        "verified"
    ]


    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()


        for result in results:

            writer.writerow({
                "case_id": result.get("case_id", ""),
                "ai_root_cause": result.get("root_cause", ""),
                "ai_osi_layer": result.get("osi_layer", ""),
                "ai_confidence": result.get("confidence", ""),
                "ai_evidence": result.get("evidence", ""),
                "ai_next_command": result.get("next_command", ""),
                "ai_fix_steps": result.get("fix_steps", ""),
                "expected_fault": result.get("expected_fault", ""),

                "human_decision": "",
                "human_correction": "",
                "reason_for_correction": "",
                "final_diagnosis": "",
                "verified": ""
            })


    print("\n==============================================")
    print("      HUMAN REVIEW FILE CREATED")
    print("==============================================")
    print(f"AI results read : {len(results)}")
    print(f"Review file     : {OUTPUT_FILE}")
    print("==============================================\n")


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":
    create_review_file()