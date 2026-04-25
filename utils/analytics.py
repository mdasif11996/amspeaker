import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class AnalyticsManager:
    """Track usage analytics for production monitoring"""
    
    def __init__(self):
        self.session_start = datetime.now()
        self.interactions = 0
        self.errors = 0
    
    def track_interaction(self, interaction_type):
        """Track user interaction"""
        self.interactions += 1
        logger.info(f"Interaction: {interaction_type} (Total: {self.interactions})")
    
    def track_error(self, error_type):
        """Track errors"""
        self.errors += 1
        logger.error(f"Error tracked: {error_type} (Total errors: {self.errors})")
    
    def get_session_stats(self):
        """Get session statistics"""
        duration = datetime.now() - self.session_start
        return {
            "duration": str(duration),
            "interactions": self.interactions,
            "errors": self.errors,
            "session_start": self.session_start.strftime("%Y-%m-%d %H:%M:%S")
        }
