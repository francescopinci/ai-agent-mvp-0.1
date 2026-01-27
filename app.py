import logging
import streamlit as st

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from config import WELCOME_MESSAGE
from orchestrator import handle_user_message

def show_landing_page():
    # Language toggle
    lang = st.sidebar.radio("🌐 Language / Lingua", ["English", "Italiano"])
    
    if lang == "English":
        show_landing_english()
    else:
        show_landing_italian()

def show_landing_english():
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
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">🌍 NomaTax</div>
            <div class="hero-subtitle">
                AI-Powered Cross-Border Wealth Optimization
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        ### What is NomaTax?
        
        **NomaTax** is an AI-powered platform designed to optimize taxation and wealth management 
        for individuals living between two countries.
        
        **Currently optimized for:** 🇮🇹 Italy - 🇺🇸 USA  
        **Coming soon:** All major countries worldwide
        
        ---
        
        ### Complete Wealth Optimization
        
        NomaTax helps you optimize every aspect of your financial life:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-box">
                <h4>💰 Tax Optimization</h4>
                <p>Minimize taxes across both countries with personalized strategies and special regimes</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <h4>📊 Investment Management</h4>
                <p>Cross-border investment strategies, tax-advantaged accounts, and capital gains optimization</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <h4>🏠 Real Estate</h4>
                <p>Property purchase/sale strategies, rental income optimization, and capital gains planning</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-box">
                <h4>📈 Stocks & Securities</h4>
                <p>RSU/equity compensation, stock options, QSBS strategies, and dividend optimization</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <h4>🎯 Pension Planning</h4>
                <p>401(k), IRA, INPS coordination, and retirement account optimization</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <h4>💼 Complete Wealth Tracking</h4>
                <p>Centralized view of all your assets, liabilities, and financial obligations across countries</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🚀 Get Started")
    st.markdown("Choose your role to continue:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 I Need Tax Help", use_container_width=True, type="primary"):
            st.session_state.show_landing = False
            st.session_state.selected_role = "User"
            st.rerun()
    with col2:
        if st.button("👨💼 I'm a Tax Accountant", use_container_width=True):
            st.session_state.show_landing = False
            st.session_state.selected_role = "Tax Accountant"
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            ⚠️ <strong>Disclaimer:</strong> NomaTax provides general AI-based guidance. 
            Always consult a certified tax professional (CPA in US, commercialista in Italy) for final decisions.
        </div>
    """, unsafe_allow_html=True)

def show_landing_italian():
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
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">🌍 NomaTax</div>
            <div class="hero-subtitle">
                Ottimizzazione Patrimoniale Cross-Border con AI
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        ### Cos'è NomaTax?
        
        **NomaTax** è una piattaforma AI-powered progettata per ottimizzare la tassazione e la gestione 
        patrimoniale per individui che vivono tra due paesi.
        
        **Attualmente ottimizzato per:** 🇮🇹 Italia - 🇺🇸 USA  
        **Prossimamente:** Tutti i principali paesi del mondo
        
        ---
        
        ### Ottimizzazione Patrimoniale Completa
        
        NomaTax ti aiuta a ottimizzare ogni aspetto della tua vita finanziaria:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-box">
                <h4>💰 Ottimizzazione Fiscale</h4>
                <p>Minimizza le tasse in entrambi i paesi con strategie personalizzate e regimi speciali</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <h4>📊 Gestione Investimenti</h4>
                <p>Strategie di investimento cross-border, conti agevolati e ottimizzazione capital gains</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <h4>🏠 Immobiliare</h4>
                <p>Strategie acquisto/vendita, ottimizzazione redditi da locazione e plusvalenze</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-box">
                <h4>📈 Azioni & Titoli</h4>
                <p>RSU/equity compensation, stock options, strategie QSBS e ottimizzazione dividendi</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <h4>🎯 Pianificazione Pensionistica</h4>
                <p>Coordinamento 401(k), IRA, INPS e ottimizzazione conti pensionistici</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-box">
                <h4>💼 Tracciamento Patrimoniale Completo</h4>
                <p>Vista centralizzata di tutti i tuoi asset, passività e obblighi finanziari tra paesi</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🚀 Inizia Ora")
    st.markdown("Scegli il tuo ruolo per continuare:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 Ho Bisogno di Aiuto Fiscale", use_container_width=True, type="primary"):
            st.session_state.show_landing = False
            st.session_state.selected_role = "User"
            st.rerun()
    with col2:
        if st.button("👨💼 Sono un Commercialista", use_container_width=True):
            st.session_state.show_landing = False
            st.session_state.selected_role = "Tax Accountant"
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

if "selected_role" not in st.session_state:
    st.session_state.selected_role = "User"

# Show landing page first
if st.session_state.show_landing:
    show_landing_page()
else:
    # Back to home button
    if st.sidebar.button("🏠 Back to Home"):
        st.session_state.show_landing = True
        st.session_state.current_user_id = None
        st.rerun()
    
    # Use selected role from landing page
    role = st.session_state.selected_role

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
                    st.session_state.recent_messages = st.session_state.users_data[user_id]['messages']
                    st.session_state.final_report = st.session_state.users_data[user_id]['final_report']
                
                st.rerun()
        else:
            user_id = st.session_state.current_user_id
            user_data = st.session_state.users_data[user_id]
            
            st.sidebar.write(f"**User:** {user_data['name']}")
            if st.sidebar.button("Request Human Accountant"):
                st.session_state.users_data[user_id]['support_requested'] = True
                st.sidebar.success("Support requested!")
            
            if st.sidebar.button("Logout"):
                st.session_state.current_user_id = None
                st.rerun()
            
            if st.session_state.error:
                st.error(st.session_state.error)

            if st.session_state.status == "READY":
                report = st.session_state.final_report
                
                st.session_state.users_data[user_id]['final_report'] = report
                st.session_state.users_data[user_id]['messages'] = st.session_state.recent_messages
                
                import re
                savings_match = re.search(r'Total estimated annual savings:\s*([€$][\d,k\-]+)', report)
                confidence_match = re.search(r'Confidence.*?(🟢|🟡|🔴)', report)
                
                st.title("📊 Your Tax Strategy Report")
                
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
                
                sections = report.split("## ")
                
                if sections[0].strip():
                    st.markdown(sections[0])
                
                for section in sections[1:]:
                    if not section.strip():
                        continue
                        
                    lines = section.split('\n', 1)
                    title = lines[0].strip()
                    content = lines[1] if len(lines) > 1 else ""
                    
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
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💬 Continue Asking Questions", use_container_width=True):
                        st.session_state.status = ""
                        st.rerun()
                with col2:
                    st.download_button(
                        label="📥 Download Report",
                        data=report,
                        file_name=f"tax_report_{user_data['name']}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                with st.expander("📜 View conversation history"):
                    for msg in st.session_state.recent_messages:
                        with st.chat_message(msg["role"]):
                            st.write(msg["content"])

            else:
                for msg in st.session_state.recent_messages:
                    with st.chat_message(msg["role"]):
                        st.write(msg["content"])

                if user_input := st.chat_input("Type your message..."):
                    st.session_state.recent_messages.append({"role": "user", "content": user_input})
                    with st.chat_message("user"):
                        st.write(user_input)

                    handle_user_message(user_input)
                    
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

            
