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

#ifndef __int64
#define __int64 long long
#endif

#define can_visit(visited, node, cost) (visited.find(node) == visited.end() \
    || visited[node] > (cost))


template <int numbers>
class Puzzle {
    __int64 _puzzle;
#define BITWISE 4
#define LOWERBIT 15
    int dim_size;
public:
    static Puzzle goal;
    int space_i, space_j;

    explicit Puzzle(__int64 puzzle = 0) : dim_size(sqrt(numbers + 1) + 0.5), _puzzle(puzzle) { }

    int get(int i, int j) const {
        i = (i * dim_size + j) * BITWISE;
        return (_puzzle >> i) & LOWERBIT;
    }

    void set(int i, int j, int x) {
        __int64 x64 = LOWERBIT;;
        int offset = (i * dim_size + j) * BITWISE;
        _puzzle &= ~(x64 << offset);
        x64 = x;
        _puzzle |= (x64 << offset);
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
            if (n_i >= 0 && n_j >= 0 && n_i < dim_size && n_j < dim_size) {
                neighbor[x] = make_pair(n_i, n_j);
            } else {
                neighbor[x] = make_pair(-1, -1);
            }
        }
    }

    int size() const {
        return dim_size;
    }

    bool operator<(const Puzzle& other) const {
        return _puzzle < other._puzzle;
    }

    bool operator==(const Puzzle& other) const {
        return _puzzle == other._puzzle;
    }

    friend istream& operator>>(istream& in, Puzzle& a) {
        int x;
        for (int i = 0; i < a.dim_size; ++i) {
            for (int j = 0; j < a.dim_size; ++j) {
                in >> x;
                a.set(i, j, x);
            }
        }
        return in;
    }

    friend ostream& operator<<(ostream& out, const Puzzle& a) {
        for (int i = 0; i < a.dim_size; ++i) {
            for (int j = 0; j < a.dim_size; ++j) {
                out << setw(2) << a.get(i, j) << ' ';
            }
            out << endl;
        }
        return out;
    }
};

template <>
Puzzle<15> Puzzle<15>::goal(0xFEDCBA987654321ULL);

template <>
Puzzle<8> Puzzle<8>::goal(0x087654321);
#endif //INC_16337113_LAOMADONG_LAB7_C_PUZZLE_H
