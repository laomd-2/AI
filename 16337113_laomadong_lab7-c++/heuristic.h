//
// Created by laomd on 2018/11/10.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_HEURISTIC_H
#define INC_16337113_LAOMADONG_LAB7_C_HEURISTIC_H

#include <cmath>
#include "puzzle.h"

class Manhattan {
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
public:
    int operator()(int x, int i, int j, int space_i, int space_j, int size) {
        int sum = 0;
        sum -= distance(x, i, j, size);
        sum += distance(x, space_i, space_j, size);
        return sum;
    }
    int operator()(const Puzzle& puzzle) {
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
};

#endif //INC_16337113_LAOMADONG_LAB7_C_HEURISTIC_H
