from typing import Dict

# Maps drug → primary pharmacogenomic gene (CPIC)
DRUG_GENE_MAP = {
    "WARFARIN":      "CYP2C9",
    "CODEINE":       "CYP2D6",
    "CLOPIDOGREL":   "CYP2C19",
    "SIMVASTATIN":   "SLCO1B1",
    "AZATHIOPRINE":  "TPMT",
    "FLUOROURACIL":  "DPYD",
}

# CPIC-based risk rules: (drug, phenotype_code) → recommendation
RISK_RULES = {
    # ── WARFARIN / CYP2C9 ─────────────────────────────────────────────
    ("WARFARIN", "NM"): {
        "risk_label": "Safe",
        "severity":   "none",
        "action":     "Standard warfarin dosing is appropriate.",
        "dosing_adjustment": None,
        "monitoring": "Routine INR monitoring.",
        "alternatives": [],
        "cpic_guideline": "CPIC Warfarin Guideline 2017",
    },
    ("WARFARIN", "IM"): {
        "risk_label": "Adjust Dosage",
        "severity":   "moderate",
        "action":     "Reduce warfarin starting dose by 10–25%.",
        "dosing_adjustment": "Start at 75% of standard dose.",
        "monitoring": "Biweekly INR for first month.",
        "alternatives": [],
        "cpic_guideline": "CPIC Warfarin Guideline 2017",
    },
    ("WARFARIN", "PM"): {
        "risk_label": "Adjust Dosage",
        "severity":   "high",
        "action":     "Reduce warfarin starting dose by 25–50%.",
        "dosing_adjustment": "Start at 50% of standard dose.",
        "monitoring": "Weekly INR monitoring for first month.",
        "alternatives": ["Apixaban", "Rivaroxaban"],
        "cpic_guideline": "CPIC Warfarin Guideline 2017",
    },

    # ── CODEINE / CYP2D6 ──────────────────────────────────────────────
    ("CODEINE", "NM"): {
        "risk_label": "Safe",
        "severity":   "none",
        "action":     "Standard codeine dosing is appropriate.",
        "dosing_adjustment": None,
        "monitoring": "Routine clinical monitoring.",
        "alternatives": [],
        "cpic_guideline": "CPIC Codeine Guideline 2014",
    },
    ("CODEINE", "IM"): {
        "risk_label": "Adjust Dosage",
        "severity":   "low",
        "action":     "Use label-recommended codeine dose; monitor for reduced effect.",
        "dosing_adjustment": "Label-recommended dose.",
        "monitoring": "Monitor for inadequate pain relief.",
        "alternatives": ["Morphine", "Oxycodone"],
        "cpic_guideline": "CPIC Codeine Guideline 2014",
    },
    ("CODEINE", "PM"): {
        "risk_label": "Ineffective",
        "severity":   "moderate",
        "action":     "Codeine will not convert to morphine — no analgesic effect.",
        "dosing_adjustment": "Do not use.",
        "monitoring": None,
        "alternatives": ["Morphine", "Oxycodone", "Non-opioid analgesics"],
        "cpic_guideline": "CPIC Codeine Guideline 2014",
    },
    ("CODEINE", "URM"): {
        "risk_label": "Toxic",
        "severity":   "critical",
        "action":     "AVOID codeine — ultrarapid conversion causes morphine toxicity.",
        "dosing_adjustment": "Contraindicated.",
        "monitoring": None,
        "alternatives": ["Non-opioid analgesics", "Tramadol (with caution)"],
        "cpic_guideline": "CPIC Codeine Guideline 2014",
    },
    ("CODEINE", "RM"): {
        "risk_label": "Toxic",
        "severity":   "high",
        "action":     "High risk of opioid toxicity due to rapid codeine metabolism.",
        "dosing_adjustment": "Avoid or use lowest possible dose.",
        "monitoring": "Close respiratory monitoring.",
        "alternatives": ["Non-opioid analgesics"],
        "cpic_guideline": "CPIC Codeine Guideline 2014",
    },

    # ── CLOPIDOGREL / CYP2C19 ─────────────────────────────────────────
    ("CLOPIDOGREL", "NM"): {
        "risk_label": "Safe",
        "severity":   "none",
        "action":     "Standard clopidogrel dosing is appropriate.",
        "dosing_adjustment": None,
        "monitoring": "Routine platelet function monitoring.",
        "alternatives": [],
        "cpic_guideline": "CPIC Clopidogrel Guideline 2022",
    },
    ("CLOPIDOGREL", "IM"): {
        "risk_label": "Adjust Dosage",
        "severity":   "moderate",
        "action":     "Consider alternative antiplatelet therapy.",
        "dosing_adjustment": "Higher dose may be required.",
        "monitoring": "Platelet function testing recommended.",
        "alternatives": ["Prasugrel", "Ticagrelor"],
        "cpic_guideline": "CPIC Clopidogrel Guideline 2022",
    },
    ("CLOPIDOGREL", "PM"): {
        "risk_label": "Ineffective",
        "severity":   "high",
        "action":     "Clopidogrel will not activate — high cardiovascular risk.",
        "dosing_adjustment": "Contraindicated.",
        "monitoring": None,
        "alternatives": ["Prasugrel", "Ticagrelor"],
        "cpic_guideline": "CPIC Clopidogrel Guideline 2022",
    },
    ("CLOPIDOGREL", "URM"): {
        "risk_label": "Adjust Dosage",
        "severity":   "low",
        "action":     "Possibly enhanced effect; monitor for bleeding.",
        "dosing_adjustment": "Standard dose with bleeding monitoring.",
        "monitoring": "Monitor for increased bleeding risk.",
        "alternatives": [],
        "cpic_guideline": "CPIC Clopidogrel Guideline 2022",
    },

    # ── SIMVASTATIN / SLCO1B1 ─────────────────────────────────────────
    ("SIMVASTATIN", "NM"): {
        "risk_label": "Safe",
        "severity":   "none",
        "action":     "Standard simvastatin dosing is appropriate.",
        "dosing_adjustment": None,
        "monitoring": "Routine CK monitoring.",
        "alternatives": [],
        "cpic_guideline": "CPIC Simvastatin Guideline 2014",
    },
    ("SIMVASTATIN", "IM"): {
        "risk_label": "Adjust Dosage",
        "severity":   "moderate",
        "action":     "Prescribe ≤20mg simvastatin or switch statin.",
        "dosing_adjustment": "Max 20mg/day.",
        "monitoring": "CK levels monthly for 3 months.",
        "alternatives": ["Pravastatin", "Rosuvastatin"],
        "cpic_guideline": "CPIC Simvastatin Guideline 2014",
    },
    ("SIMVASTATIN", "PM"): {
        "risk_label": "Toxic",
        "severity":   "high",
        "action":     "High risk of simvastatin-induced myopathy — avoid high doses.",
        "dosing_adjustment": "Use lowest dose (5mg) or switch statin.",
        "monitoring": "CK levels monthly.",
        "alternatives": ["Pravastatin", "Rosuvastatin", "Fluvastatin"],
        "cpic_guideline": "CPIC Simvastatin Guideline 2014",
    },

    # ── AZATHIOPRINE / TPMT ───────────────────────────────────────────
    ("AZATHIOPRINE", "NM"): {
        "risk_label": "Safe",
        "severity":   "none",
        "action":     "Standard azathioprine dosing is appropriate.",
        "dosing_adjustment": None,
        "monitoring": "CBC every 1–3 months.",
        "alternatives": [],
        "cpic_guideline": "CPIC Thiopurines Guideline 2018",
    },
    ("AZATHIOPRINE", "IM"): {
        "risk_label": "Adjust Dosage",
        "severity":   "moderate",
        "action":     "Reduce azathioprine dose by 30–70%.",
        "dosing_adjustment": "Start at 30–70% of standard dose.",
        "monitoring": "CBC weekly for first month.",
        "alternatives": [],
        "cpic_guideline": "CPIC Thiopurines Guideline 2018",
    },
    ("AZATHIOPRINE", "PM"): {
        "risk_label": "Toxic",
        "severity":   "critical",
        "action":     "AVOID azathioprine — severe life-threatening myelosuppression risk.",
        "dosing_adjustment": "Reduce to 10% of standard dose or avoid entirely.",
        "monitoring": "CBC weekly if used.",
        "alternatives": ["Mycophenolate mofetil"],
        "cpic_guideline": "CPIC Thiopurines Guideline 2018",
    },

    # ── FLUOROURACIL / DPYD ───────────────────────────────────────────
    ("FLUOROURACIL", "NM"): {
        "risk_label": "Safe",
        "severity":   "none",
        "action":     "Standard fluorouracil dosing is appropriate.",
        "dosing_adjustment": None,
        "monitoring": "Routine CBC and clinical monitoring.",
        "alternatives": [],
        "cpic_guideline": "CPIC Fluoropyrimidines Guideline 2017",
    },
    ("FLUOROURACIL", "IM"): {
        "risk_label": "Adjust Dosage",
        "severity":   "high",
        "action":     "Reduce fluorouracil starting dose by 25–50%.",
        "dosing_adjustment": "Start at 50–75% of standard dose.",
        "monitoring": "CBC and clinical status weekly.",
        "alternatives": [],
        "cpic_guideline": "CPIC Fluoropyrimidines Guideline 2017",
    },
    ("FLUOROURACIL", "PM"): {
        "risk_label": "Toxic",
        "severity":   "critical",
        "action":     "AVOID fluorouracil — life-threatening toxicity risk.",
        "dosing_adjustment": "Reduce by ≥50% or avoid entirely.",
        "monitoring": "CBC and clinical status if used.",
        "alternatives": ["Capecitabine (with dose reduction)", "Raltitrexed"],
        "cpic_guideline": "CPIC Fluoropyrimidines Guideline 2017",
    },
}


def assess_drug_risk(drug: str, phenotype_code: str, confidence: float) -> Dict:
    """
    Look up CPIC risk rule for drug + phenotype combination.
    Returns Unknown result if no rule found — never fabricates.
    """
    key = (drug.upper(), phenotype_code)
    rule = RISK_RULES.get(key)

    if not rule:
        return {
            "risk_label":        "Unknown",
            "severity":          "none",
            "confidence_score":  0.4,
            "action":            "Insufficient data for this drug-gene-phenotype combination.",
            "dosing_adjustment": None,
            "alternatives":      [],
            "cpic_guideline":    None,
        }

    return {**rule, "confidence_score": round(confidence, 2)}
