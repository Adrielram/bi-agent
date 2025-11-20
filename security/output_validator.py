"""
Output validator and guardrails for BI Agent (Fase 1.5)

Responsabilidades:
- Analizar la respuesta del agente y las salidas de las herramientas
- Detectar y redactar PII
- Detectar probables inventos/hallucinations (heurísticas) y sugerir citas
- Proveer formato y mensajes de seguridad al usuario cuando sea necesario
"""
from typing import Tuple, Dict, Any
from utils.logging_config import logger
from security.pii_detector import detect_pii, redact_pii
import re


def validate_and_sanitize_output(text: str) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validate and sanitize a textual output from the agent.

    Returns: (is_safe, sanitized_text, details)
    - If PII is found, it's redacted and details include what was removed
    - If potential hallucination is detected (naive heuristic): details includes flags
    """
    details = {
        "pii": {},
        "hallucination": False,
        "notes": []
    }

    # 1) Detect PII and redact
    pii_found = detect_pii(text)
    if pii_found:
        details['pii'] = pii_found
        sanitized = redact_pii(text)
        logger.warning(f"PII detected and redacted in output: {list(pii_found.keys())}")
    else:
        sanitized = text

    # 2) Heuristic for hallucination: check for phrases indicating factual certainty without citation.
    #    The system prompt requests the agent to cite sources. If the text contains strong factual
    #    claims without citing a file or ID, we flag it for review.
    # NOTE: This is a heuristic and will produce false positives; keep conservative.
    # Criteria: Presence of "we have"/"our team"/"our project" or numeric claims and no file names/IDs
    #  - Check for presence of 'proyectos.json' or 'consultores.json' or 'CLI' IDs like 'PROJ001'
    contains_strong_claim = bool(re.search(r"\b(we have|our team|our project|we did|we built|our consultant|we have experience|ex-weather)\b", sanitized, re.IGNORECASE))
    contains_source = bool(re.search(r"(proyectos\.json|consultores\.json|casos_estudio|PROJ|CONS|CLI|CVS|propuestas|id[:\s])", sanitized, re.IGNORECASE))

    if contains_strong_claim and not contains_source:
        details['hallucination'] = True
        details['notes'].append("Potential assertion without a cited source. Ask the agent to provide citations or confirm with read_lines/search.")
        logger.warning("Possible hallucination detected: strong claim without a cited source")

    # Return safe flag: False if PII found (but we still return sanitized text)
    is_safe = not bool(pii_found)
    return is_safe, sanitized, details


def redact_tools_output(tool_name: str, output_text: str) -> Tuple[str, Dict[str, Any]]:
    """Helper to be called by tools to mask PII from their outputs before returning to the agent.

    Returns: (sanitized_text, details)
    """
    is_safe, sanitized, details = validate_and_sanitize_output(output_text)
    if not is_safe:
        # tools should be conservative: they remove PII and also add notes
        details['note'] = f"Tool '{tool_name}' output redacted for PII"
    return sanitized, details


if __name__ == "__main__":
    sample = "We have a consultant with email juan.perez@example.com and project PROJ001"
    safe, s, d = validate_and_sanitize_output(sample)
    print(safe)
    print(s)
    print(d)
