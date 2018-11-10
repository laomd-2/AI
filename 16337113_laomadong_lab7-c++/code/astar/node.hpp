//
// Created by laomd on 2018/11/9.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_SEARCH_H
#define INC_16337113_LAOMADONG_LAB7_C_SEARCH_H

#include <vector>
#include "../heuristic.h"
using namespace std;

template <typename Heuristic, int numbers>
class AstarNode {
    static int count;
    static Heuristic heuristic;
public:
    Puzzle<numbers> puzzle;
    int cost;
    int estimate_cost;
    int exchange = 0;
    const AstarNode* from;

    explicit AstarNode(const Puzzle<numbers>& puzzle1)
        : puzzle(puzzle1), from(nullptr),
          cost(0), estimate_cost(heuristic(puzzle)) {
        count++;
    }

    AstarNode(const AstarNode* other, int i, int j) : AstarNode(*other) {
        from = other;
        estimate_cost += heuristic(exchange, i, j, puzzle.space_i, puzzle.space_j, puzzle.size());
        exchange = puzzle.swap(i, j);
        cost++;

        count++;
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
