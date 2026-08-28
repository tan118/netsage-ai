# NetSage AI

## AI-Assisted Cisco Network Troubleshooting Assistant

NetSage AI is an AI-assisted network troubleshooting system that combines
deterministic configuration checks, structured network evidence, AI-based
diagnosis, human review, and an interactive dashboard.

The system is designed to help identify common Cisco networking problems
while keeping a human engineer responsible for the final decision.

---

# Features

- Structured network troubleshooting case dataset
- Cisco Packet Tracer troubleshooting cases
- Python deterministic rule checker
- Gemini-powered AI diagnosis
- Structured JSON AI output
- Confidence estimation
- Evidence-based diagnosis
- Recommended diagnostic commands
- Suggested remediation steps
- Human review workflow
- Responsible AI logging
- Streamlit dashboard
- Git-based project versioning

---

# System Architecture

```text
                    NetSage AI
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
       Dataset     Rule Checker    Gemini AI
          |             |             |
          |             |             v
          |             |       AI Diagnosis
          |             |             |
          +-------------+-------------+
                        |
                        v
                  Human Review
                        |
                        v
                 Final Diagnosis
                        |
                        v
                    Dashboard