"""
PII detector and redaction utilities.

Implementa detección por patrones (regex) para datos sensibles comunes:
- emails
- phone numbers (various formats)
- credit card numbers (Luhn check)
- social security numbers (US pattern, as example)
- IBAN (simple pattern)

Esta implementación es un punto de partida para Fase 1.5.
"""
import re
from typing import Dict, List
from utils.logging_config import logger


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:(?:\+\d{1,3}[- ]?)?\(?\d{1,4}\)?[- ]?)?\d{3,4}[- ]?\d{4}")
CREDIT_CARD_RE = re.compile(r"\b(?:\d[ -]*?){13,16}\b")  # naive
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")  # US SSN
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b")


def _luhn_check(card_num: str) -> bool:
    # Remove spaces and dashes
    digits = re.sub(r"[^0-9]", "", card_num)
    if len(digits) < 13 or len(digits) > 19:
        return False
    total = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        n = int(d)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def detect_pii(text: str) -> Dict[str, List[str]]:
    """Detects PII elements and returns a dict of type -> matches"""
    results = {}

    emails = EMAIL_RE.findall(text)
    if emails:
        results['emails'] = emails

    phones = PHONE_RE.findall(text)
    if phones:
        results['phones'] = phones

    cc_candidates = CREDIT_CARD_RE.findall(text)
    valid_cc = [c for c in cc_candidates if _luhn_check(c)]
    if valid_cc:
        results['credit_cards'] = valid_cc

    ssn = SSN_RE.findall(text)
    if ssn:
        results['ssn'] = ssn

    iban = IBAN_RE.findall(text)
    if iban:
        results['iban'] = iban

    return results


def redact_pii(text: str, placeholder: str = "[REDACTED]") -> str:
    """Return text with PII masked using placeholder"""
    # Order: credit cards (Luhn) first, then emails, ssn, phones, iban
    cc_repl = lambda m: placeholder
    # Credit cards we need to check with Luhn to avoid false positives
    def cc_replacer(m):
        c = m.group(0)
        if _luhn_check(c):
            return placeholder
        return c

    text = CREDIT_CARD_RE.sub(cc_replacer, text)
    text = EMAIL_RE.sub(placeholder, text)
    text = SSN_RE.sub(placeholder, text)
    text = PHONE_RE.sub(placeholder, text)
    text = IBAN_RE.sub(placeholder, text)
    return text


if __name__ == "__main__":
    sample = "Contact: juan.perez@example.com, phone +1 555-123-4567, card 4111 1111 1111 1111, SSN 123-45-6789"
    print(detect_pii(sample))
    print(redact_pii(sample))
