"""
Ethical AI Implementation Framework for Healthcare
Author: Yash Vashisth
Roll No: 2301730149

Description:
Core framework module that defines ethical principles, evaluates AI systems
against them, and produces an ethics compliance report for healthcare
organizations deploying Generative AI.
"""

from datetime import datetime


ETHICAL_PRINCIPLES = {
    "Fairness": {
        "description": "AI outputs should not discriminate across age, gender, race, or socioeconomic status.",
        "checks": [
            "bias_tested_across_demographics",
            "training_data_representative",
            "performance_parity_documented"
        ]
    },
    "Transparency": {
        "description": "Clinicians and patients should understand how the AI arrived at a recommendation.",
        "checks": [
            "model_card_available",
            "explanations_provided_to_clinician",
            "limitations_disclosed_to_patient"
        ]
    },
    "Accountability": {
        "description": "Clear ownership of AI-driven decisions and a path for redress when harm occurs.",
        "checks": [
            "human_in_the_loop",
            "audit_logs_enabled",
            "incident_response_plan_defined"
        ]
    },
    "Privacy": {
        "description": "Patient data must be protected in line with HIPAA, GDPR, and India's DPDP Act.",
        "checks": [
            "phi_anonymized",
            "encryption_at_rest_and_transit",
            "consent_collected_and_revocable"
        ]
    },
    "Safety": {
        "description": "AI should not cause physical, psychological, or financial harm to patients.",
        "checks": [
            "clinical_validation_completed",
            "failure_modes_documented",
            "continuous_monitoring_in_place"
        ]
    },
    "Beneficence": {
        "description": "The AI must demonstrably improve patient outcomes or clinical workflow.",
        "checks": [
            "outcome_metric_defined",
            "baseline_comparison_available",
            "real_world_benefit_measured"
        ]
    },
    "Autonomy": {
        "description": "Patients retain the right to refuse AI-driven decisions and seek human judgment.",
        "checks": [
            "opt_out_mechanism_available",
            "informed_consent_obtained",
            "human_alternative_offered"
        ]
    }
}


REGULATORY_REFERENCES = {
    "HIPAA": "US health data privacy and security rule.",
    "GDPR": "EU regulation on personal data and automated decision-making.",
    "DPDP Act 2023": "India's Digital Personal Data Protection Act.",
    "FDA SaMD": "FDA guidance on Software as a Medical Device.",
    "WHO Ethics Guidance": "WHO guidance on ethics and governance of AI for health.",
    "EU AI Act": "Classifies medical AI as high-risk and mandates conformity assessment."
}


RISK_LEVELS = {
    "low": (0.85, 1.00),
    "moderate": (0.60, 0.85),
    "high": (0.30, 0.60),
    "critical": (0.00, 0.30)
}


def evaluate_system(system_name, responses):
    """
    Evaluate a healthcare AI system against the framework.

    Args:
        system_name: name of the AI system being audited
        responses: dict mapping check_id -> bool (True = compliant)

    Returns:
        dict with per-principle scores, overall score, risk level, and gaps
    """
    principle_results = {}
    all_gaps = []

    for principle, meta in ETHICAL_PRINCIPLES.items():
        checks = meta["checks"]
        passed = sum(1 for c in checks if responses.get(c, False))
        total = len(checks)
        score = passed / total if total else 0

        gaps = [c for c in checks if not responses.get(c, False)]
        all_gaps.extend([(principle, g) for g in gaps])

        principle_results[principle] = {
            "score": round(score, 2),
            "passed": passed,
            "total": total,
            "gaps": gaps
        }

    overall = sum(r["score"] for r in principle_results.values()) / len(principle_results)
    overall = round(overall, 2)

    risk = "critical"
    for level, (low, high) in RISK_LEVELS.items():
        if low <= overall <= high:
            risk = level
            break

    return {
        "system_name": system_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "overall_score": overall,
        "risk_level": risk,
        "principles": principle_results,
        "gaps": all_gaps
    }


def get_recommendations(evaluation):
    """Return a list of recommendations based on the gaps found."""
    recs = []
    gap_to_rec = {
        "bias_tested_across_demographics": "Run bias audits across age, gender, race, and income groups.",
        "training_data_representative": "Augment training data to cover underrepresented populations.",
        "performance_parity_documented": "Publish subgroup performance metrics in the model card.",
        "model_card_available": "Create a model card covering intended use, data, and limits.",
        "explanations_provided_to_clinician": "Integrate SHAP or feature attribution in the clinician UI.",
        "limitations_disclosed_to_patient": "Add a plain-language disclosure before AI-driven advice.",
        "human_in_the_loop": "Require clinician sign-off for all treatment-level recommendations.",
        "audit_logs_enabled": "Enable immutable audit logs for every model inference.",
        "incident_response_plan_defined": "Draft and rehearse an AI-incident response runbook.",
        "phi_anonymized": "De-identify PHI before it reaches the model; review re-identification risk.",
        "encryption_at_rest_and_transit": "Enforce TLS 1.3 in transit and AES-256 at rest.",
        "consent_collected_and_revocable": "Add a consent flow that allows withdrawal at any time.",
        "clinical_validation_completed": "Run a prospective clinical validation study before deployment.",
        "failure_modes_documented": "List and test known failure modes; publish in the model card.",
        "continuous_monitoring_in_place": "Deploy drift and performance monitoring in production.",
        "outcome_metric_defined": "Agree on a clinical outcome metric with the medical team.",
        "baseline_comparison_available": "Compare AI-assisted vs standard-of-care performance.",
        "real_world_benefit_measured": "Track real-world benefit for the first 6 months after launch.",
        "opt_out_mechanism_available": "Let patients opt out of AI-driven pathways without penalty.",
        "informed_consent_obtained": "Obtain explicit informed consent for AI-assisted care.",
        "human_alternative_offered": "Always offer a human-only clinical pathway as an alternative."
    }

    for principle, gap in evaluation["gaps"]:
        recs.append({
            "principle": principle,
            "gap": gap,
            "recommendation": gap_to_rec.get(gap, "Address this gap per organizational policy.")
        })
    return recs


def format_text_report(evaluation, recommendations):
    """Render the evaluation as a plain-text report."""
    lines = []
    lines.append("=" * 70)
    lines.append("  ETHICAL AI ASSESSMENT REPORT")
    lines.append("  Healthcare Generative AI Framework")
    lines.append("=" * 70)
    lines.append(f"System    : {evaluation['system_name']}")
    lines.append(f"Assessed  : {evaluation['timestamp']}")
    lines.append(f"Score     : {evaluation['overall_score']}  (Risk: {evaluation['risk_level'].upper()})")
    lines.append("-" * 70)

    lines.append("\nPRINCIPLE SCORES")
    for principle, r in evaluation["principles"].items():
        lines.append(f"  {principle:<16} {r['score']:.2f}  ({r['passed']}/{r['total']} checks passed)")

    if recommendations:
        lines.append("\nRECOMMENDATIONS")
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"  {i}. [{rec['principle']}] {rec['recommendation']}")
    else:
        lines.append("\nNo gaps detected. System passes the framework.")

    lines.append("\n" + "=" * 70)
    lines.append("  Prepared using the Ethical AI Framework for Healthcare")
    lines.append("  Author: Yash Vashisth (2301730149)")
    lines.append("=" * 70)
    return "\n".join(lines)


def main():
    """CLI entry point for a quick demo assessment."""
    print("\nEthical AI Framework for Healthcare - Demo Assessment")
    print("Author: Yash Vashisth (2301730149)\n")

    demo_responses = {
        "bias_tested_across_demographics": True,
        "training_data_representative": False,
        "performance_parity_documented": True,
        "model_card_available": True,
        "explanations_provided_to_clinician": True,
        "limitations_disclosed_to_patient": False,
        "human_in_the_loop": True,
        "audit_logs_enabled": True,
        "incident_response_plan_defined": False,
        "phi_anonymized": True,
        "encryption_at_rest_and_transit": True,
        "consent_collected_and_revocable": True,
        "clinical_validation_completed": False,
        "failure_modes_documented": True,
        "continuous_monitoring_in_place": False,
        "outcome_metric_defined": True,
        "baseline_comparison_available": True,
        "real_world_benefit_measured": False,
        "opt_out_mechanism_available": True,
        "informed_consent_obtained": True,
        "human_alternative_offered": True
    }

    evaluation = evaluate_system("Demo Radiology Assistant", demo_responses)
    recommendations = get_recommendations(evaluation)
    print(format_text_report(evaluation, recommendations))


if __name__ == "__main__":
    main()
