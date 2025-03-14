import pickle
import random
from blackjack_multi import BlackjackGameMulti, Player
from agent import QLearningAgent
from gui import plot_training_rewards_moving_average

def train(agent: QLearningAgent, episodes: int = 100000):
    """
    Train the Q-learning agent by running simulated blackjack episodes.
    """
    sim_human = Player("Sim_Human", balance=100, is_human=False)
    ai_player = Player("AI_Player", balance=100, is_human=False)
    game = BlackjackGameMulti(players=[sim_human, ai_player])
    rewards_history = []
    for i in range(episodes):
        sim_human.balance = 100
        ai_player.balance = 100
        game.place_bets(bet_amount=10)
        game.deal_initial()
        for player in game.players:
            while True:
                state = game.get_state(player)
                if player.name == "Sim_Human":
                    action = random.choice(["hit", "stick"])
                else:
                    action = agent.select_action(state)
                if action == "hit":
                    player.hand.append(game.deal_card())
                    if game.get_hand_value(player.hand) > 21:
                        break
                else:
                    break
        game.dealer_turn()
        dealer_total = game.get_hand_value(game.dealer.hand)
        ai_total = game.get_hand_value(ai_player.hand)
        if ai_total > 21:
            reward = -1
        elif dealer_total > 21 or ai_total > dealer_total:
            reward = 1
        elif ai_total == dealer_total:
            reward = 0
        else:
            reward = -1
        rewards_history.append(reward)
        state = game.get_state(ai_player)
        agent.update(state, action, reward, state, done=True)
        if i % (max(episodes // 10, 1)) == 0:
            print(f"Episode {i}: reward = {reward}")
    return agent, rewards_history

if __name__ == "__main__":
    actions = ["hit", "stick"]
    agent = QLearningAgent(actions, alpha=0.1, gamma=0.9, epsilon=0.1)
    episodes = 100000
    trained_agent, rewards_history = train(agent, episodes=episodes)
    with open("q_table.pkl", "wb") as f:
        pickle.dump({"Q": trained_agent.Q, "episodes": episodes}, f)
    plot_training_rewards_moving_average(rewards_history, window_size=1000)
