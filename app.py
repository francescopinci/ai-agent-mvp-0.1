import logging
import streamlit as st

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from config import WELCOME_MESSAGE
from orchestrator import handle_user_message



def show_landing_page():
    st.markdown("""
        <style>
        .hero-section {
            text-align: center;
            padding: 3rem 1rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .hero-title {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .hero-subtitle {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            opacity: 0.95;
        }
        .feature-box {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }
        .cta-button {
            background: #667eea;
            color: white;
            padding: 1rem 3rem;
            font-size: 1.2rem;
            border-radius: 8px;
            border: none;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">🌍 NomaTax</div>
            <div class="hero-subtitle">
                AI-Powered Wealth Management per Expat Italia-USA
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Description
    st.markdown("""
        ### Chi Siamo
        
        **NomaTax** è una piattaforma AI-powered di wealth management personalizzato progettata per aiutare 
        individui che si trasferiscono tra paesi a ottimizzare la loro situazione finanziaria complessiva.
        
        La piattaforma fornisce consulenza su:
    """)
    
    # Features
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-box">
                <h4>💰 Tassazione</h4>
                <p>Ottimizza le tue tasse tra Italia e USA con strategie personalizzate</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <h4>📊 Investimenti</h4>
                <p>Strategie di investimento cross-border e incentivi fiscali</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-box">
                <h4>🏠 Proprietà Immobiliari</h4>
                <p>Consulenza su acquisto, vendita e gestione immobili</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <h4>🎯 Pianificazione Finanziaria</h4>
                <p>Fondi pensionistici e pianificazione finanziaria generale</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # CTA Section
    st.markdown("### 🚀 Inizia la Tua Consulenza Gratuita")
    st.markdown("Rispondi ad alcune domande e ricevi un report personalizzato in pochi minuti.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📝 Inizia Ora", use_container_width=True, type="primary"):
            st.session_state.show_landing = False
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            ⚠️ <strong>Disclaimer:</strong> NomaTax fornisce consulenza generale basata su AI. 
            Consulta sempre un commercialista certificato per decisioni fiscali definitive.
        </div>
    """, unsafe_allow_html=True)




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



if "show_landing" not in st.session_state:
    st.session_state.show_landing = True

# Show landing page first
if st.session_state.show_landing:
    show_landing_page()
else


# Role selection
# Show landing page first
if st.session_state.show_landing:
    show_landing_page()
else:
    # Role selection
    role = st.sidebar.selectbox("Select Role", ["User", "Tax Accountant"])

    if role == "User":
        st.title("Tax Consultation Assistant")
        ...

    
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
            report = st.session_state.final_report
            
            # Save report to user data
            st.session_state.users_data[user_id]['final_report'] = report
            st.session_state.users_data[user_id]['messages'] = st.session_state.recent_messages
            
            # Extract key metrics from report
            import re
            savings_match = re.search(r'Total estimated annual savings:\s*([€$][\d,k\-]+)', report)
            confidence_match = re.search(r'Confidence.*?(🟢|🟡|🔴)', report)
            
            # Dashboard Header
            st.title("📊 Your Tax Strategy Report")
            
            # Key Metrics Row
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Estimated Annual Savings", 
                         savings_match.group(1) if savings_match else "See report")
            with col2:
                confidence = confidence_match.group(1) if confidence_match else "🟡"
                st.metric("Confidence Level", confidence)
            with col3:
                st.metric("Status", "✅ Complete")
            
            st.divider()
            
            # Split report into sections
            sections = report.split("## ")
            
            # Display first section (intro) normally
            if sections[0].strip():
                st.markdown(sections[0])
            
            # Display remaining sections as expandable
            for section in sections[1:]:
                if not section.strip():
                    continue
                    
                lines = section.split('\n', 1)
                title = lines[0].strip()
                content = lines[1] if len(lines) > 1 else ""
                
                # Color code certain sections
                if "SITUATION" in title.upper() or "GLANCE" in title.upper():
                    with st.expander(f"📋 {title}", expanded=True):
                        st.markdown(content)
                elif "OPTIMIZATION" in title.upper() or "SAVINGS" in title.upper():
                    with st.expander(f"💰 {title}", expanded=True):
                        st.markdown(content)
                elif "ACTION" in title.upper() or "NEXT STEPS" in title.upper():
                    with st.expander(f"✅ {title}", expanded=True):
                        st.markdown(content)
                elif "RISK" in title.upper() or "GAP" in title.upper():
                    with st.expander(f"⚠️ {title}", expanded=False):
                        st.markdown(content)
                else:
                    with st.expander(f"{title}", expanded=False):
                        st.markdown(content)
            
            st.divider()
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💬 Continue Asking Questions", use_container_width=True):
                    st.session_state.status = ""
                    st.rerun()
            with col2:
                if st.button("📥 Download Report", use_container_width=True):
                    st.download_button(
                        label="Download as Text",
                        data=report,
                        file_name=f"tax_report_{user_data['name']}.txt",
                        mime="text/plain"
                    )

            with st.expander("📜 View conversation history"):
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
