import streamlit as st
from datetime import datetime
from config.settings import config
from services.content_service import ContentService
from ui.voice import speak_button
from utils.analytics import AnalyticsManager


def render_sidebar(content_service, analytics):
    """Render the sidebar with controls and information"""
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    st.markdown('<img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Alex&backgroundColor=b6e3f4" style="width: 120px; height: 120px; border-radius: 50%; border: 4px solid #0ea5e9; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
    st.markdown('<div style="background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; padding: 8px 16px; border-radius: 20px; font-weight: bold; font-size: 14px; margin-top: 10px; display: inline-block;">AI English Coach v2.0</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # System status for production monitoring
    st.markdown("### System Status")
    if config.environment == "production":
        st.success("Environment: Production")
    else:
        st.info(f"Environment: {config.environment}")
    
    st.caption(f"Version: {config.app_version}")
    
    # Session analytics
    if config.enable_analytics:
        stats = analytics.get_session_stats()
        with st.expander("Session Analytics"):
            st.write(f"Session Duration: {stats['duration']}")
            st.write(f"Interactions: {stats['interactions']}")
            st.write(f"Errors: {stats['errors']}")
    
    st.divider()
    
    # Daily content update section
    st.markdown("### Daily Content Auto-Update")
    
    # Display last update time for all streams
    if st.session_state.daily_content["last_updated"]:
        last_update = st.session_state.daily_content["last_updated"]
        time_ago = datetime.now() - last_update
        hours_ago = int(time_ago.total_seconds() / 3600)
        if hours_ago < 24:
            st.success(f"All content updated {hours_ago} hours ago")
            st.caption("✓ Vocabulary ✓ Idioms ✓ Topics")
        else:
            st.warning(f"Content updated {hours_ago} hours ago (needs refresh)")
    else:
        st.info("No content fetched yet")
    
    col_update1, col_update2 = st.columns([1, 1])
    with col_update1:
        if st.button("Update All Content", help="Fetch fresh vocabulary, idioms, and topics from internet", use_container_width=True):
            with st.spinner("Fetching fresh content from internet..."):
                updated_content = content_service.update_daily_content(st.session_state.daily_content)
                if updated_content:
                    st.session_state.daily_content = updated_content
                    # Also update dynamic topics with fresh content
                    if updated_content.get("topics"):
                        st.session_state.dynamic_topics = updated_content.get("topics")
                    st.success("All content streams updated successfully!")
                    analytics.track_interaction("manual_content_update")
                    st.rerun()
                else:
                    st.error("Failed to update. Try again later.")
    
    with col_update2:
        if st.button("Auto-Update All", help="Enable automatic daily updates for all content", use_container_width=True):
            if "auto_update_enabled" not in st.session_state:
                st.session_state.auto_update_enabled = False
            st.session_state.auto_update_enabled = not st.session_state.auto_update_enabled
            if st.session_state.auto_update_enabled:
                st.success("Auto-update enabled for all content")
            else:
                st.info("Auto-update disabled")
    
    st.divider()
    
    # Display daily speaking vocabulary if available
    if st.session_state.daily_content["vocabulary"]:
        st.markdown("### Today's Speaking Vocabulary")
        for word, meaning, example in st.session_state.daily_content["vocabulary"][:3]:
            with st.expander(f"🗣️ {word}"):
                st.write(f"**Meaning:** {meaning}")
                st.write(f"**Speaking Example:** {example}")
                speak_button(f"{word}. {meaning}. Example: {example}", f"Hear {word}")
    
    st.divider()
    st.success("✅ AI Coach Online")
    st.markdown('<div class="teacher-box">🎯 Ready to help you speak confidently!</div>', unsafe_allow_html=True)
    st.write("")
    
    # Voice Chat with AI Teacher
    with st.expander("🎤 Voice Chat with AI Teacher"):
        st.markdown("""
        **Voice Chat Mode:**
        - Pure voice-to-voice conversation
        - Real-time speech recognition
        - AI speaks back automatically
        - Perfect for fluency practice
        """)
        if st.button("Start Voice Chat"):
            st.session_state.page = "Voice Chat"
            st.rerun()
    
    with st.expander("📖 Quick Start Guide"):
        st.markdown("""
        **How to use:**
        1. Select your level and topic
        2. Click "Start Speaking" 
        3. Speak naturally in English
        4. AI will respond automatically
        5. Listen and improve!
        
        **Tips:**
        - Use Chrome/Edge for voice
        - Allow microphone permission
        - Speak clearly at natural pace
        """)
    
    st.write("")
    st.markdown("### Audio Controls")
    speak_button(st.session_state.last_feedback, "Replay Last AI Response")

    st.markdown("---")
    st.markdown("### Practice Modes")
    page = st.radio(
        "Select Mode:",
        [
            "Conversation Practice",
            "Voice Chat with AI",
            "Speaking Vocabulary",
            "Natural Expressions",
            "Idioms in Speech",
            "Speaking Interview",
            "Progress Report",
            "Daily News Vocabulary",
        ],
        label_visibility="collapsed"
    )
    
    return page
