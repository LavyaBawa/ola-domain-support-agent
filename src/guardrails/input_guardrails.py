import re


PHONE_PATTERN = re.compile(r"\b(?:\+91[- ]?)?[6-9]\d{9}\b")


INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"ignore all previous instructions",
    r"reveal the system prompt",
    r"show me the system prompt",
    r"disregard your instructions",
]


def mask_pii(text: str) -> str:
    """Mask fixed-format phone numbers."""
    return PHONE_PATTERN.sub("[PHONE_REDACTED]", text)


def detect_prompt_injection(text: str) -> bool:
    """Return True when common prompt-injection instructions are detected."""
    lowered = text.lower()

    return any(
        re.search(pattern, lowered)
        for pattern in INJECTION_PATTERNS
    )


def validate_input(text: str) -> dict:
    """Apply input guardrails before processing a request."""
    masked_text = mask_pii(text)

    if detect_prompt_injection(masked_text):
        return {
            "allowed": False,
            "text": masked_text,
            "reason": "Prompt injection detected.",
        }

    return {
        "allowed": True,
        "text": masked_text,
        "reason": None,
    }

def guard_input(text: str) -> str:
    """Validate and sanitize an incoming support request."""

    result = validate_input(text)

    if not result["allowed"]:
        raise ValueError(result["reason"])

    return result["text"]
