import logging
import streamlit as st

# Configure logging for Streamlit
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from config import WELCOME_MESSAGE
from orchestrator import handle_user_message

# Initialize session state
if "summary" not in st.session_state:
    st.session_state.summary = ""

if "recent_messages" not in st.session_state:
    st.session_state.recent_messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]

if "status" not in st.session_state:
    st.session_state.status = ""

if "error" not in st.session_state:
    st.session_state.error = ""

if "turns_since_summarization" not in st.session_state:
    st.session_state.turns_since_summarization = 0

if "final_report" not in st.session_state:
    st.session_state.final_report = ""

# Error display
if st.session_state.error:
    st.error(st.session_state.error)

# Main content
if st.session_state.status == "READY":
    st.header("Your Report")
    st.markdown(st.session_state.final_report)

    with st.expander("View conversation history"):
        for msg in st.session_state.recent_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
else:
    # Display chat history
    for msg in st.session_state.recent_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    if user_input := st.chat_input("Type your message..."):
        # Add user message to state and display immediately
        st.session_state.recent_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Process message (orchestrator adds assistant response to state)
        handle_user_message(user_input)

        # Display error or assistant response
        if st.session_state.error:
            st.error(st.session_state.error)
        elif st.session_state.recent_messages[-1]["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write(st.session_state.recent_messages[-1]["content"])

        # Rerun to ensure consistent display from session state
        st.rerun()
