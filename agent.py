import random
from typing import Any, Dict, List, Tuple

State = Tuple[Any, ...]  # A tuple representing the game state

class QLearningAgent:
    def __init__(self, actions: List[str], alpha: float = 0.1, gamma: float = 0.9, epsilon: float = 0.1) -> None:
        """
        Q-learning agent for blackjack.
        :param actions: List of possible actions (e.g., ["hit", "stick"]).
        :param alpha: Learning rate.
        :param gamma: Discount factor.
        :param epsilon: Exploration rate.
        """
        self.Q: Dict[State, Dict[str, float]] = {}  # Q-table: state -> action -> value
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = actions

    def get_Q(self, state: State, action: str) -> float:
        return self.Q.get(state, {}).get(action, 0.0)

    def select_action(self, state: State) -> str:
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            q_values = {a: self.get_Q(state, a) for a in self.actions}
            max_q = max(q_values.values())
            best_actions = [a for a, q in q_values.items() if q == max_q]
            return random.choice(best_actions)

    def update(self, state: State, action: str, reward: float, next_state: State, done: bool) -> None:
        current_q = self.get_Q(state, action)
        max_next_q = 0 if done else max(self.get_Q(next_state, a) for a in self.actions)
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        if state not in self.Q:
            self.Q[state] = {}
        self.Q[state][action] = new_q
