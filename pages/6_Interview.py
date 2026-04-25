import streamlit as st
from datetime import datetime
from services import AIService
from ui.voice import speak_button
from utils import AnalyticsManager
from ui.styles import apply_custom_styles
from ui.navigation import render_page_header

# Page config
st.set_page_config(
    page_title="Interview Practice - AMspeaker",
    page_icon="💼",
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
render_page_header("Interview Speaking Practice", "💼", "Practice answering common interview questions with AI feedback")

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

INTERVIEW = [
    "Tell me about yourself.",
    "Why should we hire you?",
    "What are your strengths?",
    "Explain your project.",
    "Where do you see yourself in five years?",
    "What is your greatest weakness?",
    "Why do you want to work here?",
    "Describe a challenging situation you overcame."
]

question = st.selectbox("Interview Question", INTERVIEW)
st.info(question)

st.markdown("---")
st.markdown("### Practice Your Answer")

text = st.text_area("Practice your spoken answer", height=180)

if st.button("Practice with AMspeaker"):
    if text.strip():
        feedback, scores = ai_service.ask_ai_teacher(text, "Intermediate", question, "Interview")
        st.session_state.history.append({
            "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "topic": question,
            "answer": text,
            "feedback": feedback,
            "scores": scores
        })
        analytics.track_interaction("conversation")
        st.markdown(feedback)
        speak_button(feedback)
