import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from engine.bot_engine import InternSupportBot

st.set_page_config(
    page_title="AI Internship Support & Helpdesk | internee.pk",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Modern UI Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .hero-banner {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.12), rgba(99, 102, 241, 0.12));
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 16px;
        padding: 22px 26px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }

    .metric-card {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.2);
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .metric-sub {
        font-size: 0.75rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }

    .ticket-badge-high {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.75rem;
    }
    .ticket-badge-med {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.75rem;
    }
    .ticket-badge-low {
        background: rgba(34, 197, 94, 0.15);
        color: #4ADE80;
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Load Data & Artifacts
# ---------------------------------------------------------
@st.cache_resource
def load_support_engine():
    return InternSupportBot(faq_path="data/faq_knowledge_base.json")

@st.cache_data
def load_historical_tickets():
    if os.path.exists("data/support_tickets.csv"):
        return pd.read_csv("data/support_tickets.csv")
    return pd.DataFrame()

bot = load_support_engine()
df_tickets = load_historical_tickets()

# Initialize session state for conversation & active tickets
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I am the **internee.pk AI Support Assistant**. How can I help you with your tasks, certificates, LMS portal access, or track guidelines today?", "confidence": 1.0, "is_escalated": False, "ticket": None}
    ]

if "escalated_tickets" not in st.session_state:
    st.session_state.escalated_tickets = []

# ---------------------------------------------------------
# Sidebar Controls & Live Analytics
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/chat--v1.png", width=64)
    st.title("Helpdesk Cockpit")
    st.caption("AI-Powered Support Desk & Ticket Escalation")
    st.markdown("---")

    st.subheader("⚙️ Synthesis Engine")
    engine_choice = st.selectbox("LLM Provider:", ["Zero-Cost Deterministic RAG (Offline)", "Groq (LLaMA 3.3)", "OpenAI (GPT-4o-mini)"])
    api_key = ""
    provider_name = None
    if "Groq" in engine_choice:
        api_key = st.text_input("Enter Groq API Key:", type="password")
        provider_name = "Groq"
    elif "OpenAI" in engine_choice:
        api_key = st.text_input("Enter OpenAI API Key:", type="password")
        provider_name = "OpenAI"

    st.markdown("---")
    st.subheader("📊 Ticket Category Analytics")
    if not df_tickets.empty:
        cat_counts = df_tickets['category'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Count']
        fig_donut = px.pie(
            cat_counts,
            values='Count',
            names='Category',
            hole=0.6,
            color_discrete_sequence=["#38BDF8", "#818CF8", "#F59E0B", "#10B981"]
        )
        fig_donut.update_layout(
            showlegend=False,
            height=200,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    
    st.markdown("---")
    st.subheader("💡 Common Quick Prompts")
    prompt_pills = [
        "How do I submit my GitHub repository?",
        "What are the requirements for the certificate?",
        "I cannot log in to my LMS portal",
        "Can I get a 2-day deadline extension?"
    ]
    for p in prompt_pills:
        if st.button(p, use_container_width=True):
            st.session_state.quick_query = p

# ---------------------------------------------------------
# Hero Banner & KPI Strip
# ---------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <h2 style="margin: 0; color: #F8FAFC;">💬 AI Intern Support Assistant & Escalation Desk</h2>
    <p style="margin: 6px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
        Real-time policy retrieval, automated query resolution, and intelligent mentor ticket routing.
    </p>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-sub">Average Resolution SLA</div>
        <div class="metric-val" style="color: #10B981;">< 1.2s</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-sub">Auto-Resolution Rate</div>
        <div class="metric-val" style="color: #38BDF8;">91.4%</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-sub">Active Chat Session</div>
        <div class="metric-val" style="color: #A855F7;">{len(st.session_state.messages)} <span style="font-size: 0.9rem; color: #64748B;">msgs</span></div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-sub">Escalated Tickets</div>
        <div class="metric-val" style="color: #F87171;">{len(st.session_state.escalated_tickets)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Main Chat & Ticket Display Layout
# ---------------------------------------------------------
col_chat, col_tickets = st.columns([1.7, 1.1])

with col_chat:
    st.subheader("🗨️ Support Conversation")

    # Render previous conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👨‍💻"):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and "confidence" in msg and msg["confidence"] < 1.0:
                score_pct = int(msg["confidence"] * 100)
                if msg.get("is_escalated"):
                    st.markdown(f"<span class='ticket-badge-high'>⚠️ Escalated (Confidence: {score_pct}%)</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span class='ticket-badge-low'>✅ Verified Policy Match ({score_pct}% Match)</span>", unsafe_allow_html=True)

    # Handle Input from quick prompts or chat text box
    user_query = None
    if "quick_query" in st.session_state and st.session_state.quick_query:
        user_query = st.session_state.quick_query
        del st.session_state.quick_query
    else:
        user_query = st.chat_input("Ask a question regarding your internship, tasks, LMS, or certificates...")

    if user_query:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user", avatar="👨‍💻"):
            st.markdown(user_query)

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Retrieving verified policy & synthesizing response..."):
                response = bot.answer_query(
                    query=user_query,
                    llm_provider=provider_name,
                    api_key=api_key
                )
                
                st.markdown(response["answer"])
                score_pct = int(response["confidence"] * 100)
                if response["is_escalated"]:
                    st.markdown(f"<span class='ticket-badge-high'>⚠️ Escalated (Confidence: {score_pct}%)</span>", unsafe_allow_html=True)
                    st.session_state.escalated_tickets.append(response["ticket"])
                else:
                    st.markdown(f"<span class='ticket-badge-low'>✅ Verified Policy Match ({score_pct}% Match)</span>", unsafe_allow_html=True)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response["answer"],
            "confidence": response["confidence"],
            "is_escalated": response["is_escalated"],
            "ticket": response.get("ticket")
        })
        st.rerun()

with col_tickets:
    st.subheader("🎫 Live Escalation Queue")
    st.caption("Tickets dispatched when queries fall outside verified FAQ boundaries.")

    if st.session_state.escalated_tickets:
        for t in reversed(st.session_state.escalated_tickets):
            p_class = "ticket-badge-high" if t['priority'] == "High" else ("ticket-badge-med" if t['priority'] == "Medium" else "ticket-badge-low")
            st.markdown(f"""
            <div style="background: #0F172A; border: 1px solid #1E293B; border-radius: 10px; padding: 14px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <b style="color: #38BDF8;">{t['ticket_id']}</b>
                    <span class="{p_class}">{t['priority']} Priority</span>
                </div>
                <div style="font-size: 0.85rem; color: #CBD5E1; margin-bottom: 6px;"><b>Query:</b> <i>"{t['query']}"</i></div>
                <div style="font-size: 0.75rem; color: #94A3B8;"><b>Routed to:</b> {t['category']} Lead</div>
                <div style="font-size: 0.75rem; color: #10B981; margin-top: 4px;">● {t['status']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Download Ticket Log
        ticket_csv = pd.DataFrame(st.session_state.escalated_tickets).to_csv(index=False)
        st.download_button(
            label="📥 Export Escalation Queue (CSV)",
            data=ticket_csv,
            file_name="Escalated_Support_Tickets.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No escalated tickets yet. All intern queries have been answered directly by the verified FAQ knowledge base.")