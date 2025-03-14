import pytest
from blackjack_multi import BlackjackGameMulti, Player

@pytest.fixture
def game():
    # Create a game with one dummy player.
    player = Player("Test_Player", balance=100, is_human=False)
    return BlackjackGameMulti(players=[player])

def test_deck_creation(game):
    deck = game.create_deck()
    # Expect 52 cards in a standard deck.
    assert len(deck) == 52

def test_hand_value_adjusts_ace(game):
    # Test a hand with an Ace that should adjust from 11 to 1.
    hand = [11, 10, 2]  # A, 10, 2: initially 23 but Ace becomes 1 to yield 13
    value = game.get_hand_value(hand)
    assert value == 13

def test_get_state_contains_risk(game):
    # Verify that get_state returns a tuple including the risk category.
    player = game.players[0]
    player.hand = [10, 5]
    state = game.get_state(player)
    # Expected structure: (player_total, dealer_visible, usable_ace, balance_category)
    assert len(state) == 4
    assert isinstance(state[3], str)
