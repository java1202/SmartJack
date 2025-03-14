import matplotlib.pyplot as plt

def plot_training_rewards(rewards):
    """
    Plot rewards over training episodes.
    """
    plt.figure()
    plt.plot(rewards)
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.title("Training Rewards Over Episodes")
    plt.show()
