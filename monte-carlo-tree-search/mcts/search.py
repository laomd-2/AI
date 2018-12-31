import numpy as np
import threading
from .node import TwoPlayersGameMonteCarloTreeSearchNode


def simulation(c):
    game_res = c.simulation()
    c.back_propagation(game_res)


class MonteCarloTreeSearch:
    def __init__(self, state: TwoPlayersGameMonteCarloTreeSearchNode):
        self.root = state

    def selection(self):
        node = self.root
        while node.children:
            node = np.random.choice(node.children)
        return node

    def search(self, play_round):
        for _ in range(play_round):
            # print('selection')
            leaf: TwoPlayersGameMonteCarloTreeSearchNode = self.selection()
            if leaf.state.is_game_over():
                leaf = self.root
            # print('expansion')
            children = leaf.expansion(4)
            # print('simulation')
            if len(children) == 1:
                simulation(children[0])
            else:
                threads = [threading.Thread(target=simulation, args=(c, )) for c in children]
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()
            # print('done')
        return self.root.best_child(1.414)
