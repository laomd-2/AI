//
// Created by laomd on 2018/11/9.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_SEARCH_H
#define INC_16337113_LAOMADONG_LAB7_C_SEARCH_H

#include <vector>
#include "../heuristic.h"
using namespace std;

class AstarNode {
    Heuristic* heuristic;
public:
    Puzzle puzzle;
    int cost;
    int estimate_cost;
    int exchange = 0;
    const AstarNode* from;

    explicit AstarNode(const Puzzle& puzzle1, Heuristic* h)
        : puzzle(puzzle1), from(nullptr), heuristic(h),
          cost(0), estimate_cost((*heuristic)(puzzle)) {
    }

    AstarNode(const AstarNode* other, int i, int j) : AstarNode(*other) {
        from = other;
        exchange = puzzle.get(i, j);
        estimate_cost += heuristic->relative_distance(puzzle, i, j);
        cost++;
    }
};

#endif //INC_16337113_LAOMADONG_LAB7_C_SEARCH_H
