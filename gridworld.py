import numpy as np
import time

class GridworldEnv:
    def __init__(self):
        # Define the grid with the correct orientation
        self.grid = np.array([
            ["S7", "S8", "S9", "end +1"],
            ["S5", "BLOCK", "S6", "end -1"],
            ["S0", "S1", "S2", "S3"]
        ])
        self.rewards = {
            "start": 0,
            "end +1": 1,
            "end -1": -1,
            "BLOCK": None  # Impassable state
        }
        self.terminal_states = {"end +1", "end -1"}
        self.agent_position = [2, 0]  # Start position at "start"
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]

    def reset(self):
        """Reset the environment to the initial state."""
        self.agent_position = [2, 0]  # Starting at "start"
        return str(self.grid[self.agent_position[0], self.agent_position[1]]), {}

    def step(self, action):
        """Take a step in the environment."""
        if action not in self.actions:
            raise ValueError(f"Invalid action: {action}")

        # Calculate new position based on action
        row, col = self.agent_position
        if action == "UP":
            row = max(0, row - 1)
        elif action == "DOWN":
            row = min(2, row + 1)
        elif action == "LEFT":
            col = max(0, col - 1)
        elif action == "RIGHT":
            col = min(3, col + 1)

        # Check if the move is valid
        new_state = self.grid[row, col]
        if new_state == "BLOCK":
            new_state = self.grid[self.agent_position[0], self.agent_position[1]]  # Stay in the same position
        else:
            self.agent_position = [row, col]

        # Get reward
        reward = self.rewards.get(new_state, 0)

        # Check if the state is terminal
        done = new_state in self.terminal_states

        return str(new_state), reward, done, {}

    def render(self):
        """Render the current state of the environment with aligned cells."""
        grid_render = self.grid.copy()
        row, col = self.agent_position
        grid_render[row, col] = " A "  # Mark the agent's position with padding for alignment

        # Determine the maximum width of any cell
        max_width = max(len(cell) for row in self.grid for cell in row)

        # Add padding to all cells for alignment
        padded_grid = np.array([[cell.center(max_width) for cell in row] for row in grid_render])

        # Print the formatted grid
        for row in padded_grid:
            print(" | ".join(row))
        print()


def create_q_table(tot_states, tot_actions):
    # creates a Q-table full of zeros with the shape we want
    return np.zeros((tot_states, tot_actions), dtype=float)

def state_to_idx(state):
    if state == "end +1":
        return 11
    elif state == "end -1":
        return 10
    else:
        # this just gets the string, removes the S and returns the number, ie S2 becomes 2
        return int(state[1:])

def action_to_idx(action):
    if action == "LEFT":
        return 0
    elif action == "RIGHT":
        return 1
    elif action == "UP":
        return 2
    elif action == "DOWN":
        return 3
    else:
        raise Exception("Invalid Action!")

def idx_to_action(action):
    if action == 0:
        return "LEFT"
    elif action == 1:
        return "RIGHT"
    elif action == 2:
        return "UP"
    elif action == 3:
        return "DOWN"
    else:
        raise Exception("Invalid Action!")

def choose_action(state, qtable):
    # we are going to choose our favourite action 90% of the time, and randomly choose one 10%

    if np.random.random() < 0.9:
        q_values = qtable[state]

        # choose the action with the highest value
        return np.argmax(q_values)
    else:
        # return random action
        return np.random.randint(0, 4)

def pretty_print(qtable):
    """Pretty print the Q-table with aligned rows and columns."""
    # Define state and action labels
    state_labels = [f"S{i}" for i in range(10)] + ["end -1", "end +1"]
    action_labels = ["LEFT", "RIGHT", "UP", "DOWN"]

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
    # practive code

    """
    # Example usage
    env = GridworldEnv()
    env.reset()
    env.render()

    # Take a few actions
    print(env.step("RIGHT"))  # Move to S1
    env.render()
    print(env.step("UP"))  # Move to S5
    env.render()
    print(env.step("RIGHT"))  # Move to BLOCK (invalid)
    env.render()
    print(env.step("RIGHT"))  # Move to S6
    env.render()
    print(env.step("UP"))  # Move to "end -1"
    env.render()
    print("Ending our practice code!")
    """

    # here we define our Q-table. Technically the two terminal states don't need to be in the Q-table,
    # but it makes code easier if you include them

    # 12 is S0 to S9 + 2 end states. 4 is number of actions
    qtable = create_q_table(tot_states=12, tot_actions=4)
    discount_rate = 0.8

    # have a look at our empty Q-table!
    pretty_print(qtable)

    # lets count how many episodes we're doing
    episodes = 0

    # you can also add env.render() down below to have a look whats going on

    # lets create our environment
    env = GridworldEnv()
    state, _ = env.reset()

    # convert our state to an idx for our table
    state = state_to_idx(state)

    while True:
        # we train forever!

        action = choose_action(state, qtable)

        next_state, reward, done, _ = env.step(idx_to_action(action))

        # convert our state to an idx for our table
        next_state = state_to_idx(next_state)

        # lets update our Q-table using the Q-Learning equation
        qtable[state, action] = reward + discount_rate * np.max(qtable[next_state])

        # move our state forward
        state = next_state

        if done:
            # remove this if you wanna go fast
            time.sleep(0.2)

            episodes += 1

            # if you wanna go fast, change this 1 to something much higher... or RIP your terminal
            if episodes % 1 == 0:
                pretty_print(qtable)

            state, _ = env.reset()
            # convert our state to an idx for our table
            state = state_to_idx(state)


