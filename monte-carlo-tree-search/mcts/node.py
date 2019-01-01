import math
import numpy as np
from games.common import TwoPlayersGameState


class Node:

    def __init__(self, state: TwoPlayersGameState, action=None, parent=None):
        self.state = state
        self.action = action
        self.parent = parent
        self.__children = dict()
        self.__fully = False
        self.win = self.visited = 0

    def is_fully_expanded(self):
        return self.__fully

    def simulation(self):
        state = self.state
        while not state.is_game_over():
            actions = state.get_legal_actions()
            if actions:
                action = np.random.choice(actions)
                state = state.move(action)
            else:
                state = state.pass_()
        return (-self.state.next_to_move * np.sign(state.game_result())) / 2 + 0.5

    def expansion(self):
        actions = self.state.get_legal_actions()
        if actions:
            np.random.shuffle(actions)
            action = np.random.choice(actions)
            for action in actions:
                if action not in self.__children:
                    new_state = self.state.move(action)
                    self.__children[action] = Node(new_state, action, self)
                    break
            else:
                self.__fully = True
        else:
            self.__fully = True
            action = None
            if action in self.__children:
                return self.__children[action]
            new_state = self.state.pass_()
            self.__children[action] = Node(new_state, action, self)
        return self.__children[action]

    def back_propagation(self, result):
        self.visited += 1
        self.win += result
        if self.parent:
            self.parent.back_propagation(1 - result)

    @property
    def children(self):
        return list(self.__children.values())

    def best_child(self, c=1.414):
        score = [(child.win / child.visited + c * math.sqrt(math.log(self.visited) / child.visited))
                 for child in self.children]
        return self.children[np.argmax(score)]
