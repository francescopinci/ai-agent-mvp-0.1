import os
import time

import streamlit as st
from openai import OpenAI, APIConnectionError, RateLimitError, APITimeoutError, AuthenticationError


def get_api_key() -> str:
    try:
        return st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        pass
    if "OPENAI_API_KEY" in os.environ:
        return os.environ["OPENAI_API_KEY"]
    raise ValueError("OPENAI_API_KEY not found in st.secrets or environment variables")


def call_llm(model: str, system_prompt: str, messages: list[dict]) -> str:
    client = OpenAI(api_key=get_api_key())

    full_messages = [{"role": "system", "content": system_prompt}] + messages

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=full_messages
            )
            return response.choices[0].message.content
        except AuthenticationError:
            raise
        except (RateLimitError, APITimeoutError, APIConnectionError):
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                raise
