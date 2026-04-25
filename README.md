# AMspeaker - AI English Speaking Coach

A modern, multi-page Streamlit application for mastering spoken English with AI-powered conversation partners.

## Architecture Overview

This application follows a clean, modular architecture with separation of concerns and multi-page structure:

```
streamlit_app/
├── app.py                 # Main landing/home page
├── pages/                 # Multi-page structure (Streamlit native)
│   ├── 1_Conversation.py      # Conversation practice page
│   ├── 2_Voice_Chat.py         # Voice chat page
│   ├── 3_Vocabulary.py         # Vocabulary practice page
│   ├── 4_Expressions.py        # Natural expressions page
│   ├── 5_Idioms.py             # Idioms practice page
│   ├── 6_Interview.py          # Interview practice page
│   ├── 7_Progress.py           # Progress tracking page
│   └── 8_News.py               # News vocabulary page
├── config/                # Configuration management
│   ├── __init__.py
│   └── settings.py       # AppConfig class with environment variables
├── services/              # Business logic layer
│   ├── __init__.py
│   ├── ai_service.py      # AI conversation and feedback service
│   └── content_service.py # Dynamic content management (topics, vocab, idioms)
├── ui/                    # User interface components
│   ├── __init__.py
│   ├── styles.py          # Custom CSS styling (SpeakX branding)
│   ├── voice.py           # Voice input/output components
│   ├── pages.py           # Legacy page rendering functions
│   └── sidebar.py         # Sidebar component
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── decorators.py      # Error handling and performance decorators
│   ├── cache.py           # In-memory caching
│   ├── analytics.py       # Session analytics tracking
│   └── helpers.py         # Helper functions (score extraction)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
└── README.md             # This file
```

## Module Descriptions

### app.py
Main landing/home page featuring:
- Hero section with SpeakX branding
- Practice mode cards for navigation
- Quick start guide
- Session state initialization

### pages/ (Multi-page Structure)
Streamlit's native multi-page system with numbered files for ordering:

- **1_Conversation.py**: Main conversation practice with AI
- **2_Voice_Chat.py**: Pure voice-to-voice conversation
- **3_Vocabulary.py**: Vocabulary learning and practice
- **4_Expressions.py**: Natural expressions for fluency
- **5_Idioms.py**: Idioms practice for native-like speech
- **6_Interview.py**: Job interview question practice
- **7_Progress.py**: Progress tracking and reports
- **8_News.py**: Daily news vocabulary from current events

### config/settings.py
Centralized configuration management using environment variables:
- API keys and endpoints
- Cache TTL settings
- Analytics configuration
- Environment detection (development/production)
- Version management

### services/ai_service.py
Handles all AI-related operations:
- Conversation with AI teacher
- Dynamic vocabulary generation
- Personalized exercise generation
- Score extraction from AI responses
- Error handling for API rate limits

### services/content_service.py
Manages dynamic content:
- AI-generated conversation topics
- Daily vocabulary and idioms from current events
- Content caching with TTL
- Fallback to default content when API fails

### ui/styles.py
Custom CSS styling for SpeakX branding:
- Modern gradient backgrounds (sky blue to purple)
- Card and hero components
- Button styling with hover effects
- Responsive design elements
- SpeakX brand color scheme

### ui/voice.py
Voice input/output components:
- Browser-based speech recognition
- Text-to-speech playback
- Voice recording controls
- Microphone permission handling

### ui/sidebar.py
Sidebar component with:
- System status display
- Session analytics
- Daily content update controls
- Practice mode selection
- Quick start guide

### utils/decorators.py
Python decorators for:
- `@handle_errors`: Graceful error handling with logging
- `@monitor_performance`: Function execution time tracking

### utils/cache.py
In-memory caching system:
- Key-value storage with timestamps
- TTL-based expiration
- Cache clearing functionality

### utils/analytics.py
Session analytics tracking:
- Interaction counting
- Error tracking
- Session duration monitoring
- Statistics reporting

### utils/helpers.py
Helper functions:
- Score extraction from AI feedback text
- Data validation utilities

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_api_key_here
LOG_LEVEL=INFO
CACHE_TTL=3600
MAX_HISTORY_ITEMS=100
ENABLE_ANALYTICS=true
ENVIRONMENT=development
```

Get a free Groq API key from: https://console.groq.com/

## Running the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Features

- **Multi-Page Architecture**: Native Streamlit multi-page navigation
- **Voice-to-Voice Conversation**: Practice speaking with AI using browser speech recognition
- **Multiple Practice Modes**: Casual, Interview, Formal, Debate, Storytelling
- **Dynamic Content**: AI-generated topics, vocabulary, and idioms updated daily
- **Real-time Feedback**: Instant AI feedback with speaking metrics
- **Progress Tracking**: Track your improvement over time
- **Personalized Exercises**: AI generates exercises based on your weaknesses
- **Audio Playback**: Listen to AI responses with text-to-speech
- **Modern UI**: SpeakX branding with gradient colors and card-based design

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key for AI services | Required |
| `LOG_LEVEL` | Logging level (INFO, DEBUG, ERROR) | INFO |
| `CACHE_TTL` | Cache time-to-live in seconds | 3600 |
| `MAX_HISTORY_ITEMS` | Maximum conversation history items | 100 |
| `ENABLE_ANALYTICS` | Enable session analytics | true |
| `ENVIRONMENT` | Environment (development, production) | development |

## Development

### Adding New Features

1. **New Service**: Add to `services/` directory
2. **New UI Component**: Add to `ui/` directory
3. **New Utility**: Add to `utils/` directory
4. **New Page**: Add function to `ui/pages.py` and route in `app.py`

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Use decorators for error handling and performance monitoring

### Testing

The application includes built-in error handling and logging. Check `app.log` for runtime errors and performance metrics.

## Production Deployment

1. Set `ENVIRONMENT=production` in `.env`
2. Use a production-grade WSGI server
3. Enable proper logging and monitoring
4. Set up rate limiting for API calls
5. Use environment-specific API keys

## License

This project is for educational purposes.

## Support

For issues or questions, please check the application logs or review the code documentation.
