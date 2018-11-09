//
// Created by laomd on 2018/11/9.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_SEARCH_H
#define INC_16337113_LAOMADONG_LAB7_C_SEARCH_H

#include <vector>
#include <queue>
#include <map>
#include "puzzle.h"
using namespace std;

int distance(int x, int i, int j, int dim_size) {
    int target_i, target_j;
    int d = 0;
    if (x != 0) {
        x -= 1;
        target_i = x / dim_size;
        target_j = x % dim_size;
        d = abs(i - target_i) + abs(j - target_j);
    }
    return d;
}

int manhattan_distace(const Puzzle& puzzle) {
    int x;
    int d = 0;
    for (int i = 0; i < puzzle.dim_size; ++i) {
        for (int j = 0; j < puzzle.dim_size; ++j) {
            x = puzzle.get(i, j);
            d += distance(x, i, j, puzzle.dim_size);
        }
    }
    return d;
}

class AstarNode {
    int space_i, space_j;
public:
    Puzzle puzzle;
    int cost;
    int estimate_cost;
    int exchange = 0;
    const AstarNode* from;

    AstarNode(const Puzzle& puzzle1, int g, int h, AstarNode* p = nullptr) : puzzle(puzzle1), from(p) {
        cost = g;
        estimate_cost = h;
        for (int i = 0; i < puzzle.dim_size; ++i) {
            for (int j = 0; j < puzzle.dim_size; ++j) {
                if (puzzle.get(i, j) == 0) {
                    space_i = i;
                    space_j = j;
                    break;
                }
            }
        }
    }

    void swap(int i, int j) {
        exchange = puzzle.get(i, j);
        puzzle.set(space_i, space_j, exchange);
        puzzle.set(i, j, 0);

        estimate_cost -= distance(exchange, i, j, puzzle.dim_size);
        estimate_cost += distance(exchange, space_i, space_j, puzzle.dim_size);
        space_i = i;
        space_j = j;
        cost++;
    }

    vector<AstarNode*> neighbors() const {
        vector<AstarNode*> neighbor;
        int n_i, n_j;
        int dx[] = {0, 0, 1, -1};
        int dy[] = {-1, 1, 0, 0};

        int i, j;
        for (int x = 0; x < 4; ++x) {
            i = dx[x];
            j = dy[x];
            n_i = space_i + i;
            n_j = space_j + j;
            if (n_i >= 0 && n_j >= 0 && n_i < puzzle.dim_size && n_j < puzzle.dim_size) {
                auto *n = new AstarNode(*this);
                n->from = this;
                n->swap(n_i, n_j);
                neighbor.emplace_back(n);
            }
        }
        return neighbor;
    }
};

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

#endif //INC_16337113_LAOMADONG_LAB7_C_SEARCH_H
