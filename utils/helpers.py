import re
import logging

logger = logging.getLogger(__name__)


def extract_scores(text):
    """Extract scores from AI feedback text"""
    scores = {
        "overall": 70,
        "grammar": 70,
        "vocabulary": 70,
        "fluency": 70,
        "communication": 70,
        "pronunciation": 70,
    }

    for key in scores:
        match = re.search(rf"{key}\s*[:\-]\s*(\d+)", text, re.IGNORECASE)
        if match:
            scores[key] = max(0, min(100, int(match.group(1))))

    return scores
