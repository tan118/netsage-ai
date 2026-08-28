# NetSage AI — Demonstration Guide

## 1. Demonstration Objective

The demonstration shows how NetSage AI assists with troubleshooting a
Cisco network configuration problem.

The demonstration follows one complete troubleshooting case from failure
to diagnosis, human review, remediation, and verification.

---

## 2. Demonstration Workflow

```text
Broken Network
      |
      v
Connectivity Test
      |
      v
Cisco Evidence
      |
      v
Deterministic Rule Checker
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
Connectivity Verification
      |
      v
Dashboard
3. Recommended Demonstration Case
NET-001 — Wrong VLAN Assignment

NET-001 is used as the primary end-to-end demonstration case.

The case represents a Layer 2 connectivity problem caused by an incorrect
VLAN assignment on a switch access interface.

4. Step 1 — Show the Network

Open the NET-001 Cisco Packet Tracer topology.

Show:

PC-A
PC-B
Switch
Network connections
IP configuration
Relevant switch interfaces
5. Step 2 — Demonstrate the Failure

Perform a ping between the affected hosts.

Record the unsuccessful connectivity result.

This establishes the initial network failure before troubleshooting.

6. Step 3 — Collect Cisco Evidence

Use an appropriate Cisco command such as:

show vlan brief

Capture the output showing the VLAN assignments.

The evidence should be saved as a screenshot for the project demo.

7. Step 4 — Run the Rule Checker

From the project root, run:

python checker\rule_checker.py

Show the deterministic troubleshooting result.

The rule checker provides a non-AI baseline for identifying configuration
problems.

8. Step 5 — AI Diagnosis

When Gemini API quota is available, run:

python ai_diagnosis\diagnose_case.py

The AI diagnosis provides:

Root cause
OSI layer
Confidence
Evidence
Next diagnostic command
Fix steps
Additional evidence required
Risk

The AI output is treated as a recommendation rather than an automatic
decision.

9. Step 6 — Human Review

Open:

human_review\responsible_ai_log.csv

The reviewer compares the AI diagnosis against the actual Cisco evidence.

The reviewer records one of:

Accepted
Edited
Rejected

If the AI diagnosis contains an unsupported claim or requires correction,
the reviewer records the correction and the reason.

10. Step 7 — Apply the Fix

For NET-001, the affected switch interface can be corrected using the
appropriate Cisco configuration.

Example:

configure terminal
interface Fa0/2
switchport mode access
switchport access vlan 10
end

The configuration should only be applied after human review.

11. Step 8 — Verify the Fix

Repeat the connectivity test.

A successful ping demonstrates that the configuration change restored
connectivity.

Capture the successful ping as evidence.

12. Step 9 — Dashboard

Start the dashboard using:

streamlit run dashboard\app.py

The dashboard presents:

Total cases
AI diagnosis count
Confidence distribution
Case categories
AI agreement
Human review decisions
Rule-checker output
AI diagnosis results
13. Suggested Demonstration Recording
Part 1 — Introduction

Briefly explain:

NetSage AI is an AI-assisted Cisco network troubleshooting system
combining deterministic checks, AI diagnosis, and human review.

Part 2 — Network Failure

Show the Packet Tracer topology and unsuccessful ping.

Part 3 — Evidence

Show the Cisco command output that demonstrates the configuration issue.

Part 4 — Rule Checker

Run the Python rule checker and show its finding.

Part 5 — AI Diagnosis

Show the structured AI diagnosis.

Part 6 — Human Review

Show how the reviewer evaluates the AI recommendation.

Part 7 — Remediation

Apply the reviewed configuration fix.

Part 8 — Verification

Show the successful ping.

Part 9 — Dashboard

Open the Streamlit dashboard and explain the displayed results.