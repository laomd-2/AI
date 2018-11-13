//
// Created by laomd on 2018/11/10.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_ASTAR_H
#define INC_16337113_LAOMADONG_LAB7_C_ASTAR_H

#include <queue>
//#include <map>
#include <unordered_map>
#include <algorithm>
#include "node.hpp"
#include "../heuristic.h"
using namespace std;

void astar_search(const Puzzle& start, Heuristic* h, vector<int>& path) {
    typedef AstarNode node_type;

    auto pred = [](node_type* a, node_type* b) {
        return a->cost + a->estimate_cost >= b->cost + b->estimate_cost;
    };
    priority_queue<node_type*, vector<node_type*>, decltype(pred)> open_set(pred);

//    map<Puzzle, int> visited;
    unordered_map<Puzzle, int> visited;
    unordered_map<const node_type*, const node_type*> path_parent;
    int dy[] = {0, 0, 1, -1};
    int dx[] = {-1, 1, 0, 0};
    pair<int, int> neighbors[4];

    const node_type* target_node = nullptr;
    auto* start_node = new node_type(start, h);
    open_set.push(start_node);
    while (!open_set.empty()) {
        node_type* node = open_set.top();
        open_set.pop();
        if (can_visit(visited, node->puzzle, node->cost)) {
            path_parent[node] = node->from;
            if (node->puzzle == node->puzzle.goal) {
                target_node = node;
                break;
            }
            visited[node->puzzle] = node->cost;
            node->puzzle.neighbors(dy, dx, neighbors);
            for (auto &neighbor : neighbors) {
                int ny = neighbor.first;
                int nx = neighbor.second;
                if (nx > -1 && ny > -1) {
                    auto *n = new node_type(node, ny, nx);
                    if (can_visit(visited, n->puzzle, n->cost))
                        open_set.push(n);
                    else
                        delete n;
                }
            }
        }
    }

    while (target_node && target_node != start_node) {
        path.push_back(target_node->exchange);
        target_node = path_parent[target_node];
    }
}

#endif //INC_16337113_LAOMADONG_LAB7_C_ASTAR_H
