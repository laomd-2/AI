//
// Created by laomd on 2018/11/10.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_ASTAR_H
#define INC_16337113_LAOMADONG_LAB7_C_ASTAR_H

#include <queue>
#include <map>
#include "search.h"
using namespace std;

#define can_visit(visited, node) (visited.find(node.puzzle) == visited.end() \
    || visited[node.puzzle] > node.cost)

int astar_search(const Puzzle& start, vector<int>& path) {
    Puzzle target = start;
    for (int i = 0; i < target.dim_size; ++i) {
        for (int j = 0; j < target.dim_size; ++j) {
            target.set(i, j, (i * target.dim_size + j + 1) % (target.dim_size * target.dim_size));
        }
    }

    auto pred = [](AstarNode* a, AstarNode* b) {
        return a->cost + a->estimate_cost >= b->cost + b->estimate_cost;
    };
    priority_queue<AstarNode*, vector<AstarNode*>, decltype(pred)> queue1(pred);
    auto* start_node = new AstarNode(start, 0, manhattan_distace(start));
    const AstarNode* target_node = nullptr;
    queue1.push(start_node);

    int cnt = 1;
    map<Puzzle, int> visited;
    map<const AstarNode*, const AstarNode*> path_parent;
    while (!queue1.empty()) {
        AstarNode* node = queue1.top();
        queue1.pop();
        if (can_visit(visited, (*node))) {
            path_parent[node] = node->from;
            if (node->puzzle == target) {
                target_node = node;
                break;
            }
            visited[node->puzzle] = node->cost;
            for (auto& n: node->neighbors()) {
                if (can_visit(visited, (*n))) {
                    queue1.push(n);
                    cnt++;
                }
            }
        }
    }

    while (target_node && target_node != start_node) {
        path.push_back(target_node->exchange);
        target_node = path_parent[target_node];
    }
    return cnt;
}

#endif //INC_16337113_LAOMADONG_LAB7_C_ASTAR_H
