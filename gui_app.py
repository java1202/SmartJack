import tkinter as tk
from tkinter import messagebox, simpledialog
from blackjack_multi import BlackjackGameMulti, Player, categorize_balance
from agent import QLearningAgent

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
        master.title("SmartJack: AI-Powered Blackjack")
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

        self.round_over = False  # New flag to track if round is finished
        self.create_widgets()
        self.start_new_round()

    def create_widgets(self):
        self.dealer_label = tk.Label(self.master, text="Dealer's Hand: ", font=("Helvetica", 14))
        self.dealer_label.pack(pady=5)

        self.player_label = tk.Label(self.master, text="Your Hand: ", font=("Helvetica", 14))
        self.player_label.pack(pady=5)

        self.balance_label = tk.Label(self.master, text="Your Balance: ", font=("Helvetica", 12))
        self.balance_label.pack(pady=5)

        self.bet_label = tk.Label(self.master, text="Bet this round: ", font=("Helvetica", 12))
        self.bet_label.pack(pady=5)

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
        # Show only the dealer's visible (up) card if the round is still in progress.
        if not self.round_over:
            dealer_cards = card_to_str(self.game.dealer_visible)
        else:
            dealer_cards = " ".join([card_to_str(card) for card in self.game.dealer.hand])
        self.dealer_label.config(text=f"Dealer's Hand: {dealer_cards}")
        human = self.game.players[0]
        player_cards = " ".join([card_to_str(card) for card in human.hand])
        self.player_label.config(text=f"Your Hand: {player_cards} (Total: {self.game.get_hand_value(human.hand)})")
        self.balance_label.config(text=f"Your Balance: {human.balance} (Initial: {human.starting_balance})")
        self.bet_label.config(text=f"Your Bet This Round: {human.bet}")
        if self.enable_suggestion and not self.round_over:
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
        self.round_over = True  # Mark round as over so full dealer hand is shown
        human = self.game.players[0]
        dealer_total = self.game.get_hand_value(self.game.dealer.hand)
        dealer_cards = " ".join([card_to_str(card) for card in self.game.dealer.hand])
        results = self.game.settle_bets()
        result = results.get("Human", "lose")
        # Build a detailed result message showing the dealer's hand and total.
        result_text = f"Dealer's Hand: {dealer_cards} (Total: {dealer_total})\n"
        if result == "win":
            result_text += "You win!"
        elif result == "draw":
            result_text += "It's a draw!"
        else:
            result_text += "You lose!"
        messagebox.showinfo("Result", result_text)
        self.end_round()

    def start_new_round(self):
        human = self.game.players[0]
        self.round_over = False  # Reset the flag for a new round
        # Prompt for bet amount with a dialog (default 10, maximum equal to current balance).
        bet = 10
        bet_input = simpledialog.askinteger("Bet", f"Enter your bet amount (Current Balance: {human.balance}):",
                                              initialvalue=10, minvalue=1, maxvalue=human.balance)
        if bet_input is not None:
            bet = bet_input
        self.game.place_bets(bet_amount=bet)
        self.game.deal_initial()
        self.update_display()

    def end_round(self):
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()
