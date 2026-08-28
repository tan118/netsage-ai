# NetSage AI — Methodology

## 1. Project Overview

NetSage AI is an AI-assisted Cisco network troubleshooting system designed
to help identify common network configuration problems.

The system combines:

1. A structured troubleshooting case dataset
2. Deterministic Python-based network checks
3. AI-assisted diagnosis using the Gemini API
4. Human review of AI recommendations
5. A dashboard for presenting results

The system is designed as a decision-support tool rather than an autonomous
network configuration system.

---

## 2. Problem Definition

Network troubleshooting often requires engineers to inspect multiple
configuration outputs and determine whether the observed symptoms are
consistent with a configuration problem.

NetSage AI attempts to reduce this effort by organizing troubleshooting
evidence and providing a structured diagnosis containing:

- Root cause
- OSI layer
- Confidence
- Evidence
- Next diagnostic command
- Fix steps
- Additional evidence required
- Risk

---

## 3. Dataset

The project contains a structured collection of network troubleshooting
cases.

Each case contains information such as:

- Case ID
- Category
- Symptom
- Topology information
- Cisco show-command evidence
- Expected fault
- OSI layer
- Networking concept
- Severity

The cases cover common networking problems including VLANs, routing,
gateway configuration, interfaces, DNS, DHCP, ACLs and related
configuration issues.

Packet Tracer cases are used to demonstrate realistic network symptoms,
configuration evidence and successful remediation.

---

## 4. System Workflow

The overall workflow is:

    Troubleshooting Case
            |
            v
    Network Evidence
            |
            +----------------------+
            |                      |
            v                      v
    Deterministic Rules       AI Diagnosis
            |                      |
            +----------+-----------+
                       |
                       v
                 Human Review
                       |
                       v
                Final Decision
                       |
                       v
                 Dashboard

---

## 5. Deterministic Rule Checker

The Python rule checker performs basic deterministic checks.

The implemented checks include:

1. Duplicate IP addresses
2. Invalid or incorrect subnet masks
3. Gateway mismatches
4. Interfaces that are down
5. Missing VLANs
6. Missing routes

These checks are deterministic and do not depend on an AI model.

This provides a baseline against which AI-assisted diagnosis can be
compared.

---

## 6. AI Diagnosis

The AI diagnosis component uses the Google Gemini API.

The model receives structured case information including:

- Network symptom
- Topology information
- Cisco command evidence
- Expected fault information for evaluation

The model is instructed to:

- Analyze the supplied evidence
- Avoid inventing command output
- Identify the likely root cause
- Identify the OSI layer
- Report confidence
- Reference supplied evidence
- Recommend a next diagnostic command
- Provide fix steps
- Identify additional evidence when required

The response is constrained to a structured JSON format.

---

## 7. Human Review

AI output is not treated as automatically correct.

Human review records whether a diagnosis is:

- Accepted
- Edited
- Rejected

When an AI diagnosis requires correction, the reviewer records:

- What was corrected
- Why the correction was necessary
- The final diagnosis
- Whether the final result was verified

This allows the project to evaluate the usefulness and limitations of
AI-assisted troubleshooting.

---

## 8. Evidence-Based Evaluation

AI diagnoses are compared with the known expected fault for each case.

Evaluation considers:

- Root-cause correctness
- Appropriate OSI layer
- Evidence usage
- Diagnostic command quality
- Fix quality
- Confidence appropriateness

Human review is treated as the final decision layer.

---

## 9. Dashboard

The dashboard presents project results including:

- Total cases
- AI diagnoses available
- Confidence distribution
- Case categories
- Preliminary AI agreement
- Human review decisions
- Rule-checker output
- AI diagnosis records

The dashboard is implemented using Streamlit.

---

## 10. Limitations

NetSage AI has several limitations:

- AI responses may occasionally be incorrect.
- AI may interpret incomplete evidence incorrectly.
- API availability and quota limits can affect automated diagnosis.
- Deterministic checks only cover the rules implemented in the checker.
- Packet Tracer does not represent every production networking environment.
- Human verification remains necessary before applying network changes.

---

## 11. Reproducibility

The project can be reproduced by:

1. Creating a Python virtual environment
2. Installing the dependencies
3. Configuring the Gemini API key through `.env`
4. Running the deterministic checker
5. Running the AI diagnosis script when API quota is available
6. Running the dashboard

API credentials must never be committed to the GitHub repository.