import tiktoken

_encoding = None


def _get_encoding():
    """Lazily initialize and return the tiktoken encoding."""
    global _encoding
    if _encoding is None:
        _encoding = tiktoken.get_encoding("cl100k_base")
    return _encoding


def count_tokens(text: str) -> int:
    """Count tokens for a single string."""
    return len(_get_encoding().encode(text))


def count_message_tokens(message: dict) -> int:
    """Count tokens for a single message {"role": ..., "content": ...}.
    Counts only the content field, not message structure overhead."""
    return count_tokens(message["content"])


def count_context_tokens(summary: str, messages: list) -> int:
    """Count total tokens for summary + all message contents combined."""
    total = count_tokens(summary)
    for message in messages:
        total += count_message_tokens(message)
    return total
