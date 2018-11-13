#include <ctime>
#include <iostream>
#include <fstream>
#include "../heuristic.h"
#include "idastar.hpp"
using namespace std;

int main(int argc, const char* argv[])
{
    Puzzle<15> puzzle;
    fstream fin(argv[1]);
    fin >> puzzle;
    cout << puzzle;

    vector<int> path;

    clock_t start_time = clock();
    ManhattanWithLC<15> h;
    idastar_search(puzzle, &h, path);
    clock_t end_time = clock();

    cout << "Time Used: " << (double)(end_time - start_time) / CLOCKS_PER_SEC << " sec" << endl;
    cout << "An optional solution " << path.size() << " moves" << endl;
    for (auto it = path.rbegin(); it != path.rend(); ++it) {
        cout << *it << ' ';
    }
    cout << endl;
    return 0;
}