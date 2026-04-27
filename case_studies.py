"""
Case Studies - Real-world Healthcare AI Ethics Scenarios
Author: Gopesh Aggarwal (2301730158)

Description:
A library of short case studies illustrating ethical issues in healthcare AI
and how the framework applies to each.
"""

CASE_STUDIES = [
    {
        "title": "Radiology Triage Model with Demographic Bias",
        "scenario": (
            "A hospital deploys a chest X-ray triage model. Post-deployment audit "
            "shows sensitivity is 12% lower for female patients over 60 because "
            "the training data skewed male and younger."
        ),
        "principles_affected": ["Fairness", "Safety", "Beneficence"],
        "framework_response": (
            "Pause deployment for the affected cohort, retrain with balanced data, "
            "publish subgroup performance in the model card, and require clinician "
            "override for high-risk findings in that cohort."
        ),
        "outcome": (
            "Sensitivity gap narrowed to 3% after retraining; hospital published "
            "the audit as part of its transparency commitment."
        )
    },
    {
        "title": "Generative AI for Patient Discharge Summaries",
        "scenario": (
            "A clinic pilots an LLM that drafts discharge summaries from the EHR. "
            "In 2% of cases the model hallucinates a medication the patient was "
            "never prescribed."
        ),
        "principles_affected": ["Safety", "Accountability", "Transparency"],
        "framework_response": (
            "Mandatory clinician review before the summary is signed, automatic "
            "flagging of any medication not present in the EHR, and a documented "
            "incident-response process for any summary that reaches the patient "
            "with a hallucination."
        ),
        "outcome": (
            "Hallucinations in signed summaries dropped to zero over six months; "
            "clinicians reported 35% time savings on paperwork."
        )
    },
    {
        "title": "Mental Health Chatbot with No Opt-Out",
        "scenario": (
            "A health app routes all first-contact mental health queries through "
            "an AI chatbot. Patients in crisis cannot reach a human without first "
            "answering several bot questions."
        ),
        "principles_affected": ["Autonomy", "Safety", "Beneficence"],
        "framework_response": (
            "Add a persistent 'Talk to a human now' button, auto-escalate any "
            "message matching a crisis keyword list, and offer a human-only "
            "pathway at signup."
        ),
        "outcome": (
            "Escalation time for crisis messages reduced from 14 minutes to 45 "
            "seconds; regulatory complaint was withdrawn."
        )
    },
    {
        "title": "Predictive Model Using Re-identifiable Data",
        "scenario": (
            "A startup trains a readmission-risk model on 'anonymized' hospital "
            "data. A researcher demonstrates that patients can be re-identified "
            "using ZIP code plus admission date."
        ),
        "principles_affected": ["Privacy", "Accountability"],
        "framework_response": (
            "Apply k-anonymity with k>=5 before training, aggregate ZIP to the "
            "first three digits, run a formal re-identification risk assessment, "
            "and update the data-sharing agreement."
        ),
        "outcome": (
            "Re-identification risk dropped below 1%; the model was re-certified "
            "under the hospital's privacy policy."
        )
    },
    {
        "title": "AI-Generated Imaging Reports Without Clinician Sign-off",
        "scenario": (
            "A teleradiology vendor auto-sends AI-generated reports directly to "
            "referring physicians for simple cases, with no radiologist review."
        ),
        "principles_affected": ["Accountability", "Safety", "Autonomy"],
        "framework_response": (
            "Require a licensed radiologist to sign every report that leaves the "
            "system, keep an audit trail of sign-off, and disclose AI involvement "
            "to the referring physician and patient."
        ),
        "outcome": (
            "One missed subtle finding was caught during mandatory review; the "
            "vendor avoided a regulatory action."
        )
    }
]


def get_case(index):
    """Return a case study by 0-based index, or None if out of range."""
    if 0 <= index < len(CASE_STUDIES):
        return CASE_STUDIES[index]
    return None


def list_titles():
    """Return just the list of case study titles."""
    return [c["title"] for c in CASE_STUDIES]
