import streamlit as st
from datetime import datetime
from services import AIService, ContentService
from ui.voice import speak_button
from utils import AnalyticsManager
from ui.styles import apply_custom_styles
from ui.navigation import render_page_header

# Page config
st.set_page_config(
    page_title="Vocabulary - AMspeaker",
    page_icon="📚",
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
render_page_header("Speaking Vocabulary", "📚", "Practice vocabulary for natural speaking with AI feedback")

# Initialize services
if "ai_service" not in st.session_state:
    st.session_state.ai_service = AIService()
if "content_service" not in st.session_state:
    st.session_state.content_service = ContentService()
if "analytics" not in st.session_state:
    st.session_state.analytics = AnalyticsManager()

ai_service = st.session_state.ai_service
content_service = st.session_state.content_service
analytics = st.session_state.analytics

# Initialize session state
if "daily_content" not in st.session_state:
    st.session_state.daily_content = {
        "last_updated": None,
        "vocabulary": [],
        "idioms": [],
        "topics": [],
        "exercises": []
    }
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("---")

if st.session_state.daily_content["vocabulary"]:
    vocab_to_use = st.session_state.daily_content["vocabulary"]
    st.info("📅 Using today's auto-updated speaking vocabulary")
else:
    vocab_to_use = content_service.get_default_vocab()
    st.info("📚 Using default vocabulary. Check sidebar to get fresh daily vocabulary.")

for word, meaning, example in vocab_to_use:
    with st.expander(f"{word.title()}"):
        st.write(f"**Meaning:** {meaning}")
        st.write(f"**Speaking Example:** {example}")
        speak_button(f"{word}. {meaning}. Example: {example}", f"Hear {word}")

st.markdown("---")
st.markdown("### Practice Using These Words")

text = st.text_area("Practice using these words in speech", height=160)

if st.button("Practice with AMspeaker"):
    if text.strip():
        feedback, scores = ai_service.ask_ai_teacher(text, "Beginner", "Speaking Vocabulary", "Vocabulary")
        st.session_state.history.append({
            "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "topic": "Speaking Vocabulary",
            "answer": text,
            "feedback": feedback,
            "scores": scores
        })
        analytics.track_interaction("conversation")
        st.markdown(feedback)
        speak_button(feedback)
