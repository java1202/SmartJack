import pickle
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict

def load_q_table(filename: str = "q_table.pkl") -> Tuple[Dict, int]:
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
        return data["Q"], data.get("episodes", 0)
    except Exception as e:
        print("Error loading Q table:", e)
        return {}, 0

def chart_probabilities() -> None:
    q_table, episodes = load_q_table()
    if not q_table:
        print("No Q table available for analysis.")
        return

    risk_categories = ["low", "medium", "high"]
    usable_options = [True, False]
    player_totals = list(range(4, 22))  # 4 to 21 inclusive
    dealer_cards = list(range(2, 12))   # 2 to 11 (11 represents Ace)
    # Use a fixed bet fraction for analysis; e.g., 0.5 means betting 50% of starting balance.
    fixed_bet_fraction = 0.5

    # Create a subplot grid: rows for risk categories, columns for usable ace True/False.
    fig, axes = plt.subplots(len(risk_categories), len(usable_options), figsize=(12, 12), squeeze=False)
    for i, risk in enumerate(risk_categories):
        for j, usable in enumerate(usable_options):
            grid = np.zeros((len(player_totals), len(dealer_cards)))
            suggestion_grid = np.empty((len(player_totals), len(dealer_cards)), dtype=object)
            for y, player_total in enumerate(player_totals):
                for x, dealer in enumerate(dealer_cards):
                    state = (player_total, dealer, usable, risk, fixed_bet_fraction)
                    q_hit = q_table.get(state, {}).get("hit", 0.0)
                    q_stick = q_table.get(state, {}).get("stick", 0.0)
                    best_action = "hit" if q_hit >= q_stick else "stick"
                    best_value = max(q_hit, q_stick)
                    # Convert expected reward to an approximate win probability in [0, 1].
                    p_win = (best_value + 1) / 2
                    grid[y, x] = np.clip(p_win, 0, 1)
                    suggestion_grid[y, x] = "H" if best_action == "hit" else "S"
            ax = axes[i][j]
            im = ax.imshow(grid, cmap='viridis', origin='lower', aspect='auto', vmin=0, vmax=1)
            ax.set_xticks(range(len(dealer_cards)))
            ax.set_xticklabels(dealer_cards)
            ax.set_yticks(range(len(player_totals)))
            ax.set_yticklabels(player_totals)
            ax.set_xlabel("Dealer's Visible Card")
            ax.set_ylabel("Player's Total")
            title = f"Risk: {risk}, Usable Ace: {usable}\nBet Fraction: {fixed_bet_fraction}"
            ax.set_title(title)
            # Annotate each cell with the AI suggestion and probability value.
            for y in range(len(player_totals)):
                for x in range(len(dealer_cards)):
                    text = f"{suggestion_grid[y, x]}\n{grid[y, x]:.2f}"
                    ax.text(x, y, text, ha='center', va='center', color='white', fontsize=8)
    fig.suptitle("AI Estimated Win Probabilities and Suggested Actions\n(Approx. win probability computed as (expected reward + 1)/2)")
    fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.6)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    chart_probabilities()
