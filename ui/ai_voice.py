import base64
import streamlit as st
import logging
from services.audio_service import audio_service
from utils.decorators_simple import handle_errors, monitor_performance

logger = logging.getLogger(__name__)


@handle_errors()
@monitor_performance()
def ai_voice_player(text: str, voice: str = "alloy", auto_play: bool = True) -> str:
    """
    Create an AI voice player component using OpenAI's TTS
    
    Args:
        text: Text to convert to speech
        voice: Voice ID (alloy, echo, fable, onyx, nova, shimmer)
        auto_play: Whether to auto-play the generated audio
        
    Returns:
        HTML component for AI voice playback
    """
    if not text or not text.strip():
        logger.warning("No text provided for AI voice generation")
        return ""
    
    # Generate audio using OpenAI
    audio_data = audio_service.generate_speech(text, voice)
    
    if not audio_data:
        logger.error("Failed to generate AI voice audio")
        st.error("❌ Failed to generate AI voice. Please try again.")
        return ""
    
    # Convert to base64 for web playback
    audio_b64 = audio_service.get_audio_base64(audio_data)
    
    if not audio_b64:
        logger.error("Failed to convert audio to base64")
        st.error("❌ Failed to process audio data.")
        return ""
    
    # Create unique IDs for this audio instance
    audio_id = f"ai_voice_{hash(text) % 10000}"
    
    # Voice options with descriptions
    voice_options = {
        "alloy": {"name": "Alloy", "description": "Natural, balanced voice", "icon": "🗣️"},
        "echo": {"name": "Echo", "description": "Deep, resonant voice", "icon": "🔊"},
        "fable": {"name": "Fable", "description": "Expressive, warm voice", "icon": "🎭"},
        "onyx": {"name": "Onyx", "description": "Deep, authoritative voice", "icon": "🎙️"},
        "nova": {"name": "Nova", "description": "Bright, friendly voice", "icon": "✨"},
        "shimmer": {"name": "Shimmer", "description": "Soft, ethereal voice", "icon": "🌟"}
    }
    
    current_voice = voice_options.get(voice, voice_options["alloy"])
    
    html_component = f"""
    <div style="
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), rgba(139, 92, 246, 0.1));
        border: 1px solid rgba(14, 165, 233, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin: 16px 0;
        box-shadow: 0 8px 32px rgba(15, 23, 42, 0.1);
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="
                    width: 48px;
                    height: 48px;
                    border-radius: 12px;
                    background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 20px;
                ">
                    {current_voice["icon"]}
                </div>
                <div>
                    <div style="font-size: 16px; font-weight: 700; color: #1e293b; margin-bottom: 4px;">
                        🤖 AI Voice: {current_voice["name"]}
                    </div>
                    <div style="font-size: 14px; color: #64748b;">
                        {current_voice["description"]}
                    </div>
                </div>
            </div>
            
            <div style="display: flex; gap: 8px;">
                <button id="playBtn_{audio_id}" onclick="playAIVoice('{audio_id}')" style="
                    background: linear-gradient(135deg, #10b981, #059669);
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 12px;
                    font-size: 14px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                ">
                    ▶️ Play AI Voice
                </button>
                
                <button id="stopBtn_{audio_id}" onclick="stopAIVoice('{audio_id}')" style="
                    background: linear-gradient(135deg, #dc2626, #ef4444);
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 12px;
                    font-size: 14px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                ">
                    ⏹️ Stop
                </button>
                
                <button id="downloadBtn_{audio_id}" onclick="downloadAIVoice('{audio_id}')" style="
                    background: linear-gradient(135deg, #6366f1, #4f46e5);
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 12px;
                    font-size: 14px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                ">
                    📥 Download
                </button>
            </div>
        </div>
        
        <div id="status_{audio_id}" style="
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 8px;
            padding: 12px;
            margin-top: 12px;
            font-size: 14px;
            color: #059669;
            text-align: center;
            font-weight: 500;
        ">
            🎙️ Ready to play AI-generated voice
        </div>
        
        <!-- Audio element for playback -->
        <audio id="audioPlayer_{audio_id}" style="display: none;"></audio>
        
        <!-- Store audio data -->
        <script>
            window.aiVoiceData_{{audio_id}} = "data:audio/wav;base64,{audio_b64}";
            
            function playAIVoice(audioId) {{
                const audioPlayer = document.getElementById('audioPlayer_' + audioId);
                const playBtn = document.getElementById('playBtn_' + audioId);
                const stopBtn = document.getElementById('stopBtn_' + audioId);
                const statusDiv = document.getElementById('status_' + audioId);
                
                if (audioPlayer.src) {{
                    audioPlayer.pause();
                    audioPlayer.currentTime = 0;
                }}
                
                audioPlayer.src = window.aiVoiceData_{{audio_id}};
                audioPlayer.play();
                
                playBtn.innerHTML = '⏸️ Playing...';
                playBtn.style.background = 'linear-gradient(135deg, #6b7280, #059669)';
                statusDiv.innerHTML = '🎵 Playing AI voice...';
                statusDiv.style.background = 'rgba(16, 185, 129, 0.2)';
                
                audioPlayer.onended = function() {{
                    playBtn.innerHTML = '▶️ Play AI Voice';
                    playBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                    statusDiv.innerHTML = '✅ Playback completed';
                    statusDiv.style.background = 'rgba(16, 185, 129, 0.1)';
                }};
                
                audioPlayer.onerror = function() {{
                    playBtn.innerHTML = '▶️ Play AI Voice';
                    playBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                    statusDiv.innerHTML = '❌ Error playing audio';
                    statusDiv.style.background = 'rgba(220, 38, 38, 0.1)';
                }};
            }}
            
            function stopAIVoice(audioId) {{
                const audioPlayer = document.getElementById('audioPlayer_' + audioId);
                const playBtn = document.getElementById('playBtn_' + audioId);
                const stopBtn = document.getElementById('stopBtn_' + audioId);
                const statusDiv = document.getElementById('status_' + audioId);
                
                if (audioPlayer.src) {{
                    audioPlayer.pause();
                    audioPlayer.currentTime = 0;
                }}
                
                playBtn.innerHTML = '▶️ Play AI Voice';
                playBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                statusDiv.innerHTML = '⏹️ Playback stopped';
                statusDiv.style.background = 'rgba(16, 185, 129, 0.1)';
            }}
            
            function downloadAIVoice(audioId) {{
                const audioData = window.aiVoiceData_{{audio_id}};
                const link = document.createElement('a');
                link.href = audioData;
                link.download = 'ai_voice_' + audioId + '.wav';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }}
            
            // Auto-play if enabled
            {f"setTimeout(() => playAIVoice('{audio_id}'), 1000);" if auto_play else ""}
        </script>
    </div>
    """
    
    return html_component


@handle_errors()
@monitor_performance()
def voice_selector(current_voice: str = "alloy") -> str:
    """
    Create a voice selector component
    
    Args:
        current_voice: Currently selected voice
        
    Returns:
        HTML component for voice selection
    """
    voice_options = {
        "alloy": {"name": "Alloy", "description": "Natural, balanced"},
        "echo": {"name": "Echo", "description": "Deep, resonant"},
        "fable": {"name": "Fable", "description": "Expressive, warm"},
        "onyx": {"name": "Onyx", "description": "Deep, authoritative"},
        "nova": {"name": "Nova", "description": "Bright, friendly"},
        "shimmer": {"name": "Shimmer", "description": "Soft, ethereal"}
    }
    
    selector_html = f"""
    <div style="margin: 16px 0;">
        <label style="font-size: 14px; font-weight: 600; color: #374151; margin-bottom: 8px; display: block;">
            🎙️ AI Voice Selection
        </label>
        <select id="voiceSelector" style="
            width: 100%;
            padding: 12px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 14px;
            background: white;
            color: #374151;
        " onchange="updateVoiceSelection(this.value)">
    """
    
    for voice_id, voice_info in voice_options.items():
        selected = "selected" if voice_id == current_voice else ""
        selector_html += f"""
            <option value="{voice_id}" {selected}>
                {voice_info["name"]} - {voice_info["description"]}
            </option>
        """
    
    selector_html += """
        </select>
        
        <script>
            function updateVoiceSelection(voiceId) {
                // Store selection in session state
                const event = new CustomEvent('voiceChange', {
                    detail: { voice: voiceId }
                });
                document.dispatchEvent(event);
            }
        </script>
    </div>
    """
    
    return selector_html


@handle_errors()
@monitor_performance()
def get_voice_info() -> dict:
    """Get information about available AI voices"""
    return audio_service.get_available_voices() or {
        "alloy": {"name": "Alloy", "language": "English", "gender": "Neutral", "description": "Natural, balanced voice"},
        "echo": {"name": "Echo", "language": "English", "gender": "Male", "description": "Deep, resonant voice"},
        "fable": {"name": "Fable", "language": "English", "gender": "Male", "description": "Expressive, warm voice"},
        "onyx": {"name": "Onyx", "language": "English", "gender": "Male", "description": "Deep, authoritative voice"},
        "nova": {"name": "Nova", "language": "English", "gender": "Female", "description": "Bright, friendly voice"},
        "shimmer": {"name": "Shimmer", "language": "English", "gender": "Female", "description": "Soft, ethereal voice"}
    }
