//
// Created by laomd on 2018/11/10.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_HEURISTIC_H
#define INC_16337113_LAOMADONG_LAB7_C_HEURISTIC_H

#include <cmath>
#include "puzzle.h"

class Manhattan {
    int distance(int x, int i, int j, int dim_size) const {
        int goal_i, goal_j;
        int d = 0;
        if (x != 0) {
            x -= 1;
            goal_i = x / dim_size;
            goal_j = x % dim_size;
            d = abs(i - goal_i) + abs(j - goal_j);
        }
        return d;
    }
public:
    int operator()(int x, int i, int j, int space_i, int space_j, int size) const {
        int sum = 0;
        sum -= distance(x, i, j, size);
        sum += distance(x, space_i, space_j, size);
        return sum;
    }

    template <int numbers>
    int operator()(const Puzzle<numbers>& puzzle) const {
        int x;
        int d = 0;
        int dim_size = puzzle.size();
        for (int i = 0; i < dim_size; ++i) {
            for (int j = 0; j < dim_size; ++j) {
                x = puzzle.get(i, j);
                d += distance(x, i, j, dim_size);
            }
        }
        return d;
    }
};

#endif //INC_16337113_LAOMADONG_LAB7_C_HEURISTIC_H
