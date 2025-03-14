# SmartJack: AI-Powered Blackjack Game with Reinforcement Learning

## Overview

This project implements an AI-powered blackjack game that combines a simulation engine, reinforcement learning, and data analysis with risk-sensitive decision making. The game features:

- **Multi-Player Support:** A human player, an AI player (trained via Q-learning), and a dealer.

- **Risk-Sensitive State:** The game factors in a player’s balance (categorized as "low", "medium", or "high") to affect decisions.
- **Interactive and Simulation Modes:** Play interactively with AI suggestions or run large-scale simulations to train the AI.
- **Analytical Insights:** Generate charts showing estimated win probabilities and optimal actions based on various state parameters.
- **GUI:** A Tkinter-based interface that displays card representations and interactive controls.

## Features

- **Reinforcement Learning:** Q-learning algorithm that learns optimal actions based on hand total, dealer’s card, usable ace, and balance risk.
- **Simulation & Analysis:** Run thousands of simulated rounds to train the AI and then analyze its learned policy.
- **User Interface:** Command-line interactive mode with AI suggestions and a GUI mode with a card display.
- **Testing & CI/CD:** Unit tests ensure correctness; GitHub Actions runs tests on every commit.

## Setup and Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/java1202/SmartJack.git
   cd SmartJack
