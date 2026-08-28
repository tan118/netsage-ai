# NetSage AI — Responsible AI

## 1. Purpose

NetSage AI is intended to assist network troubleshooting rather than
replace the judgement of a network engineer.

The AI provides recommendations based on supplied network evidence.

A human reviewer remains responsible for deciding whether the diagnosis
and proposed fix are appropriate.

---

## 2. Human Oversight

Every AI diagnosis is intended to be reviewed by a human.

The review categories are:

- Accepted
- Edited
- Rejected

An accepted diagnosis is considered sufficiently correct and supported
by the available evidence.

An edited diagnosis contains useful information but requires correction
or clarification.

A rejected diagnosis is considered unsuitable for the case.

---

## 3. Evidence Grounding

The AI prompt instructs the model to use only evidence supplied in the
case.

The model is explicitly instructed not to invent Cisco command output.

Evidence may include:

- `show vlan brief`
- `show interfaces trunk`
- `show ip interface brief`
- `show ip route`
- Interface information
- Addressing information
- Topology information

If evidence is insufficient, the model is instructed to identify the
additional evidence required.

---

## 4. Confidence

The AI reports:

- High
- Medium
- Low

Confidence does not mean that the diagnosis is guaranteed to be correct.

Confidence is treated as an indicator of how strongly the available
evidence supports the diagnosis.

---

## 5. Safe Fix Recommendations

The AI is instructed to provide diagnostic commands and fix steps.

Network configuration changes should not be applied automatically.

A human should:

1. Review the diagnosis.
2. Review the evidence.
3. Confirm the proposed command.
4. Apply the change in an appropriate environment.
5. Verify the result.

---

## 6. API Security

The Gemini API key is stored in a local `.env` file.

The `.env` file is excluded from Git using `.gitignore`.

The API key must never be placed directly inside Python source code or
committed to GitHub.

---

## 7. Known Limitations

AI-generated troubleshooting can contain:

- Incorrect conclusions
- Unsupported assumptions
- Incomplete fixes
- Overconfident responses
- Incorrect interpretation of evidence

For this reason, NetSage AI does not perform autonomous network changes.

---

## 8. Human Correction

Human corrections are recorded in:

`human_review/responsible_ai_log.csv`

The record includes:

- AI diagnosis
- Expected fault
- Human decision
- Correction
- Reason for correction
- Final diagnosis
- Verification status

This provides an auditable record of human oversight.

---

## 9. Responsible Use

NetSage AI should be used as a troubleshooting assistant.

It should not be used as an unrestricted autonomous network administration
system.

Production configuration changes should always be validated by a
qualified network administrator.