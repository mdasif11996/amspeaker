import streamlit as st


def render_advanced_sidebar():
    """Render advanced sidebar with categories, icons, and enhanced navigation with modern styling"""
    
    # User Profile Section with glassmorphism
    st.markdown("""
    <div style="text-align: center; padding: 24px 0;">
        <div style="width: 90px; height: 90px; border-radius: 50%; background: linear-gradient(135deg, #0ea5e9, #8b5cf6, #ec4899); margin: 0 auto 16px; display: flex; align-items: center; justify-content: center; font-size: 36px; color: white; box-shadow: 0 15px 40px rgba(14, 165, 233, .4); animation: pulse 2s infinite;">
            👤
        </div>
        <h3 style="margin: 0; color: #1e293b; font-weight: 700; font-size: 18px;">Welcome to AMspeaker</h3>
        <p style="margin: 6px 0 0 0; color: #64748b; font-size: 13px; font-weight: 500;">Master English with AI</p>
    </div>
    <style>
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Quick Stats with modern cards
    if "history" in st.session_state and st.session_state.history:
        total_sessions = len(st.session_state.history)
        latest_score = st.session_state.history[-1]["scores"]["overall"]
        
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sessions", total_sessions)
        with col2:
            st.metric("Latest", f"{latest_score}%")
        st.divider()
    
    # Navigation Categories with glassmorphism cards
    st.markdown("### 🚀 Practice Modes")
    
    practice_modes = [
        {"name": "Conversation", "icon": "💬", "page": "1_Conversation", "desc": "AI conversations", "gradient": "linear-gradient(135deg, #0ea5e9, #8b5cf6)"},
        {"name": "Voice Chat", "icon": "🎤", "page": "2_Voice_Chat", "desc": "Voice-to-voice", "gradient": "linear-gradient(135deg, #8b5cf6, #ec4899)"},
        {"name": "Interview", "icon": "💼", "page": "6_Interview", "desc": "Job prep", "gradient": "linear-gradient(135deg, #ec4899, #f59e0b)"},
    ]
    
    for mode in practice_modes:
        with st.container():
            st.markdown(f"""
            <div style="padding: 16px; border-radius: 16px; background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.6); margin-bottom: 12px; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(15, 23, 42, .08);" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 25px rgba(15, 23, 42, .15)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(15, 23, 42, .08)';">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div style="width: 48px; height: 48px; border-radius: 12px; background: {mode['gradient']}; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
                        {mode['icon']}
                    </div>
                    <div>
                        <div style="font-weight: 700; color: #1e293b; font-size: 15px;">{mode['name']}</div>
                        <div style="color: #64748b; font-size: 12px; font-weight: 500;">{mode['desc']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### 📚 Learning")
    
    learning_modes = [
        {"name": "Vocabulary", "icon": "📚", "page": "3_Vocabulary", "desc": "Word practice", "gradient": "linear-gradient(135deg, #10b981, #0ea5e9)"},
        {"name": "Expressions", "icon": "💡", "page": "4_Expressions", "desc": "Natural speech", "gradient": "linear-gradient(135deg, #f59e0b, #ec4899)"},
        {"name": "Idioms", "icon": "🎯", "page": "5_Idioms", "desc": "Native phrases", "gradient": "linear-gradient(135deg, #8b5cf6, #10b981)"},
        {"name": "News", "icon": "📰", "page": "8_News", "desc": "Current events", "gradient": "linear-gradient(135deg, #0ea5e9, #10b981)"},
    ]
    
    for mode in learning_modes:
        with st.container():
            st.markdown(f"""
            <div style="padding: 16px; border-radius: 16px; background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.6); margin-bottom: 12px; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(15, 23, 42, .08);" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 25px rgba(15, 23, 42, .15)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(15, 23, 42, .08)';">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div style="width: 48px; height: 48px; border-radius: 12px; background: {mode['gradient']}; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
                        {mode['icon']}
                    </div>
                    <div>
                        <div style="font-weight: 700; color: #1e293b; font-size: 15px;">{mode['name']}</div>
                        <div style="color: #64748b; font-size: 12px; font-weight: 500;">{mode['desc']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### 📈 Progress")
    
    progress_modes = [
        {"name": "Progress Report", "icon": "📊", "page": "7_Progress", "desc": "Track growth", "gradient": "linear-gradient(135deg, #8b5cf6, #0ea5e9)"},
    ]
    
    for mode in progress_modes:
        with st.container():
            st.markdown(f"""
            <div style="padding: 16px; border-radius: 16px; background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.6); margin-bottom: 12px; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(15, 23, 42, .08);" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 25px rgba(15, 23, 42, .15)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(15, 23, 42, .08)';">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div style="width: 48px; height: 48px; border-radius: 12px; background: {mode['gradient']}; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
                        {mode['icon']}
                    </div>
                    <div>
                        <div style="font-weight: 700; color: #1e293b; font-size: 15px;">{mode['name']}</div>
                        <div style="color: #64748b; font-size: 12px; font-weight: 500;">{mode['desc']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Quick Actions with modern buttons
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠", use_container_width=True, key="nav_home", help="Go to Home"):
            st.switch_page("app.py")
    with col2:
        if st.button("🔄", use_container_width=True, key="nav_refresh", help="Refresh Content"):
            if "content_service" in st.session_state:
                updated = st.session_state.content_service.update_daily_content(st.session_state.daily_content)
                if updated:
                    st.session_state.daily_content = updated
                    st.success("Content updated!")
                    st.rerun()
    
    st.markdown('<div style="display: flex; gap: 8px; margin-top: 8px;">', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.caption("Home")
    with col4:
        st.caption("Refresh")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Settings with modern toggle
    st.markdown("### ⚙️ Settings")
    
    if "auto_update_enabled" not in st.session_state:
        st.session_state.auto_update_enabled = False
    
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    
    auto_update = st.checkbox("Auto-update content", value=st.session_state.auto_update_enabled)
    st.session_state.auto_update_enabled = auto_update
    
    dark_mode = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
    st.session_state.dark_mode = dark_mode
    
    # System Info with modern footer
    st.divider()
    st.markdown(f"""
    <div style="text-align: center; padding: 16px; background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(10px); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.4);">
        <div style="background: linear-gradient(135deg, #0ea5e9, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 700; font-size: 14px;">
            AMspeaker v2.0
        </div>
        <div style="color: #94a3b8; font-size: 11px; margin-top: 4px;">
            Made with ❤️
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_page_header(title, icon, subtitle=""):
    """Render a consistent modern page header across all pages with glassmorphism"""
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px); padding: 28px; border-radius: 20px; margin-bottom: 28px; border: 1px solid rgba(255, 255, 255, 0.6); box-shadow: 0 8px 30px rgba(15, 23, 42, .1);">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="width: 64px; height: 64px; border-radius: 16px; background: linear-gradient(135deg, #0ea5e9, #8b5cf6); display: flex; align-items: center; justify-content: center; font-size: 32px; box-shadow: 0 8px 25px rgba(14, 165, 233, .3);">
                {icon}
            </div>
            <div>
                <h1 style="margin: 0; color: #1e293b; font-size: 32px; font-weight: 700;">{title}</h1>
                {f'<p style="margin: 6px 0 0 0; color: #64748b; font-size: 15px; font-weight: 500;">{subtitle}</p>' if subtitle else ''}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_breadcrumb(items):
    """Render breadcrumb navigation"""
    breadcrumb_html = " > ".join([f'<span style="color: #64748b;">{item}</span>' for item in items])
    st.markdown(f"""
    <div style="padding: 8px 0; color: #94a3b8; font-size: 13px;">
        🏠 {breadcrumb_html}
    </div>
    """, unsafe_allow_html=True)
