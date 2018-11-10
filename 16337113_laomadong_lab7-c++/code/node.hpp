//
// Created by laomd on 2018/11/9.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_SEARCH_H
#define INC_16337113_LAOMADONG_LAB7_C_SEARCH_H

#include <vector>
#include "heuristic.h"
using namespace std;

template <typename Heuristic, int numbers>
class AstarNode {
    int space_i, space_j;
    static int count;
    static Heuristic heuristic;
public:
    Puzzle<numbers> puzzle;
    int cost;
    int estimate_cost;
    int exchange = 0;
    const AstarNode* from;

    explicit AstarNode(const Puzzle<numbers>& puzzle1) : puzzle(puzzle1), from(nullptr) {
        cost = 0;
        estimate_cost = heuristic(puzzle);
        for (int i = 0; i < puzzle.size(); ++i) {
            for (int j = 0; j < puzzle.size(); ++j) {
                if (puzzle.get(i, j) == 0) {
                    space_i = i;
                    space_j = j;
                    break;
                }
            }
        }

        count++;
    }

    AstarNode(const AstarNode* other, int i, int j) : AstarNode(*other) {
        from = other;
        exchange = puzzle.get(i, j);
        puzzle.set(space_i, space_j, exchange);
        puzzle.set(i, j, 0);

        estimate_cost += heuristic(exchange, i, j, space_i, space_j, puzzle.size());
        space_i = i;
        space_j = j;
        cost++;
        count++;
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
            if (n_i >= 0 && n_j >= 0 && n_i < puzzle.size() && n_j < puzzle.size()) {
                auto *n = new AstarNode(this, n_i, n_j);
                neighbor.emplace_back(n);
            }
        }
        return neighbor;
    }

    static int nodes_gen() {
        return count;
    }
};

template <typename T, int numbers>
int AstarNode<T, numbers>::count = 0;

template <typename T, int numbers>
T AstarNode<T, numbers>::heuristic;
#endif //INC_16337113_LAOMADONG_LAB7_C_SEARCH_H
