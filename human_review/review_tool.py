import csv
import os

INPUT_FILE = "ai_diagnosis/diagnosis_results.csv"
OUTPUT_FILE = "human_review/responsible_ai_log.csv"

reviews = {
    "NET-001": {
        "human_decision": "Corrected",
        "human_correction": "Confirmed Fa0/2 must be assigned to VLAN 10.",
        "reason_for_correction": "Compared AI diagnosis with the documented expected fault and available network evidence.",
        "final_diagnosis": "Fa0/2 is assigned to VLAN 20 instead of VLAN 10, causing Layer 2 connectivity failure."
    },
    "NET-002": {
        "human_decision": "Corrected",
        "human_correction": "Confirmed VLAN 20 must be allowed on the trunk interface.",
        "reason_for_correction": "Compared AI diagnosis with the documented expected fault and trunk evidence.",
        "final_diagnosis": "VLAN 20 is missing from the trunk allowed VLAN list, preventing VLAN 20 traffic from crossing the trunk."
    },
    "NET-003": {
        "human_decision": "Corrected",
        "human_correction": "Confirmed that inter-VLAN routing is missing between VLAN 10 and VLAN 20.",
        "reason_for_correction": "Compared AI diagnosis with the documented expected fault and Layer 3 evidence.",
        "final_diagnosis": "No Layer 3 inter-VLAN routing mechanism is configured to route traffic between VLAN 10 and VLAN 20."
    },
    "NET-004": {
        "human_decision": "Corrected",
        "human_correction": "Confirmed the native VLAN must match on both sides of the EtherChannel trunk.",
        "reason_for_correction": "Compared AI diagnosis with the documented expected fault and EtherChannel/trunk evidence.",
        "final_diagnosis": "The EtherChannel trunk has a native VLAN mismatch between the two switch peers."
    },
    "NET-005": {
        "human_decision": "Corrected",
        "human_correction": "Confirmed the PC default gateway must be changed to 192.168.10.1.",
        "reason_for_correction": "Compared AI diagnosis with the documented expected fault and router interface evidence.",
        "final_diagnosis": "The PC is configured with an incorrect default gateway of 192.168.10.254 instead of 192.168.10.1."
    }
}


def main():
    if not os.path.exists(INPUT_FILE):
        print("ERROR: AI results file not found:")
        print(INPUT_FILE)
        return

    os.makedirs("human_review", exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("ERROR: No AI results found.")
        return

    output_rows = []

    for row in rows:
        case_id = row.get("case_id", "")

        row["human_decision"] = ""
        row["human_correction"] = ""
        row["reason_for_correction"] = ""
        row["final_diagnosis"] = ""

        if case_id in reviews:
            review = reviews[case_id]

            row["human_decision"] = review["human_decision"]
            row["human_correction"] = review["human_correction"]
            row["reason_for_correction"] = review["reason_for_correction"]
            row["final_diagnosis"] = review["final_diagnosis"]

        output_rows.append(row)

    fieldnames = list(output_rows[0].keys())

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(output_rows)

    reviewed = sum(
        1 for row in output_rows
        if row.get("human_decision") == "Corrected"
    )

    print()
    print("=" * 50)
    print("       HUMAN REVIEW FILE CREATED")
    print("=" * 50)
    print(f"AI results read : {len(rows)}")
    print(f"Human reviewed  : {reviewed}")
    print(f"Review file     : {OUTPUT_FILE}")
    print("=" * 50)


if __name__ == "__main__":
    main()