import streamlit as st
from datetime import datetime
from services import AIService
from ui.voice import speak_button
from utils import AnalyticsManager
from config.settings import config
from ui.styles import apply_custom_styles
from ui.navigation import render_page_header

# Page config
st.set_page_config(
    page_title="News Vocabulary - AMspeaker",
    page_icon="📰",
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
render_page_header("Daily News Vocabulary & Idioms", "📰", "Learn vocabulary and idioms from today's news articles")

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

with st.spinner("Fetching today's news and extracting vocabulary..."):
    try:
        news_prompt = "Extract 5-8 vocabulary words and 3-5 idioms from today's current news topics (technology, business, world events, etc.). For each vocabulary word, provide: the word, definition, and example sentence from news context. For each idiom, provide: the idiom, meaning, and example sentence. Format: VOCABULARY: 1. Word - Definition - Example, IDIOMS: 1. Idiom - Meaning - Example"
        
        from openai import OpenAI
        client = OpenAI(
            base_url=config.api_base_url,
            api_key=config.api_key
        )
        
        response = client.chat.completions.create(
            model=config.model_name,
            messages=[
                {"role": "user", "content": news_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        news_content = response.choices[0].message.content
        st.markdown(news_content)
        
        st.divider()
        st.markdown("### Practice with News Vocabulary")
        
        practice_text = st.text_area("Practice using these news vocabulary words in a sentence or conversation:", height=100)
        
        if st.button("Practice with AI"):
            if practice_text.strip():
                with st.spinner("AI is analyzing your usage..."):
                    feedback, scores = ai_service.ask_ai_teacher(practice_text, "Intermediate", "News Vocabulary", "News Practice")
                    st.session_state.history.append({
                        "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
                        "topic": "News Vocabulary",
                        "answer": practice_text,
                        "feedback": feedback,
                        "scores": scores
                    })
                    analytics.track_interaction("conversation")
                st.markdown(feedback)
                speak_button(feedback, "Listen to Feedback")
            else:
                st.warning("Please write something to practice.")
                
    except Exception as e:
        st.error(f"Error fetching news vocabulary: {str(e)}")
        st.info("Please try again later or check your internet connection.")
