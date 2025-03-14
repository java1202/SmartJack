# Challenges & Learnings

## Challenges

- **Integrating Risk Sensitivity:**  
  Incorporating the bet fraction (current bet relative to starting balance) and remaining balance into the state representation was challenging. It required redefining the state tuple so that the AI can make decisions that reflect the true risk of going “all in.”

- **Balancing Simulation with Interactivity:**  
  Designing a system that supports both rapid simulation for training and interactive gameplay with real-time feedback led to a modular design that could support multiple modes without compromising usability.

- **GUI Design:**  
  Creating a user-friendly Tkinter GUI that initially hides the dealer's hole card—and then reveals the full hand after your turn—required careful state management and conditional display logic.

- **Convergence of the Q-Learning Agent:**  
  Despite running 100,000 simulation episodes, the agent sometimes exhibits counterintuitive decisions (for example, recommending a hit on a strong hand) in edge cases. Fine-tuning the reward function, learning rate, and exploration parameters remains an ongoing challenge.

## Learnings

- **Modular Code Structure:**  
  Breaking the project into distinct modules (game engine, agent, simulation, GUI, analysis) made it easier to isolate issues and extend functionality.
  
- **Importance of Data Representation:**  
  Including the bet fraction in the state representation opened up new insights on how risk and reward are balanced. This has led to further research questions about optimal betting strategies in reinforcement learning contexts.
  
- **Practical AI Considerations:**  
  The project highlights the challenges of translating theoretical reinforcement learning models into practical applications, particularly in environments with a built-in house edge.
  
- **User-Centric Design:**  
  Implementing detailed feedback in the GUI—such as displaying starting balance, current bet, and full dealer information after a round—improves the player experience and helps users better understand game outcomes.

## Interesting Findings

- **Risk vs. Reward Behavior:**  
  Preliminary analysis indicates that the AI’s optimal action shifts significantly with the bet fraction. The agent is more conservative when a larger fraction of the starting balance is wagered.
  
- **Dealer Upcard Influence:**  
  The dealer's visible card remains a critical factor in the AI's decision-making. For instance, when the dealer shows a 4–6, the AI consistently leans toward sticking, aligning with established blackjack strategies.
  
- **Training Dynamics:**  
  Analysis of the moving average reward over 100,000 episodes suggests gradual performance improvement. This demonstrates that even with a simplified reward structure, the Q-learning agent is capable of learning effective, if not optimal, strategies.

## Future Work

- Explore alternative reward functions that scale with the bet size.
- Integrate dynamic betting strategies that adjust based on the current state and risk.
- Expand the analysis with additional visualizations and statistical summaries.
- Investigate more advanced reinforcement learning algorithms (e.g., Deep Q-Networks) for improved decision-making.
