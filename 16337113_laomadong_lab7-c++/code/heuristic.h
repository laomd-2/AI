//
// Created by laomd on 2018/11/10.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_HEURISTIC_H
#define INC_16337113_LAOMADONG_LAB7_C_HEURISTIC_H

#include <cmath>
#include "puzzle.h"

class Heuristic {
public:
    pair<int, int> goal_pos(int x) const {
        x -= 1;
        return make_pair(x / N, x % N);
    }

    virtual int abs_distance(const Puzzle& b, int i, int j) const = 0;
    virtual int relative_distance(Puzzle& b, int i, int j) const {
        int d = this->operator()(b);
        b.swap(i, j);
        return this->operator()(b) - d;
    }

    int operator()(const Puzzle& puzzle) const {
        int d = 0;
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                d += abs_distance(puzzle, i, j);
            }
        }
        return d;
    }
};

class Manhattan : public Heuristic {
public:
    virtual int abs_distance(const Puzzle& b, int i, int j) const {
        int x = b.get(i, j);

        int d = 0;
        if (x != 0) {
            auto goal = this->goal_pos(x);
            d = abs(i - goal.first) + abs(j - goal.second);
        }
        return d;
    }

    virtual int relative_distance(Puzzle& b, int i, int j) const {
        int space_i = b.space_i, space_j = b.space_j;
        int d = abs_distance(b, i, j);
        b.swap(i, j);
        return abs_distance(b, space_i, space_j) - d;
    }
};

class ManhattanWithLC : public Manhattan {
    int linear_conflict(const Puzzle& b, int i, int j) const {
        int x, y;
        x = b.get(i, j);
        int count = 0;
        if (x != 0) {
            auto goal = Heuristic::goal_pos(x);
            if (goal.second == j) {
                for (int k = i + 1; k < N; ++k) {
                    y = b.get(k, j);
                    if (y == 0)
                        continue;
                    int goal_j = Heuristic::goal_pos(y).second;

                    if (goal_j == j) {
                        if (y < x && (x - y) % N == 0) {
                            ++count;
                        }
                    }
                }
            }
            if (goal.first == i) {
                for (int k = j + 1; k < N; ++k) {
                    y = b.get(i, k);
                    if (y == 0)
                        continue;
                    int goal_i = Heuristic::goal_pos(y).first;
                    if (goal_i == i) {
                        if (y < x && (x - y) < N) {
                            ++count;
                        }
                    }
                }
            }
        }
        return 2 * count;
    }
public:
    virtual int abs_distance(const Puzzle& b, int i, int j) const {
        int d = Manhattan::abs_distance(b, i, j);
        return d + linear_conflict(b, i, j);
    }

    virtual int relative_distance(Puzzle& b, int i, int j) const {
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

        auto goal = this->goal_pos(exchange);
        d -= abs(i - goal.first) + abs(j - goal.second);
        d += abs(space_i - goal.first) + abs(space_j - goal.second);
        return d;
    }
};

#endif //INC_16337113_LAOMADONG_LAB7_C_HEURISTIC_H
