import logging
from openai import OpenAI
from config.settings import config
from utils.decorators import handle_errors, monitor_performance
from utils.helpers import extract_scores

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI-powered conversation and feedback"""
    
    def __init__(self):
        self.client = OpenAI(
            base_url=config.api_base_url,
            api_key=config.api_key
        )
        logger.info(f"AIService initialized with model: {config.model_name}")
    
    @handle_errors
    @monitor_performance
    def ask_ai_teacher(self, user_text, level, topic, mode, conversation_mode="Casual", memory=None):
        """Get AI response for user's speech with feedback"""
        if memory is None:
            memory = []
        
        memory_text = "\n".join(
            [f"Student: {m['student']}\nTeacher: {m['teacher']}" for m in memory[-4:]]
        )

        mode_instructions = {
            "Casual": "Keep it friendly, informal, and relaxed like chatting with a friend",
            "Interview": "Be professional, ask job-related questions, evaluate their responses",
            "Formal": "Use formal language, proper etiquette, suitable for business settings",
            "Debate": "Challenge their views, ask for arguments, encourage critical thinking",
            "Storytelling": "Encourage them to tell stories, ask for details, make it engaging"
        }

        prompt = f"""
You are AMspeaker, a friendly human-like English conversation partner. Your goal is to help the student improve their spoken English through natural conversation.

IMPORTANT: You are NOT a teacher giving lessons. You are a conversation partner having a real dialogue.
- Respond naturally like a real person would in conversation
- Keep responses conversational, engaging, and brief (2-3 sentences)
- Don't sound like a textbook or AI
- Use contractions, casual language, and natural expressions
- Be encouraging, positive, and supportive
- Ask follow-up questions to keep the conversation going naturally
- Show genuine interest in what the student says
- React appropriately to their statements (agree, express surprise, ask for details)
- Build on the conversation context from previous messages

Student level: {level}
Topic: {topic}
Conversation Mode: {conversation_mode}
Mode Instruction: {mode_instructions.get(conversation_mode, mode_instructions['Casual'])}

Previous conversation context:
{memory_text}

Student just said:
{user_text}

Your response should:
1. Respond naturally to what they said (like a real conversation partner would)
2. Show interest and engagement with their statement
3. Gently correct 1-2 major errors if present, but don't over-correct or interrupt the flow
4. Suggest a more natural way to say something if it sounds too formal or awkward
5. Ask a relevant follow-up question to continue the conversation naturally
6. Keep it brief and conversational
7. Adapt your tone to the {conversation_mode} conversation mode

Format:
[Your natural conversational response - 2-3 sentences, engaging and natural]

💡 Quick tip: [1 brief, practical speaking tip for {conversation_mode} conversations]

❓ Follow-up: [Natural follow-up question related to what they said]
"""

        try:
            response = self.client.chat.completions.create(
                model=config.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )

            feedback = response.choices[0].message.content
            scores = extract_scores(feedback)
            logger.info(f"AI response generated successfully for user: {user_text[:50]}...")
            return feedback, scores
        except Exception as e:
            logger.error(f"Error in AI response generation: {e}")
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                feedback = """
⚠️ **API Rate Limit Exceeded**

The Groq API rate limit has been reached. Please:
1. Wait a moment and try again
2. Get a free API key from https://console.groq.com/
3. Verify your GROQ_API_KEY in .env file

Groq offers generous free tier limits for development.
"""
                scores = extract_scores(feedback)
            else:
                feedback = "I apologize, but I'm having trouble responding right now. Please try again."
                scores = {"overall": 0, "grammar": 0, "vocabulary": 0, "fluency": 0, "communication": 0, "pronunciation": 0}
            return feedback, scores
    
    @handle_errors
    @monitor_performance
    def generate_dynamic_vocabulary(self, topic, conversation_context):
        """Generate vocabulary dynamically based on topic and conversation"""
        prompt = f"""
    Generate 5-8 vocabulary words that would be useful for this conversation.
    Topic: {topic}
    Context: {conversation_context}
    
    For each word, provide the word, meaning, and an example sentence.
    
    Return as a list of tuples: [("word", "meaning", "example"), ...]
    Format: [("word", "meaning", "example"), ...]
    """
        
        try:
            response = self.client.chat.completions.create(
                model=config.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            vocab_text = response.choices[0].message.content
            import ast
            vocab = ast.literal_eval(vocab_text)
            return vocab if isinstance(vocab, list) else self._get_default_vocab()[:5]
        except:
            return self._get_default_vocab()[:5]
    
    @handle_errors
    @monitor_performance
    def generate_dynamic_exercise(self, level, topic, conversation_mode, user_weakness):
        """Generate a speaking exercise dynamically based on user's needs"""
        prompt = f"""
    Create a speaking exercise for an English learner at {level} level.
    Topic: {topic}
    Conversation mode: {conversation_mode}
    User's weakness to address: {user_weakness}
    
    Generate a specific exercise with:
    1. Exercise title
    2. Clear instructions
    3. Expected outcome
    4. Time limit (if applicable)
    
    Keep it practical and actionable.
    """
        
        try:
            response = self.client.chat.completions.create(
                model=config.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            return response.choices[0].message.content
        except:
            return "Exercise: Practice speaking about the topic for 2 minutes without stopping. Focus on using natural expressions and maintaining flow."
    
    def _get_default_vocab(self):
        """Return default vocabulary as fallback"""
        return [
            ("articulate", "express clearly", "I want to articulate my thoughts better."),
            ("fluent", "flowing smoothly", "Speaking practice helps me become more fluent."),
            ("pronunciation", "way words are spoken", "Good pronunciation makes communication easier."),
            ("conversation", "natural dialogue", "I enjoy having conversations in English."),
            ("expressive", "showing feelings", "Being expressive makes speaking more engaging.")
        ]
