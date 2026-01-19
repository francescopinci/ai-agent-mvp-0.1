import logging
import os
import time

import streamlit as st
from openai import OpenAI, APIConnectionError, RateLimitError, APITimeoutError, AuthenticationError

logger = logging.getLogger(__name__)


def get_api_key() -> str:
    try:
        return st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        pass
    if "OPENAI_API_KEY" in os.environ:
        return os.environ["OPENAI_API_KEY"]
    raise ValueError("OPENAI_API_KEY not found in st.secrets or environment variables")


def call_llm(model: str, developer_prompt: str, messages: list[dict]) -> str:
    """
    Call OpenAI API with developer role for instructions.

    The 'developer' role (replacing legacy 'system' role) provides instructions
    that have higher priority than user messages and cannot be overridden by users.
    """
    logger.info(f"Calling LLM model={model}, messages_count={len(messages)}")
    client = OpenAI(api_key=get_api_key())

    full_messages = [{"role": "developer", "content": developer_prompt}] + messages

    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"API call attempt {attempt + 1}/{max_retries}")
            response = client.chat.completions.create(
                model=model,
                messages=full_messages
            )
            content = response.choices[0].message.content
            logger.info(f"API call successful, response length={len(content)}")
            return content
        except AuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            raise
        except (RateLimitError, APITimeoutError, APIConnectionError) as e:
            logger.warning(f"Retryable error on attempt {attempt + 1}: {type(e).__name__}: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                logger.error(f"All {max_retries} attempts failed")
                raise
