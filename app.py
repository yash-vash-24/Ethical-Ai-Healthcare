"""
Ethical AI Implementation Framework for Healthcare - Streamlit App
Author: Yash Vashisth
Roll No: 2301730158

Description:
Interactive web interface for assessing healthcare AI systems against the
ethical framework, browsing case studies, and generating a downloadable
compliance report.
"""

import streamlit as st
from ethics_framework import (
    ETHICAL_PRINCIPLES,
    REGULATORY_REFERENCES,
    evaluate_system,
    get_recommendations,
    format_text_report
)
from case_studies import CASE_STUDIES

st.set_page_config(
    page_title="Ethical AI Framework - Healthcare",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #1f4e79, #2c7da0);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    .principle-box {
        background-color: #f0f8ff;
        padding: 15px;
        border-left: 4px solid #1f4e79;
        border-radius: 5px;
        margin: 8px 0;
    }
    .risk-low { color: #2e7d32; font-weight: bold; }
    .risk-moderate { color: #ed6c02; font-weight: bold; }
    .risk-high { color: #d32f2f; font-weight: bold; }
    .risk-critical { color: #b71c1c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>🩺 Ethical AI Framework for Healthcare</h1>
    <p>Responsible Generative AI in Medical Applications</p>
    <p><b>Yash Vashisth</b> | Roll No: 2301730158</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 📋 About")
    st.write(
        "A structured framework to assess healthcare AI systems against "
        "seven ethical principles aligned with HIPAA, GDPR, DPDP Act, and "
        "the WHO ethics guidance for AI in health."
    )
    st.markdown("---")
    st.markdown("### 📖 The 7 Principles")
    for p in ETHICAL_PRINCIPLES.keys():
        st.write(f"- {p}")
    st.markdown("---")
    st.markdown("### 🏛️ Regulatory Alignment")
    for reg in REGULATORY_REFERENCES.keys():
        st.write(f"- {reg}")

tab1, tab2, tab3, tab4 = st.tabs([
    "📘 Framework", "✅ Assess System", "📂 Case Studies", "📚 Guidelines"
])

with tab1:
    st.subheader("The Seven Ethical Principles")
    st.write(
        "Every AI system deployed in a healthcare setting should be evaluated "
        "against the following principles before and after deployment."
    )

    for principle, meta in ETHICAL_PRINCIPLES.items():
        with st.container(border=True):
            st.markdown(f"### {principle}")
            st.write(meta["description"])
            st.markdown("**Compliance checks:**")
            for c in meta["checks"]:
                st.write(f"- {c.replace('_', ' ').capitalize()}")

    st.markdown("---")
    st.subheader("Regulatory References")
    for reg, desc in REGULATORY_REFERENCES.items():
        st.markdown(f"**{reg}** — {desc}")

with tab2:
    st.subheader("Assess an AI System")
    st.write(
        "Complete the checklist below for your AI system. The framework will "
        "compute an ethics score, classify risk level, and produce a "
        "downloadable report."
    )

    system_name = st.text_input(
        "System name:",
        placeholder="e.g., Chest X-Ray Triage Assistant v2"
    )

    responses = {}
    with st.form("assessment_form"):
        for principle, meta in ETHICAL_PRINCIPLES.items():
            st.markdown(f"#### {principle}")
            st.caption(meta["description"])
            for check in meta["checks"]:
                label = check.replace("_", " ").capitalize()
                responses[check] = st.checkbox(label, key=check)
            st.markdown("")

        submitted = st.form_submit_button("🩺 Run Ethics Assessment", use_container_width=True)

    if submitted:
        if not system_name.strip():
            st.warning("Please provide a system name before running the assessment.")
        else:
            evaluation = evaluate_system(system_name, responses)
            recommendations = get_recommendations(evaluation)

            risk_class = f"risk-{evaluation['risk_level']}"
            col1, col2, col3 = st.columns(3)
            col1.metric("Overall Score", f"{evaluation['overall_score']:.2f}")
            col2.markdown(
                f"**Risk Level:** <span class='{risk_class}'>"
                f"{evaluation['risk_level'].upper()}</span>",
                unsafe_allow_html=True
            )
            col3.metric("Gaps Found", len(evaluation["gaps"]))

            st.markdown("### Principle Scores")
            for principle, r in evaluation["principles"].items():
                st.progress(r["score"], text=f"{principle} — {r['passed']}/{r['total']}")

            if recommendations:
                st.markdown("### Recommendations")
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(
                        f"**{i}. [{rec['principle']}]** {rec['recommendation']}"
                    )
            else:
                st.success("✅ No gaps detected. System is fully compliant with the framework.")

            report_text = format_text_report(evaluation, recommendations)
            st.download_button(
                "⬇️ Download Report",
                report_text,
                file_name=f"ethics_report_{system_name.replace(' ', '_')}.txt",
                mime="text/plain"
            )

with tab3:
    st.subheader("Case Studies")
    st.write("Real-world scenarios illustrating how the framework applies.")

    titles = [c["title"] for c in CASE_STUDIES]
    selected = st.selectbox("Pick a case study:", titles)
    case = next(c for c in CASE_STUDIES if c["title"] == selected)

    with st.container(border=True):
        st.markdown(f"### {case['title']}")
        st.markdown("**Scenario**")
        st.write(case["scenario"])

        st.markdown("**Principles affected**")
        st.write(", ".join(case["principles_affected"]))

        st.markdown("**Framework response**")
        st.write(case["framework_response"])

        st.markdown("**Outcome**")
        st.info(case["outcome"])

with tab4:
    st.subheader("Implementation Guidelines")
    st.markdown("""
    ### Pre-deployment
    1. Define the clinical problem and the measurable outcome the AI should improve.
    2. Assemble a cross-functional review team: clinician, data scientist, ethics officer, patient representative.
    3. Run the framework checklist and close every high-severity gap before pilot.
    4. Complete a Data Protection Impact Assessment (DPIA) under GDPR or the equivalent under DPDP Act.
    5. Document intended use, known limits, and failure modes in a model card.

    ### During pilot
    1. Keep a human in the loop for every clinical decision.
    2. Log every inference with inputs, outputs, and clinician action taken.
    3. Collect clinician and patient feedback weekly.
    4. Re-run the framework checklist after 30 and 90 days.

    ### Post-deployment
    1. Monitor for drift and subgroup performance regressions monthly.
    2. Publish a public-facing summary of model performance annually.
    3. Maintain an incident response runbook and practice it once per quarter.
    4. Retire or retrain the model if any principle score drops below 0.6.

    ### Quick-start checklist for healthcare organizations
    - [ ] Appoint an AI ethics officer.
    - [ ] Adopt this framework as organization policy.
    - [ ] Run the framework against every AI system in production.
    - [ ] Publish a transparency report once a year.
    - [ ] Train clinicians on AI limits and override authority.
    """)

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray; font-size:12px;'>"
    "Ethical AI Framework for Healthcare | Yash Vashisth (2301730158)"
    "</div>",
    unsafe_allow_html=True
)
