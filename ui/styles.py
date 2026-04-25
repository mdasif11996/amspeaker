import streamlit as st


def apply_custom_styles():
    """Apply modern CSS styles to the Streamlit app with glassmorphism, animations, dark mode, and mobile responsiveness"""
    
    # Add PWA manifest and viewport meta tags
    st.markdown("""
<link rel="manifest" href="/static/manifest.json">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="theme-color" content="#0ea5e9">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="AMspeaker">
<script>
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/sw.js').then(function(registration) {
            console.log('ServiceWorker registration successful');
        }, function(err) {
            console.log('ServiceWorker registration failed: ', err);
        });
    });
}
</script>
""", unsafe_allow_html=True)
    
    # Check if dark mode is enabled
    dark_mode = st.session_state.get("dark_mode", False)
    
    if dark_mode:
        # Dark mode styles
        st.markdown("""
<style>
/* Dark mode gradient background with animated pattern */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    color: #e2e8f0;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Modern hero with glassmorphism - dark mode */
.hero {
    padding: 40px;
    border-radius: 32px;
    background: linear-gradient(135deg, #0ea5e9, #8b5cf6, #ec4899);
    color: white;
    box-shadow: 0 25px 60px rgba(14, 165, 233, .4);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%) rotate(45deg); }
    100% { transform: translateX(100%) rotate(45deg); }
}

/* Glassmorphism cards - dark mode */
.card {
    background: rgba(30, 41, 59, 0.8);
    backdrop-filter: blur(20px);
    padding: 28px;
    border-radius: 24px;
    box-shadow: 0 15px 40px rgba(15, 23, 42, .3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    color: #e2e8f0;
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 25px 60px rgba(15, 23, 42, .4);
}

.teacher-box {
    background: linear-gradient(135deg, rgba(254, 243, 199, 0.2), rgba(253, 230, 138, 0.2));
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 24px;
    border: 1px solid rgba(245, 158, 11, 0.3);
    box-shadow: 0 10px 30px rgba(245, 158, 11, .15);
    color: #e2e8f0;
}

.score {
    background: rgba(30, 41, 59, 0.9);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: transform 0.3s ease;
    color: #e2e8f0;
}

.score:hover {
    transform: scale(1.05);
}

/* Modern button styling with animations - dark mode */
.stButton > button {
    border-radius: 16px;
    padding: 14px 28px;
    font-weight: 600;
    font-size: 16px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
    color: #e2e8f0;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.stButton > button:hover::before {
    width: 300px;
    height: 300px;
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 30px rgba(0,0,0,0.4);
}

.stButton > button:active {
    transform: translateY(-2px) scale(0.98);
}

/* Primary button with gradient and glow - dark mode */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
    border: none;
    color: white;
    box-shadow: 0 6px 20px rgba(14, 165, 233, .4);
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0284c7, #7c3aed);
    box-shadow: 0 12px 35px rgba(14, 165, 233, .6);
}

/* Sidebar with glassmorphism - dark mode */
.css-1d391kg {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.98) 100%);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

/* Modern input styling - dark mode */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: 12px;
    border: 2px solid #334155;
    transition: all 0.3s ease;
    background: rgba(30, 41, 59, 0.9);
    color: #e2e8f0;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.2);
    outline: none;
}

/* Modern selectbox styling - dark mode */
.stSelectbox > div > div > select {
    border-radius: 12px;
    border: 2px solid #334155;
    transition: all 0.3s ease;
    background: rgba(30, 41, 59, 0.9);
    color: #e2e8f0;
}

.stSelectbox > div > div > select:focus {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.2);
    outline: none;
}

/* Metric cards with glassmorphism - dark mode */
.stMetric {
    background: rgba(30, 41, 59, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 25px rgba(15, 23, 42, .2);
    transition: all 0.3s ease;
    color: #e2e8f0;
}

.stMetric:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(15, 23, 42, .3);
}

/* Expander with modern styling - dark mode */
.streamlit-expanderHeader {
    background: rgba(30, 41, 59, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 16px;
    transition: all 0.3s ease;
    color: #e2e8f0;
}

.streamlit-expanderHeader:hover {
    background: rgba(30, 41, 59, 1);
    box-shadow: 0 4px 15px rgba(15, 23, 42, .2);
}

/* Progress bar with gradient - dark mode */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #0ea5e9, #8b5cf6, #ec4899);
    background-size: 200% 200%;
    animation: progressGradient 3s ease infinite;
}

@keyframes progressGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Info/success/warning boxes with glassmorphism - dark mode */
.stAlert {
    backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 25px rgba(15, 23, 42, .2);
    color: #e2e8f0;
}

/* Smooth scroll behavior */
html {
    scroll-behavior: smooth;
}

/* Custom scrollbar - dark mode */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.5);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #0284c7, #7c3aed);
}

/* Text colors for dark mode */
h1, h2, h3, h4, h5, h6 {
    color: #e2e8f0 !important;
}

p, span, div {
    color: #cbd5e1;
}

/* Mobile Responsive Styles */
@media (max-width: 768px) {
    .stApp {
        font-size: 14px;
    }
    
    .hero {
        padding: 24px;
        border-radius: 20px;
    }
    
    .hero h1 {
        font-size: 24px !important;
    }
    
    .card {
        padding: 20px;
        border-radius: 16px;
    }
    
    .stButton > button {
        padding: 12px 20px;
        font-size: 14px;
        min-height: 48px;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-size: 16px;
        padding: 12px;
    }
    
    .stSelectbox > div > div > select {
        font-size: 16px;
        padding: 12px;
    }
    
    .stMetric {
        padding: 16px;
        font-size: 14px;
    }
    
    /* Sidebar mobile optimization */
    .css-1d391kg {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Hide sidebar on mobile by default, show with toggle */
    @media (max-width: 640px) {
        .css-1d391kg {
            display: none;
        }
        
        .css-1d391kg.mobile-visible {
            display: block;
            position: fixed;
            top: 0;
            left: 0;
            width: 80% !important;
            max-width: 300px !important;
            height: 100vh;
            z-index: 9999;
            overflow-y: auto;
        }
    }
    
    /* Mobile navigation toggle button */
    .mobile-nav-toggle {
        display: block !important;
        position: fixed;
        top: 16px;
        right: 16px;
        z-index: 10000;
        background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
        border: none;
        border-radius: 12px;
        padding: 12px 16px;
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
        cursor: pointer;
    }
    
    /* Adjust columns for mobile */
    .stColumns {
        flex-direction: column !important;
    }
    
    .stColumns > div {
        width: 100% !important;
        margin-bottom: 16px;
    }
    
    /* Touch-friendly spacing */
    .streamlit-expanderHeader {
        padding: 20px;
        min-height: 56px;
    }
    
    /* Optimize chat for mobile */
    .chat-message {
        padding: 16px;
        margin: 8px 0;
        border-radius: 12px;
    }
    
    /* Voice input mobile optimization */
    iframe {
        max-width: 100%;
    }
}
</style>
""", unsafe_allow_html=True)
    else:
        # Light mode styles
        st.markdown("""
<style>
/* Modern gradient background with animated pattern */
.stApp {
    background: linear-gradient(135deg, #f0f9ff 0%, #fdf4ff 50%, #fefce8 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Modern hero with glassmorphism */
.hero {
    padding: 40px;
    border-radius: 32px;
    background: linear-gradient(135deg, #0ea5e9, #8b5cf6, #ec4899);
    color: white;
    box-shadow: 0 25px 60px rgba(14, 165, 233, .4);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%) rotate(45deg); }
    100% { transform: translateX(100%) rotate(45deg); }
}

/* Glassmorphism cards */
.card {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px);
    padding: 28px;
    border-radius: 24px;
    box-shadow: 0 15px 40px rgba(15, 23, 42, .12);
    border: 1px solid rgba(255, 255, 255, 0.6);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 25px 60px rgba(15, 23, 42, .18);
}

.teacher-box {
    background: linear-gradient(135deg, rgba(254, 243, 199, 0.9), rgba(253, 230, 138, 0.9));
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 24px;
    border: 1px solid rgba(245, 158, 11, 0.3);
    box-shadow: 0 10px 30px rgba(245, 158, 11, .15);
}

.score {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,.1);
    border: 1px solid rgba(255, 255, 255, 0.6);
    transition: transform 0.3s ease;
}

.score:hover {
    transform: scale(1.05);
}

/* Modern button styling with animations */
.stButton > button {
    border-radius: 16px;
    padding: 14px 28px;
    font-weight: 600;
    font-size: 16px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    position: relative;
    overflow: hidden;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.stButton > button:hover::before {
    width: 300px;
    height: 300px;
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
}

.stButton > button:active {
    transform: translateY(-2px) scale(0.98);
}

/* Primary button with gradient and glow */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
    border: none;
    color: white;
    box-shadow: 0 6px 20px rgba(14, 165, 233, .4);
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0284c7, #7c3aed);
    box-shadow: 0 12px 35px rgba(14, 165, 233, .6);
}

/* Sidebar with glassmorphism */
.css-1d391kg {
    background: linear-gradient(180deg, rgba(240, 249, 255, 0.95) 0%, rgba(255, 255, 255, 0.98) 100%);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.5);
}

/* Modern input styling */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: 12px;
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.9);
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
    outline: none;
}

/* Modern selectbox styling */
.stSelectbox > div > div > select {
    border-radius: 12px;
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.9);
}

.stSelectbox > div > div > select:focus {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
    outline: none;
}

/* Metric cards with glassmorphism */
.stMetric {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.6);
    box-shadow: 0 8px 25px rgba(15, 23, 42, .1);
    transition: all 0.3s ease;
}

.stMetric:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(15, 23, 42, .15);
}

/* Expander with modern styling */
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.6);
    padding: 16px;
    transition: all 0.3s ease;
}

.streamlit-expanderHeader:hover {
    background: rgba(255, 255, 255, 1);
    box-shadow: 0 4px 15px rgba(15, 23, 42, .1);
}

/* Progress bar with gradient */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #0ea5e9, #8b5cf6, #ec4899);
    background-size: 200% 200%;
    animation: progressGradient 3s ease infinite;
}

@keyframes progressGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Info/success/warning boxes with glassmorphism */
.stAlert {
    backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.6);
    box-shadow: 0 8px 25px rgba(15, 23, 42, .1);
}

/* Smooth scroll behavior */
html {
    scroll-behavior: smooth;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(240, 249, 255, 0.5);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #0284c7, #7c3aed);
}

/* Mobile Responsive Styles */
@media (max-width: 768px) {
    .stApp {
        font-size: 14px;
    }
    
    .hero {
        padding: 24px;
        border-radius: 20px;
    }
    
    .hero h1 {
        font-size: 24px !important;
    }
    
    .card {
        padding: 20px;
        border-radius: 16px;
    }
    
    .stButton > button {
        padding: 12px 20px;
        font-size: 14px;
        min-height: 48px;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-size: 16px;
        padding: 12px;
    }
    
    .stSelectbox > div > div > select {
        font-size: 16px;
        padding: 12px;
    }
    
    .stMetric {
        padding: 16px;
        font-size: 14px;
    }
    
    /* Sidebar mobile optimization */
    .css-1d391kg {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Hide sidebar on mobile by default, show with toggle */
    @media (max-width: 640px) {
        .css-1d391kg {
            display: none;
        }
        
        .css-1d391kg.mobile-visible {
            display: block;
            position: fixed;
            top: 0;
            left: 0;
            width: 80% !important;
            max-width: 300px !important;
            height: 100vh;
            z-index: 9999;
            overflow-y: auto;
        }
    }
    
    /* Mobile navigation toggle button */
    .mobile-nav-toggle {
        display: block !important;
        position: fixed;
        top: 16px;
        right: 16px;
        z-index: 10000;
        background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
        border: none;
        border-radius: 12px;
        padding: 12px 16px;
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
        cursor: pointer;
    }
    
    /* Adjust columns for mobile */
    .stColumns {
        flex-direction: column !important;
    }
    
    .stColumns > div {
        width: 100% !important;
        margin-bottom: 16px;
    }
    
    /* Touch-friendly spacing */
    .streamlit-expanderHeader {
        padding: 20px;
        min-height: 56px;
    }
    
    /* Optimize chat for mobile */
    .chat-message {
        padding: 16px;
        margin: 8px 0;
        border-radius: 12px;
    }
    
    /* Voice input mobile optimization */
    iframe {
        max-width: 100%;
    }
}
</style>
""", unsafe_allow_html=True)
