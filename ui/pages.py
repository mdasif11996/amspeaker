import streamlit as st
from datetime import datetime
from services.ai_service import AIService
from services.content_service import ContentService
from ui.voice import speak_button, browser_speech_input
from utils.analytics import AnalyticsManager
from config.settings import config


def conversation_practice_page(ai_service, content_service, analytics):
    """Render the main conversation practice page"""
    left, right = st.columns([2, 1])
    
    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Practice Speaking with AI")
        st.markdown("Have a natural conversation with your AI speaking coach. Speak freely and get instant feedback!")
        
        st.markdown("---")
        
        col_level, col_topic, col_mode = st.columns([1, 2, 1])
        with col_level:
            level = st.selectbox("Your Level", ["Beginner", "Intermediate", "Advanced"], help="Select your English proficiency level")
        with col_topic:
            # Use daily topics if available and fresh, otherwise generate dynamic topics
            if st.session_state.daily_content["topics"] and not content_service.should_update_daily_content(st.session_state.daily_content.get("last_updated")):
                available_topics = st.session_state.daily_content["topics"]
            else:
                # Regenerate topics if level changes
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
        
        # Voice input section
        browser_speech_input()
        
        # Voice recording and playback
        st.markdown("---")
        st.markdown("### Voice Recording & Playback")
        col_rec1, col_rec2 = st.columns([1, 1])
        with col_rec1:
            if st.button("Record Voice Note", help="Record a voice note for practice"):
                st.info("Recording feature - Click to start recording your voice")
        with col_rec2:
            if st.button("Play Last Response", help="Replay the last AI response"):
                if st.session_state.last_feedback:
                    speak_button(st.session_state.last_feedback, "Replaying...")
        
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
            auto_response = st.checkbox("Auto-play AI Voice Response", value=True, help="AI will automatically speak its response")
            if st.button("Send to AI Teacher", type="primary", help="Send your message and get AI voice response", use_container_width=True):
                if user_text.strip():
                    with st.spinner("AI is thinking of a natural response..."):
                        feedback, scores = ai_service.ask_ai_teacher(
                            user_text, level, topic, "Conversation", 
                            conversation_mode, st.session_state.memory
                        )
                        # Save to history
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
                    
                    # Display AI response in a styled box
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f0f9ff, #e0f2fe); padding: 20px; border-radius: 16px; border: 2px solid #0ea5e9; margin: 15px 0;">
                        <strong>AI Voice Response ({conversation_mode} Mode):</strong>
                        <div style="margin-top: 10px; line-height: 1.6;">
                            {feedback}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display speaking metrics
                    st.markdown("### Speaking Metrics")
                    cols = st.columns(6)
                    cols[0].metric("Overall", f"{scores['overall']}/100")
                    cols[1].metric("Grammar", f"{scores['grammar']}/100")
                    cols[2].metric("Vocabulary", f"{scores['vocabulary']}/100")
                    cols[3].metric("Fluency", f"{scores['fluency']}/100")
                    cols[4].metric("Naturalness", f"{scores['communication']}/100")
                    cols[5].metric("Pronunciation", f"{scores['pronunciation']}/100")
                    
                    # Pronunciation feedback
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
                    
                    # Always play AI voice response for voice-to-voice conversation
                    speak_button(feedback, "Playing AI Voice Response...")
                    
                    # Clear the input for next message
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

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Voice Conversation Tips")
        st.write("• Speak clearly at natural pace")
        st.write("• Allow microphone permission in browser")
        st.write("• Copy voice text to input field")
        st.write("• AI will respond with voice automatically")
        st.write("• Listen to AI's natural responses")
        st.write("• Try different conversation modes")
        st.divider()
        st.subheader("Speaking Exercises")
        
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
        st.divider()
        st.subheader("Conversation Starters")
        st.write("• Tell me about your day...")
        st.write("• What do you think about...")
        st.write("• Have you ever...")
        st.write("• I was wondering...")
        st.write("• The thing is...")
        st.divider()
        st.subheader("Voice Controls")
        st.write("• Microphone: Browser address bar")
        st.write("• Voice Input: Click button below")
        st.write("• AI Voice: Automatic playback")
        st.write("• Recording: Voice Note feature")
        st.markdown('</div>', unsafe_allow_html=True)


def voice_chat_page(ai_service, analytics):
    """Render the voice chat page"""
    st.subheader("Voice Chat with AI Teacher")
    st.markdown("Pure voice-to-voice conversation practice. Speak naturally and the AI will respond!")
    
    st.markdown("---")
    
    # Voice input section
    st.markdown("### Your Voice Input")
    browser_speech_input()
    
    st.markdown("### Or Type Your Message")
    user_voice_text = st.text_area("Type your message here:", height=120, key="voice_chat_input", placeholder="Type or paste your speech here...")
    
    # Add conversation history display
    if st.session_state.history:
        st.markdown("---")
        st.markdown("### Recent Conversation")
        for h in st.session_state.history[-3:]:
            with st.chat_message("user"):
                st.write(h["answer"])
            with st.chat_message("assistant"):
                st.write(h["feedback"])
    
    # Send button
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
                    
                    # Display speaking metrics
                    st.markdown("---")
                    st.markdown("### Speaking Metrics")
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.metric("Overall", f"{scores.get('overall', 0)}/100")
                    with col_m2:
                        st.metric("Fluency", f"{scores.get('fluency', 0)}/100")
                    with col_m3:
                        st.metric("Communication", f"{scores.get('communication', 0)}/100")
                    
                    # Feedback based on scores
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


def vocabulary_page(content_service, ai_service, analytics):
    """Render the vocabulary practice page"""
    st.subheader("Vocabulary for Natural Speaking")
    
    # Use daily vocabulary if available, otherwise fallback to static VOCAB
    if st.session_state.daily_content["vocabulary"]:
        vocab_to_use = st.session_state.daily_content["vocabulary"]
        st.info("📅 Using today's auto-updated speaking vocabulary")
    else:
        vocab_to_use = content_service.get_default_vocab()
        st.info("📚 Using default vocabulary. Click 'Update Now' in sidebar to get fresh daily vocabulary.")

    for word, meaning, example in vocab_to_use:
        with st.expander(f"{word.title()}"):
            st.write(f"**Meaning:** {meaning}")
            st.write(f"**Speaking Example:** {example}")
            speak_button(f"{word}. {meaning}. Example: {example}", f"Hear {word}")

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
            st.session_state.last_feedback = feedback
            analytics.track_interaction("conversation")
            st.markdown(feedback)
            speak_button(feedback)


def expressions_page(ai_service, analytics):
    """Render the natural expressions page"""
    st.subheader("Natural English Expressions")

    grammar_topic = st.selectbox(
        "Choose Expression Type",
        ["Filler Words", "Transition Phrases", "Agreement Expressions", "Opinion Phrases", "Clarification", "Casual Responses"]
    )

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
            st.session_state.last_feedback = feedback
            analytics.track_interaction("conversation")
            st.markdown(feedback)
            speak_button(feedback)


def idioms_page(content_service, ai_service, analytics):
    """Render the idioms practice page"""
    st.subheader("Idioms for Natural Speech")
    
    # Use daily idioms if available, otherwise fallback to static IDIOMS
    if st.session_state.daily_content["idioms"]:
        idioms_to_use = st.session_state.daily_content["idioms"]
        st.info("📅 Using today's auto-updated idioms from daily news")
    else:
        idioms_to_use = content_service.get_default_idioms()
        st.info("📚 Using default idioms. Click 'Update Now' in sidebar to get fresh daily idioms from news.")

    for idiom, meaning, example in idioms_to_use:
        with st.expander(f"{idiom}"):
            st.write(f"**Meaning:** {meaning}")
            st.write(f"**Speaking Example:** {example}")
            speak_button(f"{idiom}. Meaning: {meaning}. Example: {example}", f"Hear {idiom}")

    text = st.text_area("Use an idiom in your speech", height=160)

    if st.button("Practice with AMspeaker"):
        if text.strip():
            feedback, scores = ai_service.ask_ai_teacher(text, "Intermediate", "Idioms in Speech", "Idioms")
            st.session_state.history.append({
                "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "topic": "Idioms in Speech",
                "answer": text,
                "feedback": feedback,
                "scores": scores
            })
            st.session_state.last_feedback = feedback
            analytics.track_interaction("conversation")
            st.markdown(feedback)
            speak_button(feedback)


def interview_page(ai_service, analytics):
    """Render the interview practice page"""
    st.subheader("Interview Speaking Practice")

    INTERVIEW = [
        "Tell me about yourself.",
        "Why should we hire you?",
        "What are your strengths?",
        "Explain your project.",
        "Where do you see yourself in five years?"
    ]

    question = st.selectbox("Interview Question", INTERVIEW)
    st.info(question)

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
            st.session_state.last_feedback = feedback
            analytics.track_interaction("conversation")
            st.markdown(feedback)
            speak_button(feedback)


def progress_page():
    """Render the progress report page"""
    st.subheader("Your Speaking Progress")

    if not st.session_state.history:
        st.warning("No progress yet. Complete a practice session first.")
    else:
        latest = st.session_state.history[-1]
        s = latest["scores"]

        cols = st.columns(6)
        cols[0].metric("Overall", s["overall"])
        cols[1].metric("Grammar", s["grammar"])
        cols[2].metric("Vocabulary", s["vocabulary"])
        cols[3].metric("Fluency", s["fluency"])
        cols[4].metric("Naturalness", s["communication"])
        cols[5].metric("Pronunciation", s["pronunciation"])

        st.progress(s["overall"] / 100)

        st.markdown(latest["feedback"])
        speak_button(latest["feedback"])

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
            file_name="speak_ai_progress_report.txt",
            mime="text/plain",
        )


def news_vocabulary_page(ai_service, analytics):
    """Render the daily news vocabulary page"""
    st.subheader("Daily News Vocabulary & Idioms")
    st.markdown("Learn vocabulary and idioms from today's news articles. Practice using them in conversation!")
    
    # Fetch news vocabulary
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
            
            # Add practice section
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
                        st.session_state.last_feedback = feedback
                        analytics.track_interaction("conversation")
                    st.markdown(feedback)
                    speak_button(feedback, "Listen to Feedback")
                else:
                    st.warning("Please write something to practice.")
                    
        except Exception as e:
            st.error(f"Error fetching news vocabulary: {str(e)}")
            st.info("Please try again later or check your internet connection.")
