# NetSage AI Architecture

## 1. Overview

NetSage AI is an AI-assisted network troubleshooting helper for Cisco-style lab networks.

The system accepts a troubleshooting case containing:

- Network symptom
- Topology information
- Packet Tracer notes
- Cisco show-command outputs

It combines deterministic rule-based checks with AI-assisted diagnosis and requires human review before a recommended fix is accepted.

## 2. System Workflow

The NetSage AI workflow is:

1. Collect troubleshooting case.
2. Extract symptom, topology and command evidence.
3. Run deterministic Python rule checks.
4. Send structured case information to the AI diagnosis prompt.
5. Generate a structured diagnosis.
6. Compare AI diagnosis with known expected fault and rule-checker evidence.
7. Perform human review.
8. Mark the diagnosis as Accepted, Edited or Rejected.
9. Apply the approved fix.
10. Verify the network behaviour.
11. Record the result for dashboard analysis.

## 3. AI Diagnosis Output

The AI diagnosis uses structured fields:

- root_cause
- osi_layer
- confidence
- evidence
- next_command
- fix_steps

The AI must use evidence from the provided case rather than making unsupported assumptions.

## 4. Rule Checker

The deterministic Python checker validates common configuration problems.

The checker will include:

- Duplicate IP detection
- Wrong subnet mask detection
- Gateway mismatch detection
- Interface-down detection
- Missing VLAN detection
- Missing route detection

## 5. Human Review

Every AI diagnosis requires human review.

The reviewer can select:

- Accepted
- Edited
- Rejected

If an AI diagnosis is incorrect or incomplete, the reviewer records the correction and explains why.

## 6. Data Flow

Case Dataset
    ↓
Rule Checker + AI Diagnosis
    ↓
Evidence and Diagnosis
    ↓
Human Review
    ↓
Approved/Corrected Diagnosis
    ↓
Fix and Verification
    ↓
Dashboard and Responsible AI Log

## 7. Project Components

- `data/` - troubleshooting cases
- `prompts/` - AI prompt library
- `checker/` - deterministic Python validation
- `ai_diagnosis/` - AI diagnosis results
- `human_review/` - human review records
- `dashboard/` - dashboard and charts
- `demo/` - demonstration materials
- `docs/` - project documentation

## 8. Required Network Fault Categories

The dataset will cover:

- VLAN
- Gateway
- DHCP
- DNS
- Routing
- ACL
- NAT
- Wireless

At least 30 troubleshooting cases will be created.