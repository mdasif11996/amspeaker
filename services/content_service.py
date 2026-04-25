import logging
import json
import ast
from datetime import datetime, timedelta
from openai import OpenAI
from config.settings import config
from utils.decorators import handle_errors, monitor_performance
from utils.cache import CacheManager

logger = logging.getLogger(__name__)


class ContentService:
    """Service for managing dynamic content (topics, vocabulary, idioms)"""
    
    def __init__(self):
        self.client = OpenAI(
            base_url=config.api_base_url,
            api_key=config.api_key
        )
        self.cache = CacheManager()
        self.default_vocab = [
            ("articulate", "express clearly", "I want to articulate my thoughts better."),
            ("fluent", "flowing smoothly", "Speaking practice helps me become more fluent."),
            ("pronunciation", "way words are spoken", "Good pronunciation makes communication easier."),
            ("conversation", "natural dialogue", "I enjoy having conversations in English."),
            ("expressive", "showing feelings", "Being expressive makes speaking more engaging.")
        ]
        self.default_idioms = [
            ("On the same page", "understanding each other", "We're on the same page about this topic."),
            ("Get the hang of", "become skilled at", "I'm getting the hang of speaking English."),
            ("Keep the ball rolling", "continue conversation", "Let's keep the ball rolling with more practice."),
            ("Speak your mind", "express your opinion", "Don't be afraid to speak your mind.")
        ]
        self.default_topics = {
            "Beginner": [
                "Introduce yourself naturally",
                "Talk about your daily routine",
                "Describe your family members",
                "Talk about your hobbies",
                "Share what you did yesterday"
            ],
            "Intermediate": [
                "Your daily routine and habits",
                "Hobbies and interests",
                "Work or school experiences",
                "Travel and adventures",
                "Food and cooking",
                "Movies and entertainment",
                "Technology and gadgets",
                "Future goals and dreams"
            ],
            "Advanced": [
                "Debate current events",
                "Discuss business trends",
                "Talk about leadership",
                "Explain complex ideas simply",
                "Discuss global issues"
            ]
        }
    
    @handle_errors
    @monitor_performance
    def generate_dynamic_topics(self, level):
        """Generate conversation topics dynamically based on level with caching"""
        cache_key = f"topics_{level}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            logger.info(f"Returning cached topics for level: {level}")
            return cached_result
        
        prompt = f"""
        Generate 8-10 engaging conversation topics for an English learner at {level} level.
        Topics should be relevant to daily life, current events, personal interests, and practical situations.
        
        Return only a Python list of topic strings, no other text.
        Format: ["Topic 1", "Topic 2", "Topic 3", ...]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=config.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=300
            )
            
            topics_text = response.choices[0].message.content
            topics = ast.literal_eval(topics_text)
            result = topics if isinstance(topics, list) else self.default_topics.get(level, self.default_topics["Intermediate"])
            self.cache.set(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"Error generating topics: {e}")
            return self.default_topics.get(level, self.default_topics["Intermediate"])
    
    @handle_errors
    @monitor_performance
    def fetch_daily_content_from_internet(self):
        """Fetch fresh daily speaking vocabulary from internet sources"""
        try:
            prompt = """
            Based on today's current events and trending topics, generate SPEAKING vocabulary for English learners.
            
            Return ONLY this exact JSON format, nothing else:
            {
                "topics": ["topic1", "topic2", "topic3"],
                "vocabulary": [
                    ["word1", "meaning1", "speaking_example1"],
                    ["word2", "meaning2", "speaking_example2"]
                ],
                "idioms": [
                    ["idiom1", "meaning1", "speaking_example1"],
                    ["idiom2", "meaning2", "speaking_example2"]
                ]
            }
            
            Generate 6-8 topics, 4-6 vocabulary words, and 2-4 idioms. Focus on SPEAKING and conversation.
            """
            
            response = self.client.chat.completions.create(
                model=config.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=600
            )
            
            content_text = response.choices[0].message.content.strip()
            
            # Clean up the response to extract JSON
            if "```json" in content_text:
                content_text = content_text.split("```json")[1].split("```")[0].strip()
            elif "```" in content_text:
                content_text = content_text.split("```")[1].split("```")[0].strip()
            
            # Parse the JSON response
            content = json.loads(content_text)
            
            # Validate the structure
            if not all(key in content for key in ["topics", "vocabulary", "idioms"]):
                raise ValueError("Invalid content structure")
            
            logger.info("Daily speaking vocabulary fetched successfully")
            return content
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching daily speaking vocabulary: {e}")
            return None
    
    def should_update_daily_content(self, last_updated):
        """Check if daily content needs to be updated (older than 24 hours)"""
        if last_updated is None:
            return True
        
        time_diff = datetime.now() - last_updated
        return time_diff > timedelta(hours=24)
    
    @handle_errors
    def update_daily_content(self, current_daily_content):
        """Update all daily content streams (vocabulary, idioms, topics) from internet"""
        if self.should_update_daily_content(current_daily_content.get("last_updated")):
            content = self.fetch_daily_content_from_internet()
            if content:
                return {
                    "last_updated": datetime.now(),
                    "vocabulary": content.get("vocabulary", self.default_vocab),
                    "idioms": content.get("idioms", self.default_idioms),
                    "topics": content.get("topics", []),
                    "exercises": []
                }
        return None
    
    def get_default_vocab(self):
        """Return default vocabulary"""
        return self.default_vocab
    
    def get_default_idioms(self):
        """Return default idioms"""
        return self.default_idioms
    
    def get_default_topics(self, level):
        """Return default topics for a level"""
        return self.default_topics.get(level, self.default_topics["Intermediate"])
