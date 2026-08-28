import os
import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

AI_RESULTS_FILE = "ai_diagnosis/diagnosis_results.csv"
REVIEW_FILE = "human_review/responsible_ai_log.csv"
CASES_FILE = "data/cases.csv"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NetSage AI Dashboard",
    page_icon="🌐",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🌐 NetSage AI — Network Troubleshooting Dashboard")

st.markdown(
    """
    **AI-assisted Cisco network troubleshooting system**

    This dashboard summarizes deterministic rule-checking,
    AI diagnosis, confidence, and human review.
    """
)

st.divider()


# ============================================================
# LOAD DATA
# ============================================================

def load_csv(path):

    if os.path.exists(path):

        try:
            return pd.read_csv(path)

        except Exception as error:
            st.error(f"Could not read {path}: {error}")

    return pd.DataFrame()


cases_df = load_csv(CASES_FILE)
ai_df = load_csv(AI_RESULTS_FILE)
review_df = load_csv(REVIEW_FILE)


# ============================================================
# DATA SUMMARY
# ============================================================

total_cases = len(cases_df)

ai_cases = len(ai_df)

if not ai_df.empty and "confidence" in ai_df.columns:

    high_confidence = (
        ai_df["confidence"]
        .astype(str)
        .str.lower()
        .str.startswith("high")
        .sum()
    )

    medium_confidence = (
        ai_df["confidence"]
        .astype(str)
        .str.lower()
        .str.startswith("medium")
        .sum()
    )

    low_confidence = (
        ai_df["confidence"]
        .astype(str)
        .str.lower()
        .str.startswith("low")
        .sum()
    )

else:

    high_confidence = 0
    medium_confidence = 0
    low_confidence = 0


# ============================================================
# TOP METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Cases",
        total_cases
    )

with col2:
    st.metric(
        "AI Diagnoses",
        ai_cases
    )

with col3:
    st.metric(
        "High Confidence",
        high_confidence
    )

with col4:
    st.metric(
        "Cases Needing Review",
        max(total_cases - ai_cases, 0)
    )


st.divider()


# ============================================================
# AI CONFIDENCE
# ============================================================

st.subheader("AI Confidence Distribution")

confidence_data = pd.DataFrame({
    "Confidence": [
        "High",
        "Medium",
        "Low"
    ],
    "Cases": [
        high_confidence,
        medium_confidence,
        low_confidence
    ]
})

if confidence_data["Cases"].sum() > 0:

    st.bar_chart(
        confidence_data.set_index("Confidence")
    )

else:

    st.info("No AI confidence data available yet.")


# ============================================================
# CASE CATEGORIES
# ============================================================

st.subheader("Case Categories")

if not cases_df.empty and "category" in cases_df.columns:

    category_counts = (
        cases_df["category"]
        .fillna("Unknown")
        .value_counts()
    )

    st.bar_chart(category_counts)

else:

    st.info("Case category information is not available.")


# ============================================================
# AI AGREEMENT
# ============================================================

st.subheader("AI Agreement — Preliminary")

if not ai_df.empty and "ai_agreement" in ai_df.columns:

    agreement_counts = (
        ai_df["ai_agreement"]
        .fillna("Unknown")
        .value_counts()
    )

    st.bar_chart(agreement_counts)

    st.caption(
        "This is a preliminary text-based indicator. "
        "Final agreement is determined through human review."
    )

else:

    st.info(
        "AI agreement information will appear after "
        "AI diagnosis results are generated."
    )


# ============================================================
# HUMAN REVIEW
# ============================================================

st.subheader("Human Review")

if not review_df.empty and "human_decision" in review_df.columns:

    decisions = (
        review_df["human_decision"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    completed_reviews = decisions[
        decisions != ""
    ]

    if len(completed_reviews) > 0:

        review_counts = (
            completed_reviews
            .value_counts()
        )

        st.bar_chart(review_counts)

        st.metric(
            "Completed Human Reviews",
            len(completed_reviews)
        )

    else:

        st.info(
            "Human review has not been completed yet."
        )

else:

    st.info(
        "Human review data is not available yet."
    )


# ============================================================
# RULE CHECKER SUMMARY
# ============================================================

st.subheader("Deterministic Rule Checker")

rule_file = "checker/sample_output.txt"

if os.path.exists(rule_file):

    with open(
        rule_file,
        "r",
        encoding="utf-8"
    ) as file:

        rule_output = file.read()

    st.text_area(
        "Latest Rule Checker Output",
        rule_output,
        height=250
    )

else:

    st.info(
        "Rule checker output has not been generated."
    )


# ============================================================
# AI DIAGNOSIS TABLE
# ============================================================

st.subheader("AI Diagnosis Results")

if not ai_df.empty:

    display_columns = [
        "case_id",
        "root_cause",
        "osi_layer",
        "confidence",
        "next_command",
        "expected_fault",
        "ai_agreement"
    ]

    available_columns = [
        column
        for column in display_columns
        if column in ai_df.columns
    ]

    st.dataframe(
        ai_df[available_columns],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No AI diagnosis results are currently available."
    )


# ============================================================
# HUMAN REVIEW TABLE
# ============================================================

st.subheader("Human Review Log")

if not review_df.empty:

    review_columns = [
        "case_id",
        "ai_root_cause",
        "ai_confidence",
        "expected_fault",
        "human_decision",
        "human_correction",
        "reason_for_correction",
        "final_diagnosis",
        "verified"
    ]

    available_review_columns = [
        column
        for column in review_columns
        if column in review_df.columns
    ]

    st.dataframe(
        review_df[available_review_columns],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No human review records are currently available."
    )


# ============================================================
# RESPONSIBLE AI NOTES
# ============================================================

st.divider()

st.subheader("Responsible AI Controls")

st.markdown(
    """
    - AI diagnoses are recommendations, not autonomous decisions.
    - Cisco command evidence is supplied as the basis for diagnosis.
    - The system is instructed not to invent command output.
    - Confidence is explicitly reported.
    - A human reviewer must accept, edit, or reject the diagnosis.
    - Fixes should be verified after implementation.
    - API credentials are stored outside the source code.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "NetSage AI — AI-assisted Cisco Network Troubleshooting Assistant"
)