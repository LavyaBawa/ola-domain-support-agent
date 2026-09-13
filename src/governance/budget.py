MAX_INPUT_CHARS = 4000
MAX_ESTIMATED_TOKENS = 1000


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def validate_request_budget(text: str) -> dict:
    estimated_tokens = estimate_tokens(text)

    if len(text) > MAX_INPUT_CHARS:
        return {
            "allowed": False,
            "reason": "Request exceeds maximum input size.",
            "estimated_tokens": estimated_tokens,
        }

    if estimated_tokens > MAX_ESTIMATED_TOKENS:
        return {
            "allowed": False,
            "reason": "Request exceeds token budget.",
            "estimated_tokens": estimated_tokens,
        }

    return {
        "allowed": True,
        "reason": None,
        "estimated_tokens": estimated_tokens,
    }
