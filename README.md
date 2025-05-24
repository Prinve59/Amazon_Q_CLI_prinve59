# NeuroShot: Reflex Protocol

A fast-paced, sci-fi themed aim training simulator where players undergo neural reflex training by eliminating moving and disappearing "glitches" in a simulated VR world.

## Features

- **Multiple Training Modes**:
  - **Flick Precision**: Test your reaction time and precision by hitting targets that appear randomly.
  - **Tracking**: Keep your crosshair on moving targets for as long as possible.
  - **Target Switch**: Quickly switch between multiple targets in sequence.
  - **Spike Diffuse**: Hit the core nodes while avoiding decoys, simulating spike defusal under pressure.

- **Difficulty Levels**:
  - Easy: Larger, slower targets with longer lifetimes. Perfect for beginners.
  - Medium: Balanced difficulty for regular practice.
  - Hard: Smaller, faster targets with shorter lifetimes. For experienced players.
  - Extreme: Tiny, very fast targets that disappear quickly. For elite players only.

- **Performance Tracking**:
  - Score tracking
  - Accuracy percentage
  - Reaction time measurement
  - Headshot counter
  - Local leaderboards

- **Customization**:
  - Crosshair styles (default, dot, circle, valorant)
  - Crosshair colors
  - Display settings

## Controls

- **Mouse**: Aim
- **Left Click**: Shoot
- **R**: Reload
- **ESC**: Pause/Menu navigation
- **Space**: Continue (after game over)

## Requirements

- Python 3.6+
- Pygame 2.0+

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/neuroshot.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the game:
   ```
   python main.py
   ```

## Project Structure

```
neuroshot/
├── assets/
│   ├── images/
│   ├── sounds/
│   └── fonts/
├── core/
│   ├── game.py
│   ├── settings.py
│   └── utils.py
├── entities/
│   ├── player.py
│   ├── target.py
│   └── effects.py
├── modes/
│   ├── flick.py
│   ├── tracking.py
│   ├── switch.py
│   └── spike.py
├── ui/
│   ├── hud.py
│   ├── menu.py
│   └── leaderboard.py
├── data/
│   ├── scores.json
│   └── settings.json
├── main.py
└── README.md
```

## Future Enhancements

- Online leaderboards
- Custom training scenarios
- Weapon spray patterns
- Audio reflex training
- Multiplayer training rooms
