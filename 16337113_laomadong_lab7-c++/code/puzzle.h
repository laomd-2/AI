//
// Created by laomd on 2018/11/9.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_PUZZLE_H
#define INC_16337113_LAOMADONG_LAB7_C_PUZZLE_H

#include <istream>
#include <ostream>
#include <iomanip>
#include <cmath>
#include <vector>
using namespace std;

#define can_visit(visited, node, cost) (visited.find(node) == visited.end() \
    || visited[node] > (cost))

#define N 4
#define offset(i,j) (((i) * N + (j)) * 4)
#define LOWERBIT 15

class Puzzle {
    uint_fast64_t _puzzle;
public:
    static Puzzle goal;
    int space_i, space_j;

    explicit Puzzle(uint_fast64_t puzzle = 0) : _puzzle(puzzle) { }

    int get(int i, int j) const {
        i = offset(i, j);
        return (_puzzle >> i) & LOWERBIT;
    }

    void set(int i, int j, int x) {
        uint_fast64_t x64 = LOWERBIT;;
        int off = offset(i, j);
        _puzzle &= ~(x64 << off);
        x64 = x;
        _puzzle |= (x64 << off);
        if (x == 0) {
            space_i = i;
            space_j = j;
        }
    }

    int swap(int i, int j) {
        int exchange = get(i, j);
        set(space_i, space_j, exchange);
        set(i, j, 0);
        return exchange;
    }

    void neighbors(const int* dy, const int* dx, pair<int, int>* neighbor) const {
        int n_i, n_j;

        int i, j;
        for (int x = 0; x < 4; ++x) {
            i = dy[x];
            j = dx[x];
            n_i = space_i + i;
            n_j = space_j + j;
            if (n_i >= 0 && n_j >= 0 && n_i < N && n_j < N) {
                neighbor[x] = make_pair(n_i, n_j);
            } else {
                neighbor[x] = make_pair(-1, -1);
            }
        }
    }

    bool operator<(const Puzzle& other) const {
        return _puzzle < other._puzzle;
    }

    bool operator==(const Puzzle& other) const {
        return _puzzle == other._puzzle;
    }

    size_t hash() const {
//        int t, x, y;
//        int sum = 0;
//        for (int i = 0; i < N * N; ++i) {
//            t = 0;
//            x = puzzle.get(i / N, i % N), y;
//            for (int j = i + 1; j < N * N; ++j) {
//                y = puzzle.get(j / N, j % N);
//                if (x > y)
//                    t++;
//            }
//            sum += t * fact[N * N - i - 1];
//        }
//        return sum + 1;
        return std::hash<uint_fast64_t>()(_puzzle);
    }

    friend istream& operator>>(istream& in, Puzzle& a) {
        int x;
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                in >> x;
                a.set(i, j, x);
            }
        }
        return in;
    }

    friend ostream& operator<<(ostream& out, const Puzzle& a) {
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                out << setw(2) << a.get(i, j) << ' ';
            }
            out << endl;
        }
        return out;
    }
};

Puzzle Puzzle::goal(0x0FEDCBA987654321ULL);

namespace {
    const int fact[] = {1,1,2,6,24,120,720,5040,40320};  //i的阶乘为fac[i]
}

namespace std {
    template<>
    struct hash<Puzzle> {
        size_t operator()(const Puzzle &puzzle) const {
            return puzzle.hash();
        }
    };
}
#endif //INC_16337113_LAOMADONG_LAB7_C_PUZZLE_H