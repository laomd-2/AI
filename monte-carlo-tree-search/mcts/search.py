from .node import Node


class MonteCarloTreeSearch:
    def __init__(self, state: Node):
        self.root = state

    @staticmethod
    def selection(node):
        while not node.state.is_game_over():
            if node.is_fully_expanded():
                node = node.best_child()
            else:
                return node.expansion()
        return None

    def search(self, play_round):
        for _ in range(play_round):
            # print(len(self.root.children))
            leaf: Node = self.selection(self.root)
            if leaf is None:
                break
            c = leaf.expansion()
            game_res = c.simulation()
            c.back_propagation(game_res)
        return self.root.best_child(c=0).action
