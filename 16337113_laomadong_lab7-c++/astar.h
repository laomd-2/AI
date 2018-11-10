//
// Created by laomd on 2018/11/10.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_ASTAR_H
#define INC_16337113_LAOMADONG_LAB7_C_ASTAR_H

#include <queue>
#include <map>
#include "node.h"
using namespace std;

#define can_visit(visited, node) (visited.find(node.puzzle) == visited.end() \
    || visited[node.puzzle] > node.cost)

int astar_search(const Puzzle& start, vector<int>& path) {
    typedef AstarNode<Manhattan> node_type;
    Puzzle target = start;
    for (int i = 0; i < target.dim_size; ++i) {
        for (int j = 0; j < target.dim_size; ++j) {
            target.set(i, j, (i * target.dim_size + j + 1) % (target.dim_size * target.dim_size));
        }
    }

    auto pred = [](node_type* a, node_type* b) {
        return a->cost + a->estimate_cost >= b->cost + b->estimate_cost;
    };
    priority_queue<node_type*, vector<node_type*>, decltype(pred)> queue1(pred);
    auto* start_node = new node_type(start);
    const node_type* target_node = nullptr;
    queue1.push(start_node);

    map<Puzzle, int> visited;
    map<const node_type*, const node_type*> path_parent;
    while (!queue1.empty()) {
        node_type* node = queue1.top();
        queue1.pop();
        if (can_visit(visited, (*node))) {
            path_parent[node] = node->from;
            if (node->puzzle == target) {
                target_node = node;
                break;
            }
            visited[node->puzzle] = node->cost;
            for (auto& n: node->neighbors()) {
                if (can_visit(visited, (*n)))
                    queue1.push(n);
            }
        }
    }

    while (target_node && target_node != start_node) {
        path.push_back(target_node->exchange);
        target_node = path_parent[target_node];
    }
    return node_type::nodes_gen();
}

#endif //INC_16337113_LAOMADONG_LAB7_C_ASTAR_H
