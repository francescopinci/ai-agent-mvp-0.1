import logging

from config import MAX_CONTEXT_TOKENS, TOKEN_THRESHOLD_PERCENT, TURNS_TO_RETAIN_AFTER_SUMMARIZATION
from token_counter import count_tokens, count_context_tokens

logger = logging.getLogger(__name__)


def check_token_threshold(summary: str, messages: list[dict]) -> bool:
    """
    Check if context (summary + messages) exceeds token threshold.
    Threshold = MAX_CONTEXT_TOKENS * TOKEN_THRESHOLD_PERCENT
    Returns True if at or over threshold, False if under.
    """
    threshold = MAX_CONTEXT_TOKENS * TOKEN_THRESHOLD_PERCENT
    total_tokens = count_context_tokens(summary, messages)
    over_threshold = total_tokens >= threshold
    logger.info(f"Token check: {total_tokens}/{threshold} ({total_tokens/threshold*100:.1f}%), over={over_threshold}")
    return over_threshold


def is_summary_over_threshold(summary: str) -> bool:
    """
    Check if summary alone exceeds token threshold.
    Returns True if summary tokens >= threshold, False otherwise.
    """
    threshold = MAX_CONTEXT_TOKENS * TOKEN_THRESHOLD_PERCENT
    summary_tokens = count_tokens(summary)
    over_threshold = summary_tokens >= threshold
    if over_threshold:
        logger.warning(f"Summary alone exceeds threshold: {summary_tokens}/{threshold}")
    return over_threshold


def trim_messages_after_summarization(messages: list[dict]) -> list[dict]:
    """
    Trim messages to last TURNS_TO_RETAIN_AFTER_SUMMARIZATION turns.
    A turn = one user message + one assistant message.
    3 turns = 6 messages.
    Returns new list (does not mutate input).
    """
    messages_to_keep = TURNS_TO_RETAIN_AFTER_SUMMARIZATION * 2
    if len(messages) <= messages_to_keep:
        logger.info(f"No trimming needed: {len(messages)} messages <= {messages_to_keep}")
        return list(messages)
    logger.info(f"Trimming messages from {len(messages)} to {messages_to_keep}")
    return list(messages[-messages_to_keep:])
