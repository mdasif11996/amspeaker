import logging
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import modular components
from config.settings import config
from services import ContentService
from ui.styles import apply_custom_styles
from ui.navigation import render_advanced_sidebar
from utils import AnalyticsManager

# Initialize Streamlit page config
st.set_page_config(
    page_title="AMspeaker - AI English Speaking Coach",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Validate configuration
try:
    config.validate()
except ValueError as e:
    logger.error(f"Configuration validation failed: {e}")
    st.error(f"Configuration error: {e}")
    st.stop()

# Initialize services
content_service = ContentService()
analytics = AnalyticsManager()

logger.info(f"AMspeaker v{config.app_version} starting in {config.environment} mode")

# Apply custom styles
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
    render_advanced_sidebar()

# Initialize session state
if "daily_content" not in st.session_state:
    st.session_state.daily_content = {
        "last_updated": None,
        "vocabulary": [],
        "idioms": [],
        "topics": [],
        "exercises": []
    }

if "dynamic_topics" not in st.session_state:
    st.session_state.dynamic_topics = content_service.generate_dynamic_topics("Intermediate")
    st.session_state.last_topic_level = "Intermediate"

# Auto-update daily content if enabled and needed
if st.session_state.get("auto_update_enabled", False):
    updated_content = content_service.update_daily_content(st.session_state.daily_content)
    if updated_content:
        st.session_state.daily_content = updated_content
        if updated_content.get("topics"):
            st.session_state.dynamic_topics = updated_content.get("topics")

# Render hero section
st.markdown("""
<div class="hero">
    <h1>🎙️ AMspeaker - Your AI English Speaking Coach</h1>
    <p style="font-size: 18px; margin-top: 10px;">
        Master spoken English with AI-powered conversations. 
        Build confidence, fluency, and natural communication skills through interactive practice.
    </p>
    <div style="margin-top: 20px; display: flex; gap: 15px; flex-wrap: wrap;">
        <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; font-size: 14px;">
            🎙️ Voice Input
        </span>
        <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; font-size: 14px;">
            💬 Real Conversation
        </span>
        <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; font-size: 14px;">
            🔊 Audio Feedback
        </span>
        <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; font-size: 14px;">
            📊 Progress Tracking
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# Render practice mode cards
st.markdown("## Choose Your Practice Mode")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💬", key="card_conv", use_container_width=True, help="Conversation Practice"):
        st.switch_page("pages/1_Conversation.py")
    st.markdown("**Conversation**")
    st.caption("Natural AI conversations")

with col2:
    if st.button("🎤", key="card_voice", use_container_width=True, help="Voice Chat"):
        st.switch_page("pages/2_Voice_Chat.py")
    st.markdown("**Voice Chat**")
    st.caption("Voice-to-voice practice")

with col3:
    if st.button("📚", key="card_vocab", use_container_width=True, help="Vocabulary"):
        st.switch_page("pages/3_Vocabulary.py")
    st.markdown("**Vocabulary**")
    st.caption("Speaking vocabulary")

with col4:
    if st.button("💼", key="card_interview", use_container_width=True, help="Interview"):
        st.switch_page("pages/6_Interview.py")
    st.markdown("**Interview**")
    st.caption("Job interview prep")

st.write("")

col5, col6, col7, col8 = st.columns(4)

with col5:
    if st.button("💡", key="card_expr", use_container_width=True, help="Expressions"):
        st.switch_page("pages/4_Expressions.py")
    st.markdown("**Expressions**")
    st.caption("Natural expressions")

with col6:
    if st.button("🎯", key="card_idioms", use_container_width=True, help="Idioms"):
        st.switch_page("pages/5_Idioms.py")
    st.markdown("**Idioms**")
    st.caption("Native-like speech")

with col7:
    if st.button("📰", key="card_news", use_container_width=True, help="News"):
        st.switch_page("pages/8_News.py")
    st.markdown("**News**")
    st.caption("Current events")

with col8:
    if st.button("📊", key="card_progress", use_container_width=True, help="Progress"):
        st.switch_page("pages/7_Progress.py")
    st.markdown("**Progress**")
    st.caption("Track improvement")

st.markdown("---")
st.markdown("### Quick Start Guide")
st.markdown("""
1. **Select a practice mode** from the sidebar or cards above
2. **Choose your level** (Beginner, Intermediate, or Advanced)
3. **Start speaking** - use voice input or type your message
4. **Get instant feedback** with AI-powered analysis
5. **Track your progress** over time

**Tips:**
- Use Chrome or Edge for the best voice input experience
- Allow microphone permission when prompted
- Practice daily for best results
- Try different conversation modes (Casual, Interview, Formal, etc.)
""")

st.divider()
st.caption("Use Chrome/Edge for voice input. Allow microphone permission in your browser if needed.")
