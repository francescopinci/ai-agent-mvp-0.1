import logging
import traceback

import streamlit as st

from config import MODEL_CONVERSATIONAL, MODEL_FINAL_REPORT, PROMPT_CONVERSATIONAL, PROMPT_FINAL_REPORT
from llm import call_llm
from status_parser import parse_status, StatusParseError, MAX_STATUS_RETRIES
from context_builder import is_summary_over_threshold, trim_messages_after_summarization
from summarization import should_summarize, run_summarization

logger = logging.getLogger(__name__)


def call_conversational_llm_with_retry(system_prompt: str, messages: list[dict]) -> tuple[str, str]:
    """
    Call conversational LLM with status retry logic.
    - Calls LLM, parses status
    - If status None: retry up to MAX_STATUS_RETRIES times
    - If still failing: raise StatusParseError
    - Returns (status, content) on success
    """
    for attempt in range(MAX_STATUS_RETRIES + 1):
        logger.info(f"LLM call attempt {attempt + 1}/{MAX_STATUS_RETRIES + 1}")
        response = call_llm(MODEL_CONVERSATIONAL, system_prompt, messages)
        logger.info(f"LLM response received, length={len(response)}")
        status, content = parse_status(response)
        logger.info(f"Parsed status: {status}")
        if status is not None:
            return (status, content)
        logger.warning(f"Status parse failed on attempt {attempt + 1}, response starts with: {response[:100]}")
    raise StatusParseError("Status parsing failed after retries")


def run_finalization() -> None:
    """
    Execute finalization sequence:
    1. Run final summarization on remaining messages
    2. Update st.session_state.summary
    3. Format PROMPT_FINAL_REPORT with summary
    4. Call final report LLM
    5. Store result in st.session_state.final_report
    """
    logger.info("Starting finalization sequence")
    logger.info(f"Running final summarization on {len(st.session_state.recent_messages)} messages")
    new_summary = run_summarization(
        st.session_state.summary,
        st.session_state.recent_messages
    )
    st.session_state.summary = new_summary
    logger.info(f"Summary updated, length={len(new_summary)}")

    logger.info("Generating final report")
    prompt = PROMPT_FINAL_REPORT.format(summary=new_summary)
    final_report = call_llm(MODEL_FINAL_REPORT, prompt, [])
    st.session_state.final_report = final_report
    logger.info(f"Final report generated, length={len(final_report)}")


def handle_user_message(user_input: str) -> None:
    """
    Main entry point. Handles a user message through the full flow.
    - Clears st.session_state.error at start
    - Updates session state as needed
    - On exception: sets st.session_state.error with generic message, logs specific error
    """
    st.session_state.error = ""
    logger.info(f"Handling user message: {user_input[:50]}...")

    try:
        st.session_state.recent_messages.append({"role": "user", "content": user_input})
        logger.info(f"Message count: {len(st.session_state.recent_messages)}, turns: {st.session_state.turns_since_summarization}")

        if is_summary_over_threshold(st.session_state.summary):
            logger.info("Summary over threshold, forcing finalization")
            run_finalization()
            return

        system_prompt = PROMPT_CONVERSATIONAL.format(summary=st.session_state.summary)
        logger.info("Calling conversational LLM")

        status, content = call_conversational_llm_with_retry(
            system_prompt,
            st.session_state.recent_messages
        )

        st.session_state.recent_messages.append({"role": "assistant", "content": content})
        st.session_state.status = status
        st.session_state.turns_since_summarization += 1
        logger.info(f"Status set to: {status}, turns now: {st.session_state.turns_since_summarization}")

        if status == "READY":
            logger.info("Status is READY, starting finalization")
            run_finalization()
            return

        if should_summarize(
            st.session_state.summary,
            st.session_state.recent_messages,
            st.session_state.turns_since_summarization
        ):
            logger.info("Summarization triggered")
            new_summary = run_summarization(
                st.session_state.summary,
                st.session_state.recent_messages
            )
            st.session_state.summary = new_summary
            st.session_state.recent_messages = trim_messages_after_summarization(
                st.session_state.recent_messages
            )
            st.session_state.turns_since_summarization = 0
            logger.info(f"Summarization complete, messages trimmed to {len(st.session_state.recent_messages)}")

        logger.info("User message handled successfully")

    except Exception as e:
        logger.error(f"Error handling user message: {e}")
        logger.error(traceback.format_exc())
        st.session_state.error = "An error occurred. Please try again."
