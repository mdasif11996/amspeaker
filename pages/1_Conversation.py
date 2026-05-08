import streamlit as st
from datetime import datetime
from services import AIService, ContentService
from ui.voice import speak_button, browser_speech_input
from ui.ai_voice import ai_voice_player, voice_selector, get_voice_info
from utils import AnalyticsManager
from ui.styles import apply_custom_styles
from ui.navigation import render_page_header

# Page config
st.set_page_config(
    page_title="Conversation Practice - AMspeaker",
    page_icon="💬",
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
render_page_header("Conversation Practice", "💬", "Natural AI conversations with real-time feedback")

# Initialize services
if "ai_service" not in st.session_state:
    st.session_state.ai_service = AIService(api_key=st.session_state.get("api_key"))
if "content_service" not in st.session_state:
    st.session_state.content_service = ContentService(api_key=st.session_state.get("api_key"))
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

if "dynamic_topics" not in st.session_state:
    st.session_state.dynamic_topics = content_service.generate_dynamic_topics("Intermediate")
    st.session_state.last_topic_level = "Intermediate"

if "history" not in st.session_state:
    st.session_state.history = []

if "memory" not in st.session_state:
    st.session_state.memory = []

if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = "Welcome to AMspeaker! I'm here to help you improve your spoken English. Let's practice together!"

if "ai_voice" not in st.session_state:
    st.session_state.ai_voice = "alloy"

if "auto_speak_ai" not in st.session_state:
    st.session_state.auto_speak_ai = False

st.markdown("---")

col_level, col_topic, col_mode = st.columns([1, 2, 1])
with col_level:
    level = st.selectbox("Your Level", ["Beginner", "Intermediate", "Advanced"], help="Select your English proficiency level")
with col_topic:
    if st.session_state.daily_content["topics"] and not content_service.should_update_daily_content(st.session_state.daily_content.get("last_updated")):
        available_topics = st.session_state.daily_content["topics"]
    else:
        if level != st.session_state.last_topic_level:
            with st.spinner("Generating personalized topics..."):
                st.session_state.dynamic_topics = content_service.generate_dynamic_topics(level)
                st.session_state.last_topic_level = level
        available_topics = st.session_state.dynamic_topics
    
    topic = st.selectbox("Topic", available_topics, help="AI-generated conversation topics for your level")
with col_mode:
    conversation_mode = st.selectbox(
        "Conversation Mode",
        ["Casual", "Interview", "Formal", "Debate", "Storytelling"],
        help="Choose the conversation style"
    )

st.markdown(f"""
<div style="background: linear-gradient(135deg, #e0f2fe, #f0f9ff); padding: 12px; border-radius: 12px; border-left: 4px solid #0ea5e9;">
    <strong>Current Topic:</strong> {topic} | <strong>Mode:</strong> {conversation_mode}
</div>
""", unsafe_allow_html=True)

# Chat history display
if st.session_state.memory:
    st.markdown("### Recent Conversation")
    for i, msg in enumerate(st.session_state.memory[-5:]):
        st.markdown(f"""
        <div style="background: #f1f5f9; padding: 12px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #0ea5e9;">
            <strong>You:</strong> {msg['student']}
        </div>
        <div style="background: linear-gradient(135deg, #ede9fe, #ddd6fe); padding: 12px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #8b5cf6;">
            <strong>AI:</strong> {msg['teacher']}
        </div>
        """, unsafe_allow_html=True)
    st.divider()

st.markdown("### Voice-to-Voice Conversation")
st.info("Speak naturally to the AI teacher! The AI will respond with voice. Allow microphone permission in your browser when prompted.")

browser_speech_input()

st.markdown("---")
st.markdown("### Or Type Your Message")

user_text = st.text_area(
    "Type your message",
    height=100,
    placeholder="Type your message here...",
    label_visibility="collapsed",
    key="user_input_text"
)

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    if st.button("Send to AI Teacher", type="primary", help="Send your message and get AI voice response", use_container_width=True):
        if user_text.strip():
            with st.spinner("AI is thinking of a natural response..."):
                feedback, scores = ai_service.ask_ai_teacher(
                    user_text, level, topic, "Conversation", 
                    conversation_mode, st.session_state.memory
                )
                st.session_state.history.append({
                    "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
                    "topic": topic,
                    "answer": user_text,
                    "feedback": feedback,
                    "scores": scores
                })
                st.session_state.memory.append({"student": user_text, "teacher": feedback})
                st.session_state.last_feedback = feedback
                analytics.track_interaction("conversation")
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f0f9ff, #e0f2fe); padding: 20px; border-radius: 16px; border: 2px solid #0ea5e9; margin: 15px 0;">
                <strong>AI Voice Response ({conversation_mode} Mode):</strong>
                <div style="margin-top: 10px; line-height: 1.6;">
                    {feedback}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Speaking Metrics")
            cols = st.columns(6)
            cols[0].metric("Overall", f"{scores['overall']}/100")
            cols[1].metric("Grammar", f"{scores['grammar']}/100")
            cols[2].metric("Vocabulary", f"{scores['vocabulary']}/100")
            cols[3].metric("Fluency", f"{scores['fluency']}/100")
            cols[4].metric("Naturalness", f"{scores['communication']}/100")
            cols[5].metric("Pronunciation", f"{scores['pronunciation']}/100")
            
            st.markdown("### Pronunciation & Speaking Feedback")
            if scores['pronunciation'] < 70:
                st.warning("Focus on clear pronunciation and word stress")
            elif scores['pronunciation'] >= 90:
                st.success("Excellent pronunciation!")
            else:
                st.info("Good pronunciation - keep practicing!")
            
            if scores['fluency'] < 70:
                st.warning("Try to speak more smoothly and reduce pauses")
            elif scores['fluency'] >= 90:
                st.success("Excellent fluency!")
            else:
                st.info("Good fluency - aim for more natural flow")
            
            st.markdown("### 🎧 AI Voice Response")
            
            # AI Voice Selection
            st.markdown("#### Choose AI Voice")
            if "ai_voice" not in st.session_state:
                st.session_state.ai_voice = "alloy"
            
            col_voice1, col_voice2 = st.columns([2, 1])
            with col_voice1:
                selected_voice = st.selectbox(
                    "Select AI Voice:",
                    options=list(get_voice_info().keys()),
                    index=list(get_voice_info().keys()).index(st.session_state.ai_voice) if st.session_state.ai_voice in get_voice_info() else 0,
                    key="ai_voice_selector"
                )
                st.session_state.ai_voice = selected_voice
            
            with col_voice2:
                if st.button("🔄 Reset Voice", help="Reset to default voice", key="reset_voice"):
                    st.session_state.ai_voice = "alloy"
                    st.rerun()
            
            # Display voice info
            voice_info = get_voice_info()
            current_voice_info = voice_info.get(st.session_state.ai_voice, voice_info["alloy"])
            st.markdown(f"""
            <div style="background: rgba(14, 165, 233, 0.1); padding: 12px; border-radius: 8px; margin: 8px 0;">
                <strong>🎙️ Current Voice:</strong> {current_voice_info["name"]}
                <br><small>{current_voice_info["description"]}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # AI Voice Player with OpenAI TTS
            st.markdown("#### AI Voice Player (OpenAI Enhanced)")
            
            # Auto-speak toggle
            auto_speak = st.checkbox(
                "🔊 Auto-play AI responses",
                value=st.session_state.get("auto_speak_ai", False),
                help="Automatically play AI responses using OpenAI's natural voice"
            )
            st.session_state.auto_speak_ai = auto_speak
            
            ai_voice_html = ai_voice_player(
                text=feedback,
                voice=st.session_state.ai_voice,
                auto_play=auto_speak
            )
            st.markdown(ai_voice_html, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 📝 Fluency Feedback Summary")
            fluency_feedback = f"""
            Your fluency score is {scores['fluency']}/100. 
            {'Great job! Your speech flows naturally.' if scores['fluency'] >= 80 else 'Keep practicing to improve your speech flow.'}
            Focus on: {'Speaking more smoothly and reducing pauses' if scores['fluency'] < 70 else 'Maintaining your natural speaking rhythm'}
            """
            st.info(fluency_feedback)
            speak_button(fluency_feedback, "🔊 Play Fluency Feedback")
            
            st.session_state.user_input_text = ""
        else:
            st.warning("Please speak or type something first to start the voice conversation.")

with col2:
    if st.button("Clear Chat History", help="Clear all conversation history to start fresh", use_container_width=True):
        st.session_state.memory = []
        st.rerun()

with col3:
    if st.button("Start New Topic", help="Clear chat and start fresh", use_container_width=True):
        st.session_state.memory = []
        st.rerun()

st.divider()
st.markdown("### Speaking Exercises")

if st.button("Generate Personalized Exercise"):
    with st.spinner("AI is creating a custom exercise for you..."):
        weakness = "overall"
        if st.session_state.history:
            latest = st.session_state.history[-1]["scores"]
            weakness = min(latest, key=latest.get)
        exercise = ai_service.generate_dynamic_exercise(level, topic, conversation_mode, weakness)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); padding: 16px; border-radius: 12px; border-left: 4px solid #f59e0b;">
            <strong>Your Personalized Exercise:</strong>
            <div style="margin-top: 10px; white-space: pre-wrap;">{exercise}</div>
        </div>
        """, unsafe_allow_html=True)

if st.button("Generate Dynamic Vocabulary"):
    with st.spinner("AI is generating vocabulary for your topic..."):
        context = "\n".join([f"{m['student']}" for m in st.session_state.memory[-3:]])
        dynamic_vocab = ai_service.generate_dynamic_vocabulary(topic, context)
        st.markdown("### AI-Generated Vocabulary")
        for word, meaning, example in dynamic_vocab:
            st.markdown(f"""
            <div style="background: #f0f9ff; padding: 12px; border-radius: 8px; margin: 8px 0;">
                <strong>{word}</strong>: {meaning}<br>
                <em>{example}</em>
            </div>
            """, unsafe_allow_html=True)
