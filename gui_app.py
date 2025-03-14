import tkinter as tk
from tkinter import messagebox
from blackjack_multi import BlackjackGameMulti, Player, categorize_balance
from agent import QLearningAgent

# Utility function to convert card value to a string representation.
def card_to_str(card: int) -> str:
    if card == 11:
        return "A"
    elif card == 10:
        return "10"  # Could represent 10 or face card
    else:
        return str(card)

class BlackjackGUI:
    def __init__(self, master):
        self.master = master
        master.title("AI-Powered Blackjack")
        self.game = BlackjackGameMulti(players=[Player("Human", balance=100, is_human=True),
                                                 Player("AI_Player", balance=100, is_human=False)])
        try:
            with open("q_table.pkl", "rb") as f:
                import pickle
                data = pickle.load(f)
                q_table = data["Q"]
                episodes_trained = data.get("episodes", 0)
            self.ai_agent = QLearningAgent(actions=["hit", "stick"], epsilon=0)
            self.ai_agent.Q = q_table
            self.enable_suggestion = episodes_trained >= 1000
        except Exception as e:
            self.ai_agent = QLearningAgent(actions=["hit", "stick"], epsilon=0)
            self.enable_suggestion = False

        self.create_widgets()
        self.start_new_round()

    def create_widgets(self):
        self.dealer_label = tk.Label(self.master, text="Dealer's Hand: ", font=("Helvetica", 14))
        self.dealer_label.pack(pady=5)

        self.player_label = tk.Label(self.master, text="Your Hand: ", font=("Helvetica", 14))
        self.player_label.pack(pady=5)

        self.balance_label = tk.Label(self.master, text="Your Balance: ", font=("Helvetica", 12))
        self.balance_label.pack(pady=5)

        self.suggestion_label = tk.Label(self.master, text="", font=("Helvetica", 12), fg="blue")
        self.suggestion_label.pack(pady=5)

        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)
        self.hit_button = tk.Button(button_frame, text="Hit", command=self.hit)
        self.hit_button.pack(side="left", padx=5)
        self.stick_button = tk.Button(button_frame, text="Stick", command=self.stick)
        self.stick_button.pack(side="left", padx=5)

        self.restart_button = tk.Button(self.master, text="New Round", command=self.start_new_round)
        self.restart_button.pack(pady=10)

    def update_display(self):
        dealer_cards = " ".join([card_to_str(card) for card in self.game.dealer.hand])
        self.dealer_label.config(text=f"Dealer's Hand: {dealer_cards}")
        human = self.game.players[0]
        player_cards = " ".join([card_to_str(card) for card in human.hand])
        self.player_label.config(text=f"Your Hand: {player_cards} (Total: {self.game.get_hand_value(human.hand)})")
        self.balance_label.config(text=f"Your Balance: {human.balance}")
        if self.enable_suggestion:
            state = self.game.get_state(human)
            suggestion = self.ai_agent.select_action(state)
            self.suggestion_label.config(text=f"AI Suggestion: {suggestion}")
        else:
            self.suggestion_label.config(text="")

    def hit(self):
        human = self.game.players[0]
        human.hand.append(self.game.deal_card())
        self.update_display()
        if self.game.get_hand_value(human.hand) > 21:
            messagebox.showinfo("Result", "You busted!")
            self.end_round()

    def stick(self):
        self.game.dealer_turn()
        human = self.game.players[0]
        results = self.game.settle_bets()
        result = results.get("Human", "lose")
        if result == "win":
            messagebox.showinfo("Result", "You win!")
        elif result == "draw":
            messagebox.showinfo("Result", "It's a draw!")
        else:
            messagebox.showinfo("Result", "You lose!")
        self.end_round()

    def start_new_round(self):
        human = self.game.players[0]
        # For simplicity, ask for bet amount via a dialog.
        bet = 10
        human.balance = max(human.balance, 100)
        self.game.place_bets(bet_amount=bet)
        self.game.deal_initial()
        self.update_display()

    def end_round(self):
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()
