import base64
import streamlit as st


def iframe_html(html, height=160):
    """Render HTML in an iframe"""
    encoded = base64.b64encode(html.encode("utf-8")).decode()
    st.markdown(
        f'<iframe src="data:text/html;base64,{encoded}" width="100%" height="{height}" frameborder="0" allow="microphone"></iframe>',
        unsafe_allow_html=True
    )


def speak_button(text, label="Listen to Response"):
    """Create a text-to-speech button"""
    safe = text.replace("\\", "\\\\").replace("`", "").replace("\n", " ").replace('"', "'")
    iframe_html(f"""
    <div style="display: flex; gap: 10px; align-items: center;">
        <button id="speakBtn" onclick="speakText()" style="
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white;
            border: none;
            padding: 14px 24px;
            border-radius: 12px;
            font-size: 16px;
            cursor: pointer;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;">
            {label}
        </button>
        <button id="stopBtn" onclick="stopSpeaking()" style="
            background: linear-gradient(135deg, #dc2626, #ef4444);
            color: white;
            border: none;
            padding: 14px 20px;
            border-radius: 12px;
            font-size: 16px;
            cursor: pointer;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;">
            Stop
        </button>
    </div>
    <script>
    function speakText() {{
        const btn = document.getElementById('speakBtn');
        const msg = new SpeechSynthesisUtterance(`{safe}`);
        msg.lang = "en-US";
        msg.rate = 0.86;
        msg.pitch = 1;
        
        msg.onstart = function() {{
            btn.innerHTML = "Playing...";
            btn.style.background = "linear-gradient(135deg, #16a34a, #22c55e)";
        }};
        
        msg.onend = function() {{
            btn.innerHTML = "{label}";
            btn.style.background = "linear-gradient(135deg, #4f46e5, #7c3aed)";
        }};
        
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
    }}
    
    function stopSpeaking() {{
        window.speechSynthesis.cancel();
        const btn = document.getElementById('speakBtn');
        btn.innerHTML = "{label}";
        btn.style.background = "linear-gradient(135deg, #4f46e5, #7c3aed)";
    }}
    </script>
    """, 95)


def browser_speech_input():
    """Create a browser-based speech input component"""
    st.error("IMPORTANT: Click the microphone icon in your browser's address bar (top left) and ALLOW microphone access BEFORE using voice input!")
    st.markdown("### Voice Input")
    st.markdown("**Step 1:** Click the microphone icon in your browser's address bar (top left) and click 'Allow'")
    st.markdown("**Step 2:** Click 'Start Speaking' button below")
    st.markdown("**Step 3:** Speak naturally")
    st.markdown("**Step 4:** Copy the text to the input field below")
    
    st.markdown("---")
    
    iframe_html("""
    <div style="background:white;border:1px solid #ddd;padding:16px;border-radius:18px;font-family:Arial;">
        <button id="micButton" onclick="toggleDictation()" style="
            background:linear-gradient(135deg,#16a34a,#0ea5e9);
            color:white;border:0;padding:12px 18px;border-radius:14px;
            font-size:16px;cursor:pointer;font-weight:bold;">
            Start Speaking
        </button>
        <p id="statusText" style="font-size:13px;color:#555;margin-top:10px;">Click to start speaking...</p>
        <textarea id="speechOutput" rows="4" placeholder="Your speech will appear here..."
        style="width:100%;border:1px solid #cbd5e1;border-radius:12px;padding:10px;font-size:15px;margin-top:10px;"></textarea>
    </div>
    <script>
    let recognition = null;
    let isListening = false;
    
    function toggleDictation() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            document.getElementById("speechOutput").value = "Speech recognition not supported. Use Chrome or Edge.";
            document.getElementById("statusText").innerHTML = "Error: Browser not supported. Please use Chrome or Edge.";
            return;
        }
        
        if (isListening) {
            stopDictation();
        } else {
            startDictation();
        }
    }
    
    function startDictation() {
        recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.interimResults = true;
        recognition.continuous = false;
        
        recognition.onstart = function() {
            isListening = true;
            document.getElementById("micButton").innerHTML = "Stop Speaking";
            document.getElementById("micButton").style.background = "linear-gradient(135deg,#dc2626,#ef4444)";
            document.getElementById("statusText").innerHTML = "Listening... Speak now!";
        };
        
        recognition.onresult = function(event) {
            let finalTranscript = "";
            for (let i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                }
            }
            if (finalTranscript) {
                document.getElementById("speechOutput").value = finalTranscript;
                document.getElementById("statusText").innerHTML = "Speech captured! Copy the text below.";
                stopDictation();
            }
        };
        
        recognition.onerror = function(event) {
            let errorMsg = "Error: " + event.error;
            if (event.error === "not-allowed") {
                errorMsg = "PERMISSION DENIED: Please click the microphone icon in your browser address bar (top left) and click ALLOW.";
            } else if (event.error === "no-speech") {
                errorMsg = "Error: No speech detected. Please try again.";
            }
            document.getElementById("statusText").innerHTML = errorMsg;
            stopDictation();
        };
        
        recognition.onend = function() {
            if (isListening) {
                stopDictation();
            }
        };
        
        recognition.start();
    }
    
    function stopDictation() {
        isListening = false;
        if (recognition) {
            recognition.stop();
        }
        document.getElementById("micButton").innerHTML = "Start Speaking";
        document.getElementById("micButton").style.background = "linear-gradient(135deg,#16a34a,#0ea5e9)";
    }
    </script>
    """, 280)
