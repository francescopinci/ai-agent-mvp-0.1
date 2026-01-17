from config import MAX_TURNS, PROMPT_SUMMARIZATION, MODEL_SUMMARIZATION
from context_builder import check_token_threshold
from llm import call_llm


def should_summarize(summary: str, messages: list[dict], turns_since_summarization: int) -> bool:
    """
    Determine if summarization should trigger.
    Returns True if: token threshold reached OR turns_since_summarization >= MAX_TURNS
    Returns False otherwise.
    """
    if turns_since_summarization >= MAX_TURNS:
        return True
    if check_token_threshold(summary, messages):
        return True
    return False


def format_messages_for_prompt(messages: list[dict]) -> str:
    """
    Format messages list as text for summarization prompt.
    Format: "User: {content}\nAssistant: {content}\n..."
    """
    lines = []
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            lines.append(f"User: {content}")
        elif role == "assistant":
            lines.append(f"Assistant: {content}")
    return "\n".join(lines)


def run_summarization(current_summary: str, messages: list[dict]) -> str:
    """
    Call summarization LLM and return new summary.
    1. Format messages using format_messages_for_prompt
    2. Format PROMPT_SUMMARIZATION with {summary} and {messages}
    3. Call call_llm with MODEL_SUMMARIZATION
    4. Return the result (new summary)
    """
    formatted_messages = format_messages_for_prompt(messages)
    prompt = PROMPT_SUMMARIZATION.format(summary=current_summary, messages=formatted_messages)
    result = call_llm(MODEL_SUMMARIZATION, prompt, [])
    return result
