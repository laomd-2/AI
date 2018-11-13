//
// Created by laomd on 2018/11/10.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_HEURISTIC_H
#define INC_16337113_LAOMADONG_LAB7_C_HEURISTIC_H

#include <cmath>
#include "puzzle.h"

template <int numbers>
class Heuristic {
public:
    pair<int, int> goal_pos(int x, int dim_size) const {
        x -= 1;
        return make_pair(x / dim_size, x % dim_size);
    }

    virtual int abs_distance(const Puzzle<numbers>& b, int i, int j) const = 0;
    virtual int relative_distance(Puzzle<numbers>& b, int i, int j) const {
        int d = this->operator()(b);
        b.swap(i, j);
        return this->operator()(b) - d;
    }

    int operator()(const Puzzle<numbers>& puzzle) const {
        int d = 0;
        int dim_size = puzzle.size();
        for (int i = 0; i < dim_size; ++i) {
            for (int j = 0; j < dim_size; ++j) {
                d += abs_distance(puzzle, i, j);
            }
        }
        return d;
    }
};

template <int numbers>
class Manhattan : public Heuristic<numbers> {
public:
    virtual int abs_distance(const Puzzle<numbers>& b, int i, int j) const {
        int n = b.size();
        int x = b.get(i, j);

        int d = 0;
        if (x != 0) {
            auto goal = this->goal_pos(x, n);
            d = abs(i - goal.first) + abs(j - goal.second);
        }
        return d;
    }

    virtual int relative_distance(Puzzle<numbers>& b, int i, int j) const {
        int space_i = b.space_i, space_j = b.space_j;
        int d = abs_distance(b, i, j);
        b.swap(i, j);
        return abs_distance(b, space_i, space_j) - d;
    }
};

template <int numbers>
class ManhattanWithLC : public Manhattan<numbers> {
    int linear_conflict(const Puzzle<numbers>& b, int i, int j) const {
        int n = b.size();
        int x, y;
        x = b.get(i, j);
        int count = 0;
        if (x != 0) {
            auto goal = Heuristic<numbers>::goal_pos(x, n);
            if (goal.second == j) {
                for (int k = i + 1; k < n; ++k) {
                    y = b.get(k, j);
                    if (y == 0)
                        continue;
                    int goal_j = Heuristic<numbers>::goal_pos(y, n).second;

                    if (goal_j == j) {
                        if (y < x && (x - y) % n == 0) {
                            ++count;
                        }
                    }
                }
            }
            if (goal.first == i) {
                for (int k = j + 1; k < n; ++k) {
                    y = b.get(i, k);
                    if (y == 0)
                        continue;
                    int goal_i = Heuristic<numbers>::goal_pos(y, n).first;
                    if (goal_i == i) {
                        if (y < x && (x - y) < n) {
                            ++count;
                        }
                    }
                }
            }
        }
        return 2 * count;
    }
public:
    virtual int abs_distance(const Puzzle<numbers>& b, int i, int j) const {
        int d = Manhattan<numbers>::abs_distance(b, i, j);
        return d + linear_conflict(b, i, j);
    }

    virtual int relative_distance(Puzzle<numbers>& b, int i, int j) const {
        int space_i = b.space_i, space_j = b.space_j;
        int d = 0;
        int exchange;

        if (i == space_i) {
            for (int k = 0; k < i + 1; ++k) {
                d -= linear_conflict(b, k, j) + linear_conflict(b, k, space_j);
            }
            for (int k = 0; k < j && k < space_j; ++k) {
                d -= linear_conflict(b, i, k);
            }
            exchange = b.swap(i, j);
            for (int k = 0; k < i + 1; ++k) {
                d += linear_conflict(b, k, j) + linear_conflict(b, k, space_j);
            }
            for (int k = 0; k < j && k < space_j; ++k) {
                d += linear_conflict(b, i, k);
            }
        } else {
            for (int k = 0; k < j + 1; ++k) {
                d -= linear_conflict(b, i, k) + linear_conflict(b, space_i, k);
            }
            for (int k = 0; k < i && k < space_i; ++k) {
                d -= linear_conflict(b, k, j);
            }
            exchange = b.swap(i, j);
            for (int k = 0; k < j + 1; ++k) {
                d += linear_conflict(b, i, k) + linear_conflict(b, space_i, k);
            }
            for (int k = 0; k < i && k < space_i; ++k) {
                d += linear_conflict(b, k, j);
            }
        }

        auto goal = this->goal_pos(exchange, b.size());
        d -= abs(i - goal.first) + abs(j - goal.second);
        d += abs(space_i - goal.first) + abs(space_j - goal.second);
        return d;
    }
};

#endif //INC_16337113_LAOMADONG_LAB7_C_HEURISTIC_H
