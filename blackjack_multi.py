import random
from typing import List, Tuple, Any

def categorize_balance(balance: int) -> str:
    """Categorize balance into 'low', 'medium', or 'high' risk appetite."""
    if balance < 50:
        return "low"
    elif balance < 150:
        return "medium"
    else:
        return "high"

class Player:
    def __init__(self, name: str, balance: int, is_human: bool = False) -> None:
        self.name = name
        self.balance = balance
        self.starting_balance = balance  # store initial balance for reference
        self.is_human = is_human
        self.hand: List[int] = []
        self.bet = 0

    def reset_hand(self) -> None:
        self.hand = []

class BlackjackGameMulti:
    def __init__(self, players: List[Player]) -> None:
        """
        Initialize a multi-player blackjack game.
        :param players: List of Player objects (e.g., one human and one AI player).
        """
        self.players = players
        self.dealer = Player("Dealer", balance=0)
        self.deck = self.create_deck()
        random.shuffle(self.deck)
        self.dealer_visible: int = 0

    def create_deck(self) -> List[int]:
        deck = []
        for _ in range(4):  # four suits
            for card in range(2, 11):
                deck.append(card)
            # Face cards count as 10; Ace as 11 (usable as 1 when needed)
            deck.extend([10, 10, 10, 11])
        return deck

    def deal_card(self) -> int:
        if len(self.deck) == 0:
            self.deck = self.create_deck()
            random.shuffle(self.deck)
        return self.deck.pop()

    def place_bets(self, bet_amount: int = 10) -> None:
        """Each player places a bet. The bet amount is subtracted from their balance.
           If the player's balance is lower than the bet, they bet whatever they have."""
        for player in self.players:
            if player.balance >= bet_amount:
                player.bet = bet_amount
                player.balance -= bet_amount
            else:
                player.bet = player.balance
                player.balance = 0

    def deal_initial(self) -> None:
        """Reset hands and deal two cards to each player and the dealer."""
        for player in self.players:
            player.reset_hand()
        self.dealer.reset_hand()
        for player in self.players:
            player.hand = [self.deal_card(), self.deal_card()]
        self.dealer.hand = [self.deal_card(), self.deal_card()]
        self.dealer_visible = self.dealer.hand[0]

    def get_hand_value(self, hand: List[int]) -> int:
        total = sum(hand)
        aces = hand.count(11)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def has_usable_ace(self, hand: List[int]) -> bool:
        return 11 in hand and self.get_hand_value(hand) <= 21

    def get_state(self, player: Player) -> Tuple[Any, ...]:
        """
        Returns a tuple representing the player's state for RL:
          - Player's hand total
          - Dealer's visible card
          - Whether the player has a usable Ace
          - Player’s risk category (based on remaining balance)
          - Bet fraction (current bet relative to starting balance)
        """
        total = self.get_hand_value(player.hand)
        usable = self.has_usable_ace(player.hand)
        risk_category = categorize_balance(player.balance)
        bet_fraction = player.bet / player.starting_balance if player.starting_balance > 0 else 0
        return (total, self.dealer_visible, usable, risk_category, bet_fraction)

    def player_turn(self, player: Player, agent: Any = None) -> None:
        """Process a single player’s turn with detailed descriptors."""
        while True:
            state = self.get_state(player)
            if player.is_human:
                if agent is not None:
                    suggestion = agent.select_action(state)
                    print(f"AI Suggestion: {suggestion}")
                print(f"{player.name} -- Starting Balance: {player.starting_balance}, Current Balance: {player.balance}, Bet this round: {player.bet}")
                action = input(
                    f"Your hand: {player.hand} (total: {self.get_hand_value(player.hand)}), Dealer shows: {self.dealer_visible}. Hit or stick? "
                ).strip().lower()
                if action not in ["hit", "stick"]:
                    print("Invalid action. Please choose 'hit' or 'stick'.")
                    continue
            else:
                action = agent.select_action(state) if agent else "stick"
                print(f"{player.name} (AI) selects: {action}")
            if action == "hit":
                player.hand.append(self.deal_card())
                hand_val = self.get_hand_value(player.hand)
                print(f"{player.name} now has {player.hand} (total: {hand_val})")
                if hand_val > 21:
                    print(f"{player.name} busts!")
                    break
            elif action == "stick":
                break
            else:
                print("Unknown action, please try again.")

    def dealer_turn(self) -> None:
        """Dealer draws cards until reaching a total of at least 17."""
        while self.get_hand_value(self.dealer.hand) < 17:
            self.dealer.hand.append(self.deal_card())
        print(f"Dealer's hand: {self.dealer.hand} (total: {self.get_hand_value(self.dealer.hand)})")

    def settle_bets(self) -> dict:
        """Compare each player's hand to the dealer and update balances accordingly."""
        dealer_total = self.get_hand_value(self.dealer.hand)
        results = {}
        for player in self.players:
            player_total = self.get_hand_value(player.hand)
            if player_total > 21:
                result = "lose"
            elif dealer_total > 21 or player_total > dealer_total:
                result = "win"
                player.balance += 2 * player.bet
            elif player_total == dealer_total:
                result = "draw"
                player.balance += player.bet
            else:
                result = "lose"
            results[player.name] = result
        return results
