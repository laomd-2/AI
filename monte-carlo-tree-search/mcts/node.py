import math
import random
import threading
import numpy as np
from games.common import TwoPlayersGameState


class TwoPlayersGameMonteCarloTreeSearchNode:

    def __init__(self, state: TwoPlayersGameState, action=None, parent=None):
        self.state = state
        self.action = action
        self.parent = parent
        self.children = []
        self.__lock = threading.Lock()
        self.win = self.visited = 0

    def simulation(self):
        state = self.state
        while not state.is_game_over():
            actions = state.get_legal_actions()
            if actions:
                action = np.random.choice(actions)
                state = state.move(action)
            else:
                state = state.pass_()
        return np.sign(state.game_result()) / 2 + 0.5

    def expansion(self, size=None):
        actions = self.state.get_legal_actions()
        if actions:
            if size is None:
                size = random.randint(1, len(actions))
            else:
                size = min(size, len(actions))
            for action in np.random.choice(actions, size):
                new_state = self.state.move(action)
                child = TwoPlayersGameMonteCarloTreeSearchNode(new_state, action, self)
                self.children.append(child)
            return self.children[-size:]
        else:
            action = None
            new_state = self.state.pass_()
            child = TwoPlayersGameMonteCarloTreeSearchNode(new_state, action, self)
            self.children.append(child)
            return [child]

    def back_propagation(self, result):
        with self.__lock:
            self.visited += 1
            self.win += result
        if self.parent:
            self.parent.back_propagation(1 - result)

    def best_child(self, c):
        score = [(child.win / child.visited + c * math.sqrt(math.log(self.visited) / child.visited))
                 for child in self.children]
        score = np.multiply(self.state.next_to_move, score)
        return self.children[np.argmax(score)]

