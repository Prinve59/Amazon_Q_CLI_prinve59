"""
Leaderboard functionality for the game
"""
import pygame
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, VALORANT_RED, VALORANT_BLUE
from core.utils import draw_text, load_json, save_json

class LeaderboardManager:
    """
    Manages the game's leaderboard data
    """
    def __init__(self, scores_file):
        """
        Initialize the leaderboard manager
        
        Args:
            scores_file (str): Path to the scores JSON file
        """
        self.scores_file = scores_file
        self.scores = load_json(scores_file) or {}
        
    def add_score(self, mode, difficulty, score_data):
        """
        Add a new score to the leaderboard
        
        Args:
            mode (str): Game mode
            difficulty (str): Difficulty level
            score_data (dict): Score data dictionary
        """
        # Create mode entry if it doesn't exist
        if mode not in self.scores:
            self.scores[mode] = {}
            
        # Create difficulty entry if it doesn't exist
        if difficulty not in self.scores[mode]:
            self.scores[mode][difficulty] = []
            
        # Add the score
        self.scores[mode][difficulty].append(score_data)
        
        # Sort scores by value (descending)
        self.scores[mode][difficulty].sort(key=lambda x: x["score"], reverse=True)
        
        # Keep only top 10 scores
        if len(self.scores[mode][difficulty]) > 10:
            self.scores[mode][difficulty] = self.scores[mode][difficulty][:10]
            
        # Save to file
        save_json(self.scores, self.scores_file)
        
    def get_high_score(self, mode, difficulty):
        """
        Get the high score for a specific mode and difficulty
        
        Args:
            mode (str): Game mode
            difficulty (str): Difficulty level
            
        Returns:
            int: High score or 0 if no scores
        """
        if mode not in self.scores:
            return 0
            
        if difficulty not in self.scores[mode]:
            return 0
            
        if not self.scores[mode][difficulty]:
            return 0
            
        return self.scores[mode][difficulty][0]["score"]
        
    def get_scores(self, mode, difficulty):
        """
        Get all scores for a specific mode and difficulty
        
        Args:
            mode (str): Game mode
            difficulty (str): Difficulty level
            
        Returns:
            list: List of score dictionaries
        """
        if mode not in self.scores:
            return []
            
        if difficulty not in self.scores[mode]:
            return []
            
        return self.scores[mode][difficulty]
        
    def get_modes(self):
        """
        Get all available modes
        
        Returns:
            list: List of mode names
        """
        return list(self.scores.keys())
        
    def get_difficulties(self, mode):
        """
        Get all available difficulties for a mode
        
        Args:
            mode (str): Game mode
            
        Returns:
            list: List of difficulty names
        """
        if mode not in self.scores:
            return []
            
        return list(self.scores[mode].keys())
