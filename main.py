import pickle
from blackjack_multi import BlackjackGameMulti, Player
from agent import QLearningAgent

def play_multiplayer_round(game: BlackjackGameMulti, ai_suggester=None) -> None:
    human = game.players[0]
    print(f"Your starting balance is: {human.balance} (Initial: {human.starting_balance})")
    try:
        bet_amount = int(input("Enter your bet amount for this round: "))
    except ValueError:
        bet_amount = 10
    game.place_bets(bet_amount=bet_amount)
    game.deal_initial()
    for player in game.players:
        game.player_turn(player, agent=ai_suggester)
    game.dealer_turn()
    results = game.settle_bets()
    print("\nRound results:")
    for name, result in results.items():
        print(f"{name}: {result}")
    print("\nCurrent balances:")
    for player in game.players:
        print(f"{player.name}: {player.balance} (Initial: {player.starting_balance})")
    print("-" * 40)

def interactive_main() -> None:
    human = Player("Human", balance=100, is_human=True)
    ai_player = Player("AI_Player", balance=100, is_human=False)
    game = BlackjackGameMulti(players=[human, ai_player])
    try:
        with open("q_table.pkl", "rb") as f:
            data = pickle.load(f)
            q_table = data["Q"]
            episodes_trained = data.get("episodes", 0)
        ai_agent = QLearningAgent(actions=["hit", "stick"], epsilon=0)
        ai_agent.Q = q_table
        if episodes_trained >= 1000:
            print(f"Loaded trained Q-table with {episodes_trained} episodes. AI suggestions enabled.")
            agent_for_suggestion = ai_agent
        else:
            print("Q-table exists but with insufficient training episodes. AI suggestions disabled.")
            agent_for_suggestion = None
    except Exception as e:
        print("Could not load trained Q-table, starting with an untrained agent.")
        ai_agent = QLearningAgent(actions=["hit", "stick"], epsilon=0)
        agent_for_suggestion = None
    while True:
        play_multiplayer_round(game, ai_suggester=agent_for_suggestion)
        cont = input("Play another round? (y/n): ").strip().lower()
        if cont != "y":
            break

def training_mode() -> None:
    from blackjack_multi import BlackjackGameMulti, Player
    sim_human = Player("Sim_Human", balance=100, is_human=False)
    ai_player = Player("AI_Player", balance=100, is_human=False)
    game = BlackjackGameMulti(players=[sim_human, ai_player])
    ai_agent = QLearningAgent(actions=["hit", "stick"], alpha=0.1, gamma=0.9, epsilon=0.1)
    try:
        episodes = int(input("Enter number of training episodes (e.g., 100000): "))
    except ValueError:
        episodes = 100000
    rewards_history = []
    import random
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
                    action = ai_agent.select_action(state)
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
        ai_agent.update(state, action, reward, state, done=True)
        if i % (max(episodes // 10, 1)) == 0:
            print(f"Episode {i}: reward = {reward}")
    with open("q_table.pkl", "wb") as f:
        pickle.dump({"Q": ai_agent.Q, "episodes": episodes}, f)
    from gui import plot_training_rewards_moving_average
    plot_training_rewards_moving_average(rewards_history, window_size=1000)

def main() -> None:
    mode = input("Choose mode (interactive/training): ").strip().lower()
    if mode == "interactive":
        interactive_main()
    elif mode == "training":
        training_mode()
    else:
        print("Invalid mode. Exiting.")

if __name__ == "__main__":
    main()
