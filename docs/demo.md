# NetSage AI — Demonstration Guide

## Demonstration Objective

The demonstration shows how NetSage AI assists with troubleshooting a
network configuration problem.

The demonstration follows one complete case from failure to verification.

---

## Demonstration Flow

    Broken Network
          |
          v
    Connectivity Test
          |
          v
    Cisco Evidence
          |
          v
    Rule Checker
          |
          v
    AI Diagnosis
          |
          v
    Human Review
          |
          v
    Configuration Fix
          |
          v
    Successful Connectivity

---

## Recommended Demonstration Case

NET-001 is used as the primary demonstration case.

### Problem

PC-A cannot communicate with PC-B even though the hosts are intended to
communicate within the same network.

### Evidence

The switch VLAN configuration shows that the two relevant interfaces are
assigned to different VLANs.

The expected fault is that the affected access interface is assigned to
the wrong VLAN.

---

## Step 1 — Show the Network

Open the NET-001 Packet Tracer topology.

Show:

- PC-A
- PC-B
- Switch
- Network connections
- IP configuration

---

## Step 2 — Demonstrate Failure

Perform a ping between the affected hosts.

Record the unsuccessful result.

---

## Step 3 — Collect Evidence

Use appropriate Cisco commands such as:

    show vlan brief

The output should be captured as project evidence.

---

## Step 4 — Run the Rule Checker

Run:

    python checker\rule_checker.py

Show the detected configuration issue.

---

## Step 5 — AI Diagnosis

Run the AI diagnosis pipeline when Gemini API quota is available.

The AI should provide:

- Root cause
- OSI layer
- Confidence
- Evidence
- Next command
- Fix steps
- Additional evidence
- Risk

---

## Step 6 — Human Review

The reviewer compares the AI recommendation with the actual evidence.

The reviewer records:

- Accepted
- Edited
- Rejected

The reviewer does not automatically accept the AI recommendation.

---

## Step 7 — Apply the Fix

Correct the affected switch interface VLAN assignment.

Example:

    configure terminal
    interface Fa0/2
    switchport mode access
    switchport access vlan 10
    end

---

## Step 8 — Verify

Repeat the connectivity test.

A successful ping demonstrates that the remediation restored connectivity.

---

## Step 9 — Dashboard

Open the NetSage AI dashboard:

    streamlit run dashboard\app.py

Show:

- Case count
- AI diagnosis count
- Confidence
- Human review
- Case categories
- Rule checker output
- Diagnosis table

---

## Suggested Video Structure

### 0:00–1:00
Introduce NetSage AI and the problem.

### 1:00–2:30
Show the Packet Tracer topology and failed ping.

### 2:30–4:00
Show Cisco evidence and deterministic rule checking.

### 4:00–6:00
Show AI diagnosis and explain the structured output.

### 6:00–7:30
Show human review and responsible-AI controls.

### 7:30–9:00
Apply the fix and demonstrate successful connectivity.

### 9:00–10:00
Show the dashboard and summarize results.

---

## Important Demonstration Principle

The demonstration should clearly show that NetSage AI is an
AI-assisted troubleshooting tool with human oversight.

The AI recommendation should not be presented as an automatically
executed network change.

Project Structure
netsage-ai/
│
├── ai_diagnosis/
│   ├── diagnose_case.py
│   ├── test_gemini.py
│   ├── diagnosis_results.csv
│   └── diagnosis_errors.csv
│
├── checker/
│   ├── rule_checker.py
│   └── sample_output.txt
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── cases.csv
│
├── demo/
│   └── ...
│
├── docs/
│   ├── methodology.md
│   ├── responsible_ai.md
│   └── demo.md
│
├── human_review/
│   ├── responsible_ai_log.csv
│   └── review_tool.py
│
├── prompts/
│   └── diagnose_prompt.md
│
├── .env
├── .gitignore
└── README.md

.env contains the local Gemini API key and must never be committed
to GitHub.

Problem Statement

Network troubleshooting often requires engineers to inspect several
Cisco command outputs and determine which configuration issue is causing
a connectivity failure.

NetSage AI organizes this process by combining deterministic network
checks with AI-assisted diagnosis.

The goal is not to replace network engineers, but to provide structured
evidence and recommendations that can be reviewed by a human.

Deterministic Rule Checker

The Python rule checker performs deterministic checks for:

Duplicate IP addresses
Incorrect subnet masks
Gateway mismatches
Interfaces that are down
Missing VLANs
Missing routes

Run it using:

python checker\rule_checker.py

The sample output is stored in:

checker/sample_output.txt
AI Diagnosis

The AI component uses the Google Gemini API.

The model receives:

Case ID
Category
Symptom
Topology information
Cisco show-command evidence
Expected fault for evaluation

The model produces structured output containing:

Root cause
OSI layer
Confidence
Evidence
Next command
Fix steps
Additional evidence required
Risk

The AI is instructed not to invent Cisco command output and to identify
when additional evidence is required.

Human Review

AI output is not automatically accepted.

The human reviewer records:

Accepted
Edited
Rejected

Corrections are recorded in:

human_review/responsible_ai_log.csv

This creates an auditable record of AI-assisted troubleshooting and
human oversight.

Dashboard

The dashboard is built using Streamlit.

Start it with:

streamlit run dashboard\app.py

The dashboard displays:

Total cases
AI diagnosis count
Confidence distribution
Case categories
Preliminary AI agreement
Human review decisions
Rule-checker output
AI diagnosis results
Setup
1. Create virtual environment
python -m venv venv

Activate it:

venv\Scripts\activate
2. Install dependencies
pip install -U google-genai python-dotenv pandas streamlit
3. Configure Gemini API key

Create a local .env file:

GEMINI_API_KEY=YOUR_API_KEY

Never commit this file to GitHub.

Running NetSage AI
Rule Checker
python checker\rule_checker.py
AI Diagnosis
python ai_diagnosis\diagnose_case.py

The AI diagnosis requires an available Gemini API quota.

Human Review File
python human_review\review_tool.py
Dashboard
streamlit run dashboard\app.py
Example Troubleshooting Workflow
Network Failure
      |
      v
Collect Cisco Evidence
      |
      v
Python Rule Checker
      |
      +------> Deterministic Finding
      |
      v
Gemini AI Diagnosis
      |
      v
Human Review
      |
      v
Apply Approved Fix
      |
      v
Verify Connectivity
Example Case
NET-001 — Wrong VLAN Assignment

Symptom:

PC-A cannot communicate with PC-B even though both hosts are intended
to communicate within the same network.

Evidence:

The relevant switch interfaces are assigned to different VLANs.

Expected fault:

The affected access interface is assigned to the wrong VLAN.

AI diagnosis:

The AI identifies the VLAN assignment as a Layer 2 problem and
recommends correcting the access VLAN.

Human review:

The reviewer checks that the diagnosis and evidence correspond to the
actual Packet Tracer configuration before accepting the remediation.

Responsible AI

NetSage AI follows several safety principles:

AI output is advisory.
Human review is required.
Evidence should be explicitly referenced.
The AI is instructed not to invent command output.
Confidence is reported.
API credentials are kept outside source code.
Network changes are not executed automatically.
Fixes should be verified after implementation.

More information is available in:

docs/responsible_ai.md
Limitations

The system has several limitations:

AI responses can be incorrect.
AI can misunderstand incomplete evidence.
API quota and availability can limit automated diagnosis.
The deterministic checker only detects implemented rules.
Packet Tracer is a simulation and does not represent every production
network environment.
Human verification is required before applying configuration changes.
Demonstration

The recommended demonstration uses NET-001.

The complete demonstration is:

Broken Packet Tracer Network
        ↓
Failed Ping
        ↓
Cisco Evidence
        ↓
Rule Checker
        ↓
AI Diagnosis
        ↓
Human Review
        ↓
Configuration Fix
        ↓
Successful Ping
        ↓
Dashboard

See:

docs/demo.md

for the complete demonstration procedure.

Technologies
Python
Google Gemini API
Google GenAI Python SDK
Streamlit
Pandas
Cisco Packet Tracer
Git
GitHub
Project Goal

NetSage AI demonstrates how deterministic network troubleshooting and
AI-assisted reasoning can be combined while maintaining human oversight.

The system prioritizes evidence, transparency, reviewability, and safe
remediation rather than autonomous network configuration.


Save it.

---

# NOW: Git checkpoint

Before we move on, run:

```cmd
git add .

Then:

git commit -m "Add project documentation and dashboard"

Then:

git push origin main