import numpy as np
from fight_run_hide import FightRunHide
import matplotlib.pyplot as plt
import time

def smooth_data(data, window_size=5000):
  """
  Smooths data using a moving average filter.

  Args:
    data: The input data to be smoothed.
    window_size: The size of the moving average window.

  Returns:
    The smoothed data.
  """

  if len(data) < window_size:
    raise ValueError("Data length must be greater than window size")

  smoothed_data = np.convolve(data, np.ones(window_size) / window_size, mode='valid')
  return smoothed_data

def agent_policy(state, q_table):

    action_q_vals = q_table[state]
    action = np.argmax(action_q_vals)

    # 0.01 is our epsilon greedy
    if np.random.random() < epsilon:
        action = np.random.randint(0, 3)

    return action

def pretty_print(qtable):
    """Pretty print the Q-table with aligned rows and columns for HP states and actions."""
    # Define state labels based on HP
    state_labels = ["0 HP"] + [f"{5 * (i - 1)} < HP <= {5 * i}" for i in range(1, 31)]

    # Define action labels
    action_labels = ["Fight", "Run", "Hide"]

    # Determine column widths for alignment
    col_width = max(len(action) for action in action_labels) + 2  # Padding for actions
    state_width = max(len(state) for state in state_labels) + 2   # Padding for states
    value_width = max(len(f"{qval:.2f}") for qval in qtable.flatten()) + 2  # Q-value width

    # Print the header row
    header = " " * state_width + "".join(f"{action.center(value_width)}" for action in action_labels)
    print(header)

    # Print each row with state labels
    for state, q_values in zip(state_labels, qtable):
        row = f"{state.ljust(state_width)}" + "".join(f"{qval:>{value_width}.2f}" for qval in q_values)
        print(row)

if __name__ == "__main__":
    qtable = np.random.rand(31, 3)  # Example Q-table with 31 states and 3 actions

    # lets take a look at our Q-table
    pretty_print(qtable)

    env = FightRunHide(150, printing=False)
    state, _ = env.reset()

    # 3 actions, and first dim is states
    agent_q_table = np.zeros((int(env.maxhealth / 5 + 1), 3)) * 30

    print(agent_q_table)

    learning_rate = 0.1
    discount_rate = 0.99
    epsilon = 0.01

    score = 0
    scores = []
    games = 0
    best_score = 0

    while True:
        
        # choose our action using Epsilon Greedy
        action = agent_policy(state, agent_q_table)

        # step forward our environment
        next_state, reward, done, _ = env.step(action)

        # keep track of the score
        score += reward

        # update equation - this uses a learning rate
        # bootstrap value is a fancy term for the max value of the next state
        # for dones, its common to multiply the next state by (1 - done), ie if multiply by 0 if done is true

        #                                   Previous Value                                                  reward                      bootstrap value
        agent_q_table[state, action] = agent_q_table[state, action] * (1 - learning_rate) + learning_rate * (reward + discount_rate * (1 - done) * np.max(agent_q_table[next_state]))

        state = next_state

        if done:
            # reset the game
            state, _ = env.reset()
            if score > best_score:
                best_score  =score
            scores.append(score)
            games += 1

            # occasionally print out the Qtable
            if games % 10000 == 0:
                print(f"Previous Score {score}")
                print("Agent Q-Table:")
                pretty_print(agent_q_table)
                print(f"Best Score {best_score}")
                
            # occasionally plot the graph
            if games % 50000 == 0:

                smoothed_scores = smooth_data(np.array(scores))
                plt.plot(smoothed_scores)
                plt.xlabel("Episodes")
                plt.ylabel("Reward")

                plt.show()

            score = 0