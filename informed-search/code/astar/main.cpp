#include <ctime>
#include <iostream>
#include <fstream>
#include "astar.hpp"
using namespace std;

int main(int argc, const char* argv[])
{
    Puzzle puzzle;
    fstream fin(argv[1]);
    fin >> puzzle;
    vector<int> path;

    clock_t start_time = clock();
    Manhattan h;
    astar_search(puzzle, &h, path);
    clock_t end_time = clock();

    cout << puzzle;
    cout << "Time Used: " << (double)(end_time - start_time) / CLOCKS_PER_SEC << " sec" << endl;
    cout << "An optional solution " << path.size() << " moves" << endl;
    for (auto it = path.rbegin(); it != path.rend(); ++it) {
        cout << *it << ' ';
    }
    cout << endl;
    return 0;
}