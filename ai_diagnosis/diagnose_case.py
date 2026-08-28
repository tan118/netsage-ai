import os
import json
import csv
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Check your .env file."
    )

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.6-flash"

INPUT_FILE = "data/cases.csv"
OUTPUT_FILE = "ai_diagnosis/diagnosis_results.csv"
ERROR_FILE = "ai_diagnosis/diagnosis_errors.csv"

DELAY_SECONDS = 3
MAX_RETRIES = 3


# ============================================================
# AI DIAGNOSIS
# ============================================================

def diagnose_case(case):

    prompt = f"""
You are NetSage AI, an AI-assisted Cisco network troubleshooting
assistant.

A human network engineer MUST review your diagnosis before accepting
or applying any fix.

Analyze the troubleshooting case below.

------------------------------------------------------------
CASE INFORMATION
------------------------------------------------------------

CASE ID:
{case["case_id"]}

CATEGORY:
{case["category"]}

SYMPTOM:
{case["symptom"]}

TOPOLOGY:
{case["topology_note"]}

SHOW-COMMAND EVIDENCE:
{case["show_outputs"]}

KNOWN EXPECTED FAULT:
{case["expected_fault"]}

------------------------------------------------------------
DIAGNOSIS RULES
------------------------------------------------------------

1. Analyze the evidence carefully.

2. Identify the most likely root cause.

3. Identify the relevant OSI layer.

4. Assign exactly one confidence level:
   High, Medium, or Low.

5. Reference ONLY evidence actually supplied in the case.

6. Do NOT claim that a command output was provided if it was not.

7. If you recommend a command that was not already provided,
   clearly treat it as a NEXT diagnostic command rather than evidence.

8. Recommend the next Cisco diagnostic command.

9. Provide practical and technically appropriate fix steps.

10. Do not invent show-command output.

11. Do not blindly copy the expected fault.

12. If the supplied evidence is insufficient, say so.

13. Do not add unnecessary commands.

14. The diagnosis is a recommendation only and requires human review.

15. Prefer the simplest diagnosis directly supported by the evidence.

------------------------------------------------------------
OUTPUT
------------------------------------------------------------

Return ONLY valid JSON with these fields:

{{
    "case_id": "",
    "root_cause": "",
    "osi_layer": "",
    "confidence": "",
    "evidence": [],
    "next_command": "",
    "fix_steps": [],
    "additional_evidence_needed": "",
    "risk": ""
}}
"""

    schema = {
        "type": "object",
        "properties": {
            "case_id": {"type": "string"},
            "root_cause": {"type": "string"},
            "osi_layer": {"type": "string"},
            "confidence": {"type": "string"},
            "evidence": {
                "type": "array",
                "items": {"type": "string"}
            },
            "next_command": {"type": "string"},
            "fix_steps": {
                "type": "array",
                "items": {"type": "string"}
            },
            "additional_evidence_needed": {"type": "string"},
            "risk": {"type": "string"}
        },
        "required": [
            "case_id",
            "root_cause",
            "osi_layer",
            "confidence",
            "evidence",
            "next_command",
            "fix_steps",
            "additional_evidence_needed",
            "risk"
        ]
    }

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema
        )
    )

    return json.loads(response.text)


# ============================================================
# PRELIMINARY AGREEMENT CHECK
# ============================================================

def calculate_initial_agreement(expected_fault, ai_root_cause):

    expected = expected_fault.lower().strip()
    actual = ai_root_cause.lower().strip()

    if expected in actual:
        return "Yes"

    return "Needs Review"


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(results):

    fieldnames = [
        "case_id",
        "root_cause",
        "osi_layer",
        "confidence",
        "evidence",
        "next_command",
        "fix_steps",
        "additional_evidence_needed",
        "risk",
        "expected_fault",
        "ai_agreement"
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

            row = result.copy()

            row["evidence"] = " | ".join(
                result.get("evidence", [])
            )

            row["fix_steps"] = " | ".join(
                result.get("fix_steps", [])
            )

            writer.writerow(row)


# ============================================================
# SAVE ERRORS
# ============================================================

def save_errors(errors):

    fieldnames = [
        "case_id",
        "error_type",
        "error_message"
    ]

    with open(
        ERROR_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for error in errors:
            writer.writerow(error)


# ============================================================
# PROCESS ONE CASE WITH RETRIES
# ============================================================

def process_case(case):

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            result = diagnose_case(case)

            result["case_id"] = case["case_id"]

            result["expected_fault"] = (
                case["expected_fault"]
            )

            result["ai_agreement"] = (
                calculate_initial_agreement(
                    case["expected_fault"],
                    result["root_cause"]
                )
            )

            return result

        except Exception as error:

            last_error = error

            print(
                f"       Attempt {attempt}/{MAX_RETRIES} failed:"
            )
            print(
                f"       {type(error).__name__}: {error}"
            )

            if attempt < MAX_RETRIES:

                wait_time = attempt * 5

                print(
                    f"       Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

    raise last_error


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n==============================================")
    print("          NETSAGE AI DIAGNOSIS")
    print("==============================================")
    print(f"Input : {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print("==============================================\n")


    # --------------------------------------------------------
    # READ CASES
    # --------------------------------------------------------

    try:

        with open(
            INPUT_FILE,
            "r",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)
            cases = list(reader)

    except Exception as error:

        print("ERROR: Could not read cases.csv.")
        print(f"{type(error).__name__}: {error}")
        return


    if not cases:

        print("ERROR: cases.csv contains no cases.")
        return


    print(f"Total cases found: {len(cases)}\n")


    # --------------------------------------------------------
    # PROCESS CASES
    # --------------------------------------------------------

    results = []
    errors = []


    for index, case in enumerate(cases, start=1):

        case_id = case["case_id"]

        print(
            f"[{index}/{len(cases)}] "
            f"Processing {case_id}..."
        )

        try:

            result = process_case(case)

            results.append(result)

            print("       ✓ Diagnosis received")

        except Exception as error:

            print("       ✗ Case failed after retries")

            errors.append({
                "case_id": case_id,
                "error_type": type(error).__name__,
                "error_message": str(error)
            })


        # ----------------------------------------------------
        # Save after EVERY case
        # ----------------------------------------------------

        save_results(results)
        save_errors(errors)


        # ----------------------------------------------------
        # Delay before next case
        # ----------------------------------------------------

        if index < len(cases):

            time.sleep(DELAY_SECONDS)


    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    successful = len(results)
    failed = len(errors)

    print("\n==============================================")
    print("       NETSAGE AI DIAGNOSIS COMPLETE")
    print("==============================================")
    print(f"Cases found     : {len(cases)}")
    print(f"Processed       : {successful}")
    print(f"Failed          : {failed}")
    print(f"Results saved   : {OUTPUT_FILE}")
    print(f"Errors saved    : {ERROR_FILE}")
    print("==============================================\n")


if __name__ == "__main__":
    main()