import streamlit as st

from orchestrator import handle_user_message

# Initialize session state
if "summary" not in st.session_state:
    st.session_state.summary = ""

if "recent_messages" not in st.session_state:
    st.session_state.recent_messages = []

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
    st.text_area(
        label="Report",
        value=st.session_state.final_report,
        height=400,
        disabled=True
    )
else:
    # Chat display - simple text
    for msg in st.session_state.recent_messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        st.write(f"**{role}:** {msg['content']}")

# Input (hidden after finalization)
if st.session_state.status != "READY":
    user_input = st.chat_input("Type your message...")
    if user_input:
        handle_user_message(user_input)
        st.rerun()
