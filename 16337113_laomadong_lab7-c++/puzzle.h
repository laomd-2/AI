//
// Created by laomd on 2018/11/9.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_PUZZLE_H
#define INC_16337113_LAOMADONG_LAB7_C_PUZZLE_H

#include <istream>
#include <ostream>
#include <iomanip>
#include <cmath>
using namespace std;

class Puzzle {
    __int64 _puzzle;
#define BITWISE 4
#define LOWERBIT 15
public:
    int dim_size = 4;

    Puzzle(int numbers) : dim_size(sqrt(numbers + 1) + 0.5), _puzzle(0) { }

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

#endif //INC_16337113_LAOMADONG_LAB7_C_PUZZLE_H