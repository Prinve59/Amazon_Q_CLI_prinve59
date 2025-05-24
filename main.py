#!/usr/bin/env python3
"""
NeuroShot: Reflex Protocol
A fast-paced aim training simulator
"""
import os
import sys
from core.game import Game

def main():
    """Main entry point for the game"""
    # Ensure we're in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Create assets directories if they don't exist
    os.makedirs("assets/images/effects", exist_ok=True)
    os.makedirs("assets/sounds", exist_ok=True)
    os.makedirs("assets/fonts", exist_ok=True)
    
    # Create and run the game
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
