import streamlit as st
from ui.voice import speak_button
from ui.styles import apply_custom_styles
from ui.navigation import render_page_header

# Page config
st.set_page_config(
    page_title="Progress - AMspeaker",
    page_icon="📊",
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
render_page_header("Your Speaking Progress", "📊", "Track your improvement over time with detailed metrics")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("---")

if not st.session_state.history:
    st.warning("No progress yet. Complete a practice session first.")
    st.info("Go to Conversation Practice or any other practice mode to start tracking your progress.")
else:
    latest = st.session_state.history[-1]
    s = latest["scores"]

    st.markdown("### Latest Session Metrics")
    cols = st.columns(6)
    cols[0].metric("Overall", s["overall"])
    cols[1].metric("Grammar", s["grammar"])
    cols[2].metric("Vocabulary", s["vocabulary"])
    cols[3].metric("Fluency", s["fluency"])
    cols[4].metric("Naturalness", s["communication"])
    cols[5].metric("Pronunciation", s["pronunciation"])

    st.markdown("---")
    st.markdown("### Overall Progress")
    st.progress(s["overall"] / 100)

    st.markdown("---")
    st.markdown("### Latest Feedback")
    st.markdown(latest["feedback"])
    speak_button(latest["feedback"])

    st.markdown("---")
    st.markdown("### Session History")
    
    # Generate report text
    lines = ["AMspeaker - Spoken English Progress Report", "=" * 45]
    for h in st.session_state.history:
        s = h["scores"]
        lines.extend([
            f"Time: {h['time']}",
            f"Topic: {h['topic']}",
            f"Answer: {h['answer']}",
            f"Overall: {s['overall']}/100",
            f"Grammar: {s['grammar']}/100",
            f"Vocabulary: {s['vocabulary']}/100",
            f"Fluency: {s['fluency']}/100",
            f"Naturalness: {s['communication']}/100",
            f"Pronunciation: {s['pronunciation']}/100",
            "-" * 45
        ])
    report_text = "\n".join(lines)

    st.download_button(
        "Download Progress Report",
        data=report_text,
        file_name="speakx_progress_report.txt",
        mime="text/plain",
    )
