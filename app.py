import logging
import streamlit as st

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from config import WELCOME_MESSAGE
from orchestrator import handle_user_message

# Initialize session state
if "users_data" not in st.session_state:
    st.session_state.users_data = {}

if "current_user_id" not in st.session_state:
    st.session_state.current_user_id = None

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

# Role selection
role = st.sidebar.selectbox("Select Role", ["User", "Tax Accountant"])

if role == "User":
    st.title("Tax Consultation Assistant")
    
    # User identification
    if not st.session_state.current_user_id:
        st.subheader("Welcome! Please identify yourself")
        user_name = st.text_input("Your Name")
        user_email = st.text_input("Your Email")
        
        if st.button("Start Consultation") and user_name and user_email:
            user_id = f"{user_name}_{user_email}"
            st.session_state.current_user_id = user_id
            
            if user_id not in st.session_state.users_data:
                st.session_state.users_data[user_id] = {
                    'name': user_name,
                    'email': user_email,
                    'messages': st.session_state.recent_messages.copy(),
                    'final_report': "",
                    'support_requested': False
                }
            else:
                # Load existing user data
                st.session_state.recent_messages = st.session_state.users_data[user_id]['messages']
                st.session_state.final_report = st.session_state.users_data[user_id]['final_report']
            
            st.rerun()
    else:
        # Existing chat interface
        user_id = st.session_state.current_user_id
        user_data = st.session_state.users_data[user_id]
        
        st.sidebar.write(f"**User:** {user_data['name']}")
        if st.sidebar.button("Request Human Accountant"):
            st.session_state.users_data[user_id]['support_requested'] = True
            st.sidebar.success("Support requested!")
        
        if st.sidebar.button("Logout"):
            st.session_state.current_user_id = None
            st.rerun()
        
        # Error display
        if st.session_state.error:
            st.error(st.session_state.error)

        # Main content
        if st.session_state.status == "READY":
            st.header("Your Report")
            st.markdown(st.session_state.final_report)
            
            # Save report to user data
            st.session_state.users_data[user_id]['final_report'] = st.session_state.final_report
            st.session_state.users_data[user_id]['messages'] = st.session_state.recent_messages

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
                st.session_state.recent_messages.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.write(user_input)

                handle_user_message(user_input)
                
                # Save to user data
                st.session_state.users_data[user_id]['messages'] = st.session_state.recent_messages

                if st.session_state.error:
                    st.error(st.session_state.error)
                elif st.session_state.recent_messages[-1]["role"] == "assistant":
                    with st.chat_message("assistant"):
                        st.write(st.session_state.recent_messages[-1]["content"])

                st.rerun()

else:  # Tax Accountant
    st.title("Tax Accountant Dashboard")
    
    if not st.session_state.users_data:
        st.info("No user consultations yet.")
    else:
        show_all = st.checkbox("Show All Users", value=False)
        
        for user_id, data in st.session_state.users_data.items():
            if show_all or data['support_requested']:
                status = "🔴 SUPPORT REQUESTED" if data['support_requested'] else "✅ Active"
                
                with st.expander(f"{data['name']} ({data['email']}) - {status}"):
                    st.write(f"**Email:** {data['email']}")
                    st.write(f"**Messages:** {len(data['messages'])}")
                    
                    if data['final_report']:
                        st.subheader("Final Report")
                        st.markdown(data['final_report'])
                    
                    st.subheader("Conversation History")
                    for msg in data['messages']:
                        st.write(f"**{msg['role'].upper()}:** {msg['content']}")
                        st.divider()
