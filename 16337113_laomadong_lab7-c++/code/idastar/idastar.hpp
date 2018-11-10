//
// Created by laomd on 2018/11/10.
//

#ifndef INC_16337113_LAOMADONG_LAB7_C_IDASTAR_HPP
#define INC_16337113_LAOMADONG_LAB7_C_IDASTAR_HPP

#include <map>
#include <algorithm>
#include <vector>
#include "../puzzle.h"
using namespace std;

template <typename Heuristic, int numbers>
bool dfs(Puzzle<numbers>& node, int cost,
        int limit, int prev_dir,
        const Heuristic& h, vector<int>& path) {
    static const int dy[4] = {0, 0, +1, -1};
    static const int dx[4] = {+1, -1, 0, 0};

    int estimate = h(node);
    if (node == node.goal) return true;
    if (cost + estimate > limit) {
        return false;
    } else {
        int space_i = node.space_i, space_j = node.space_j;
        int exchange;

        pair<int, int> neighbors[4];
        node.neighbors(dy, dx, neighbors);
        for (int i = 0; i < 4; i++)
        {
            if (i == (prev_dir ^ 1))  // 小三爷，不回头
                continue;

            int ny = neighbors[i].first;
            int nx = neighbors[i].second;

            if (nx > -1 && ny > -1) {
                exchange = node.swap(ny, nx);
                path.push_back(exchange);
                if (dfs(node, cost + 1,
                        limit, i, h, path))
                    return true;
                path.pop_back();
                node.swap(space_i, space_j);
            }
        }
        return false;
    }
}

template <typename Heuristic, int numbers>
void idastar_search(Puzzle<numbers>& start, vector<int>& path) {
    Heuristic h;
    int lower_bound = h(start);
    for (; lower_bound < 70; ++lower_bound) {
        if (dfs<Heuristic, numbers>(start, 0,
                lower_bound, -1, h, path)) {
            break;
        }
    }
    reverse(path.begin(), path.end());
}
#endif //INC_16337113_LAOMADONG_LAB7_C_IDASTAR_HPP
