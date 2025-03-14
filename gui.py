import matplotlib.pyplot as plt
import numpy as np

def plot_training_rewards(rewards):
    """
    Plot raw rewards over training episodes.
    This often looks like a dense block when there are many episodes.
    """
    plt.figure()
    plt.plot(rewards)
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.title("Training Rewards Over Episodes (Raw)")
    plt.show()

def plot_training_rewards_moving_average(rewards, window_size=1000):
    """
    Plot a rolling average (moving average) of the rewards to get a smoother curve.
    :param rewards: A list of episode rewards (e.g., -1, 0, 1).
    :param window_size: Number of episodes to average over.
    """
    # Convert to numpy array for convenience
    rewards_arr = np.array(rewards, dtype=float)

    # Compute cumulative sum
    cumsum = np.cumsum(rewards_arr)
    # For indices >= window_size, subtract the cumulative sum from earlier
    cumsum[window_size:] = cumsum[window_size:] - cumsum[:-window_size]
    # The rolling average is the difference divided by window_size
    moving_avg = cumsum[window_size - 1:] / window_size

    # Plot
    plt.figure()
    plt.plot(range(window_size - 1, len(rewards)), moving_avg, label="Moving Avg")
    plt.xlabel("Episode")
    plt.ylabel("Average Reward")
    plt.title(f"Training Rewards (Rolling Average, window={window_size})")
    plt.legend()
    plt.show()
