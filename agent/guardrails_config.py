"""
Guardrails integration for BI Agent

This file provides wrappers around the Guardrails AI validators
for input and output validation. If Guardrails is unavailable, the
code falls back to local heuristics already implemented in security/
"""
from typing import Optional
from utils.logging_config import logger

try:
    from guardrails import Guard
    from guardrails.validators import (
        ValidLength,
        DetectPII,
        RestrictToTopic,
        ToxicLanguage,
    )
    _HAS_GUARDRAILS = True
except Exception:
    _HAS_GUARDRAILS = False

from security.input_validator import validate_user_input
from security.output_validator import validate_and_sanitize_output
from monitoring.guardrails_metrics import (
    guard_input_blocked_total,
    guard_output_redacted_total,
    guard_tool_redacted_total,
)


if _HAS_GUARDRAILS:
    # Input guardrails: examples; tune for production
    input_guard = Guard().use_many(
        ValidLength(min=5, max=3000, on_fail="fix"),
        # DetectPII(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail="fix"),
        RestrictToTopic(
            valid_topics=["business intelligence", "projects", "consultants", "clients", "technology"],
            invalid_topics=["politics", "religion", "personal attacks"],
            on_fail="exception",
        ),
        ToxicLanguage(threshold=0.5, on_fail="exception"),
    )

    output_guard = Guard().use_many(
        ValidLength(min=20, max=5000, on_fail="reask"),
        # DetectPII(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD"], on_fail="fix"),
    )


def validate_input(user_input: str) -> str:
    """
    Validate input using Guardrails if available; otherwise fall back to local validator.
    Raises:
        ValueError if validation fails.
    Returns sanitized input when OK.
    """
    if _HAS_GUARDRAILS:
        try:
            validated = input_guard.validate(user_input)
            return validated.validated_output
        except Exception as e:
            logger.warning(f"Guardrails input validation failed: {str(e)}")
            raise ValueError(str(e))

    # Fallback: local validator
    ok, info = validate_user_input(user_input)
    if not ok:
        raise ValueError(info)
    return info


def validate_output(agent_output: str) -> str:
    """
    Validate/sanitize agent output using Guardrails if available; otherwise fallback.
    Does not raise by default; returns sanitized output.
    """
    if _HAS_GUARDRAILS:
        try:
            validated = output_guard.validate(agent_output)
            sanitized = validated.validated_output
            if sanitized != agent_output:
                guard_output_redacted_total.inc()
            return sanitized
        except Exception as e:
            logger.warning(f"Guardrails output validation warning: {str(e)}")
            return agent_output

    # Fallback: local validator
    safe, sanitized, details = validate_and_sanitize_output(agent_output)
    if sanitized != agent_output:
        guard_output_redacted_total.inc()
    return sanitized


def validate_tool_output(tool_name: str, output_text: str):
    """Wrapper to validate/clean tool outputs (e.g. read_lines results).

    Returns (sanitized_text, details)
    """
    details = {}
    try:
        sanitized = validate_output(output_text)
        if sanitized != output_text:
            guard_tool_redacted_total.inc()
        return sanitized, details
    except Exception as e:
        logger.warning(f"Tool output validation failed for {tool_name}: {str(e)}")
        # fallback: return the original text
        return output_text, {'error': str(e)}


if __name__ == "__main__":
    # Quick smoke tests
    try:
        print(validate_input("¿Qué proyectos tenemos en FinTech con Python?"))
    except Exception as e:
        print(f"Input failed: {e}")

    print(validate_output("Tenemos el proyecto PROJ001 donde usamos Python y obtuvimos un 20% de mejora"))
