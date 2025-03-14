# SmartJack: AI-Powered Blackjack Simulator

## Overview

**SmartJack** is an AI-powered blackjack simulator that combines reinforcement learning with real-time gameplay, simulation, and analysis. The project is designed to mimic realistic blackjack strategies by factoring in:

- **Player’s Hand:** Total value and whether a usable Ace is present.
- **Dealer’s Upcard:** Only the first card is visible during play; the second is revealed after your turn.
- **Risk Sensitivity:** The AI considers your remaining balance by categorizing it into "low," "medium," or "high" risk levels.
- **Bet Size:** The current bet (expressed as a fraction of your starting balance) is part of the state, allowing the AI to adjust its decisions based on how much you risk each round.

## Features

- **Reinforcement Learning:** Utilizes Q-learning to learn an optimal policy over many simulation runs (default is 100,000 episodes).
- **Risk-Sensitive State:** Incorporates both remaining balance and bet fraction into the AI’s decision-making.
- **Multiple Modes:**  
  - **Simulation Mode:** Train the AI with numerous episodes and visualize the performance using moving average reward charts.  
  - **Interactive CLI Mode:** Play blackjack interactively in the terminal with AI suggestions.
  - **Graphical User Interface (GUI):** A Tkinter-based GUI that displays card representations, your hand, your balance, and (after your turn) the dealer’s full hand.
- **Analysis Tools:** Generate charts to view the AI’s estimated win probabilities and suggested actions across various state combinations.
- **Extensible Design:** The project is modular and designed to be expanded with additional features (e.g., real card images or advanced betting strategies).

## Setup & Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/java1202/SmartJack.git
   cd SmartJack

2. **Create & Activate a Virtual Environment:**

   ```bash
    python -m venv venv
    # On Windows PowerShell (after setting ExecutionPolicy appropriately):
    .\venv\Scripts\Activate.ps1
    # On macOS/Linux:
    source venv/bin/activate

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    
4. **Run Tests:**

    ```bash
    python -m pytest tests/

## Usage

- **Training Mode:**
  
  Train the AI with simulation runs (default 100,000 episodes) and view a moving average of rewards:

    ```bash
    python simulation.py

- **Interactive CLI Mode:**
  
  Play blackjack interactively in the terminal:

    ```bash
    python main.py

- **Graphical User Interface (GUI) Mode:**
  
  Launch the GUI to play with visual card representations and detailed results:

    ```bash
    python gui_app.py

- **Analysis:**
  
  Generate charts displaying the AI’s estimated win probabilities and suggested actions:

    ```bash
    python analysis.py

## Interesting Findings

This section is a placeholder for insights discovered during training and analysis. Some preliminary findings include:

- Risk vs. Reward Behavior:
The AI tends to adopt a more conservative (stick) strategy when the bet fraction is high—even if the dealer’s upcard is weak.
- Dealer Upcard Impact:
The dealer's visible card greatly influences the optimal action, aligning with common blackjack strategies (e.g., sticking when the dealer shows 4–6).
- Training Dynamics:
Over 100,000 episodes, the moving average reward shows gradual improvement, suggesting that the agent is learning an increasingly effective strategy despite the inherent house edge.
Feel free to update this section with additional insights as you further analyze your simulation data.

## Files in the Repository

Ensure that your repository includes the following:

- Source Code: agent.py, analysis.py, blackjack_multi.py, gui.py, gui_app.py, main.py, simulation.py
- Tests: tests/test_blackjack.py
- Configuration: requirements.txt, .github/workflows/python-app.yml, and a proper .gitignore (exclude venv/, __pycache__/, etc.)
- Documentation: This README.md and the accompanying CHALLENGES.md

## Future Enhancements

- Integrate real card images for a more engaging GUI experience.
- Refine the state representation by further exploring dynamic betting strategies.
- Experiment with alternative reinforcement learning algorithms.
- Expand the analysis section with automated visualization tools and deeper statistical metrics.
