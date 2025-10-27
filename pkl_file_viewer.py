# view_q_table.py
import pickle
import numpy as np

# This makes the NumPy array print nicely
np.set_printoptions(precision=3, suppress=True)

def get_binary_from_state(state_index):
    """Converts a state index (0-31) into its 5-bit binary list representation."""
    # Example: state_index = 6 -> binary '110' -> padded '00110' -> reversed '01100' -> [0, 1, 1, 0, 0]
    return [int(bit) for bit in f'{state_index:05b}'[::-1]]

def view_table():
    """Loads and displays the Q-table, epsilon value, and binary states."""
    try:
        with open("q_table.pkl", "rb") as f:
            data = pickle.load(f)

        q_table = data['q_table']
        epsilon = data.get('epsilon', 'Not found')

        print("--- Q-Learning Agent Data ---")
        print(f"Epsilon (Current Curiosity Level): {epsilon:.4f}\n")
        print("--- Q-Table ---")
        print("State | Binary State    | Action:  LEFT    STRAIGHT    RIGHT")
        print("-----------------------------------------------------------------")

        for state_index, q_values in enumerate(q_table):
            binary_state = get_binary_from_state(state_index)
            binary_state_str = str(binary_state)
            
            # Print each row with aligned columns
            print(f"{state_index: >5} | {binary_state_str: <16}| [{q_values[0]: >7.3f} {q_values[1]: >7.3f} {q_values[2]: >7.3f} ]")

    except FileNotFoundError:
        print("Error: 'q_table.pkl' not found. Have you run the training script yet?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    view_table()