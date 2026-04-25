import streamlit as st
from datetime import datetime
from services import AIService
from ui.voice import speak_button
from utils import AnalyticsManager
from ui.styles import apply_custom_styles
from ui.navigation import render_page_header

# Page config
st.set_page_config(
    page_title="Natural Expressions - AMspeaker",
    page_icon="💡",
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
render_page_header("Natural English Expressions", "💡", "Learn and practice natural expressions for fluent speaking")

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

st.markdown("---")

grammar_topic = st.selectbox(
    "Choose Expression Type",
    ["Filler Words", "Transition Phrases", "Agreement Expressions", "Opinion Phrases", "Clarification", "Casual Responses"]
)

st.markdown("---")
st.markdown("### Practice Using Natural Expressions")

text = st.text_area("Practice using natural expressions", height=160)

if st.button("Practice with AMspeaker"):
    if text.strip():
        feedback, scores = ai_service.ask_ai_teacher(text, "Beginner", grammar_topic, "Expressions")
        st.session_state.history.append({
            "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "topic": grammar_topic,
            "answer": text,
            "feedback": feedback,
            "scores": scores
        })
        analytics.track_interaction("conversation")
        st.markdown(feedback)
        speak_button(feedback)
