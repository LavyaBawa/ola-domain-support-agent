def check_groundedness(answer: str, context: list[str]) -> dict:
    """Check whether the important answer text is supported by retrieved context."""

    combined_context = " ".join(context).lower()

    answer_lower = answer.lower()

    unsupported_markers = [
        "guaranteed refund",
        "free ride",
        "50% compensation",
        "instant resolution",
    ]

    for marker in unsupported_markers:
        if marker in answer_lower and marker not in combined_context:
            return {
                "grounded": False,
                "reason": f"Unsupported claim detected: {marker}",
            }

    return {
        "grounded": True,
        "reason": None,
    }
