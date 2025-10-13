import numpy as np
import random
import pickle
import os

class QLearningController:
    def __init__(self, n_states=32, n_actions=3, filename="q_table.pkl"):
        self.n_states = n_states
        self.n_actions = n_actions
        self.lr = 0.6        # learning rate α
        self.gamma = 0.8     # discount factor γ
        self.epsilon = 0.2   # exploration probability ε
        self.filename = filename
        self.q_table = np.zeros((n_states, n_actions))
        self.action_list = [0, 1, 2]  # 0 = LEFT, 1 = STRAIGHT, 2 = RIGHT

    # ---------------------
    # Convert sensors to state
    # ---------------------
    def Get_state(self, sensor_data):
        try:
            values = [float(sensor_data[key]) for key in ['left_corner', 'left', 'middle', 'right', 'right_corner']]
        except Exception as e:
            print("[ERROR] Invalid sensor data:", sensor_data)
            return 0

        # Threshold: 1 = black line, 0 = white
        binary_vals = [1 if v < 0.5 else 0 for v in values]

        # Convert to single integer
        state = 0
        for i, val in enumerate(binary_vals):
            state |= (val << i)
        return state

    # ---------------------
    # Reward function
    # ---------------------
    def Calculate_reward(self, sensor_data):
        if sensor_data == [0,0,1,0,0]:
            return 5
        elif sensor_data in ([0,1,1,0,0], [0,0,1,1,0]):
            return 2
        elif sum(sensor_data) > 0:
            return 1
        else:
            return -10


    def update_q_table(self, state, action, reward, next_state):
        a_idx = self.action_list.index(action)
        current_q = self.q_table[state][a_idx]
        max_future_q = np.max(self.q_table[next_state])
        new_q = current_q + self.lr * (reward + self.gamma * max_future_q - current_q)
        self.q_table[state][a_idx] = new_q


    def choose_action(self, state):
        if random.uniform(0,1) < self.epsilon:
            return random.choice(self.action_list)
        else:
            best_action_idx = np.argmax(self.q_table[state])
            return self.action_list[best_action_idx]


    def perform_action(self, action):
        base_speed = 2.0
        turn_speed = 1.0
        if action == 0:
            return turn_speed, base_speed
        elif action == 1:
            return base_speed, base_speed
        elif action == 2:
            return base_speed, turn_speed
        else:
            return 0,0


    def save_q_table(self):
        with open(self.filename,'wb') as f:
            pickle.dump({
                'q_table': self.q_table,
                'epsilon': self.epsilon,
                'n_action': self.n_actions,
                'n_states': self.n_states
            }, f)
        print("[QLEARN] Q-table saved.")

    def load_q_table(self):
        if os.path.exists(self.filename):
            with open(self.filename,'rb') as f:
                data = pickle.load(f)
            self.q_table = data.get('q_table', self.q_table)
            self.epsilon = data.get('epsilon', self.epsilon)
            self.n_actions = data.get('n_action', self.n_actions)
            self.n_states = data.get('n_states', self.n_states)
            # Fix shape mismatch
            if self.q_table.shape != (self.n_states, self.n_actions):
                self.q_table = np.zeros((self.n_states, self.n_actions))
            print(" Q-table loaded from file.")
            return True
        print(" No saved Q-table found. Starting fresh.")

        return False
