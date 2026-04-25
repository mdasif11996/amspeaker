import streamlit as st
from datetime import datetime
from services import AIService
from ui.voice import speak_button, browser_speech_input
from utils import AnalyticsManager
from ui.styles import apply_custom_styles
from ui.navigation import render_page_header

# Page config
st.set_page_config(
    page_title="Voice Chat - AMspeaker",
    page_icon="🎤",
    layout="wide"
)

apply_custom_styles()

# Mobile navigation toggle
st.markdown("""
<button id="mobileNavToggle" class="mobile-nav-toggle" onclick="toggleMobileNav()">
    ☰ Menu
</button>
<script>
function toggleMobileNav() {
    const sidebar = document.querySelector('.css-1d391kg');
    if (sidebar) {
        sidebar.classList.toggle('mobile-visible');
    }
}
</script>
""", unsafe_allow_html=True)

# Render advanced sidebar
with st.sidebar:
    from ui.navigation import render_advanced_sidebar
    render_advanced_sidebar()

# Render page header
render_page_header("Voice Chat", "🎤", "Pure voice-to-voice conversation practice")

# Initialize services
if "ai_service" not in st.session_state:
    st.session_state.ai_service = AIService()
if "analytics" not in st.session_state:
    st.session_state.analytics = AnalyticsManager()

ai_service = st.session_state.ai_service
analytics = st.session_state.analytics

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = "Welcome to AMspeaker Voice Chat! Speak naturally and I'll respond."

st.markdown("---")

st.markdown("### Your Voice Input")
browser_speech_input()

st.markdown("### Or Type Your Message")
user_voice_text = st.text_area("Type your message here:", height=120, key="voice_chat_input", placeholder="Type or paste your speech here...")

if st.session_state.history:
    st.markdown("---")
    st.markdown("### Recent Conversation")
    for h in st.session_state.history[-3:]:
        with st.chat_message("user"):
            st.write(h["answer"])
        with st.chat_message("assistant"):
            st.write(h["feedback"])

col_send, col_clear = st.columns([3, 1])
with col_send:
    if st.button("Send to AI Teacher", type="primary", use_container_width=True):
        user_text = user_voice_text
        
        if user_text.strip():
            with st.spinner("AI is responding..."):
                feedback, scores = ai_service.ask_ai_teacher(user_text, "Intermediate", "Voice Chat", "Voice")
                st.session_state.history.append({
                    "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
                    "topic": "Voice Chat",
                    "answer": user_text,
                    "feedback": feedback,
                    "scores": scores
                })
                st.session_state.last_feedback = feedback
                analytics.track_interaction("conversation")
                
                st.markdown("### AI Voice Response")
                st.markdown(feedback)
                speak_button(feedback, "Hear AI Response")
                
                st.markdown("---")
                st.markdown("### Speaking Metrics")
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Overall", f"{scores.get('overall', 0)}/100")
                with col_m2:
                    st.metric("Fluency", f"{scores.get('fluency', 0)}/100")
                with col_m3:
                    st.metric("Communication", f"{scores.get('communication', 0)}/100")
                
                if scores.get('fluency', 0) < 70:
                    st.warning("Practice speaking more fluently by using natural expressions and reducing pauses.")
                elif scores.get('fluency', 0) < 85:
                    st.info("Good fluency! Try to speak more smoothly with fewer hesitations.")
                else:
                    st.success("Excellent fluency! Your speech flows naturally.")

with col_clear:
    if st.button("Clear History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

st.markdown("---")
st.info("💡 Tip: Click 'Speak Now' in the voice input box, then copy the text and paste it above, or type directly!")
