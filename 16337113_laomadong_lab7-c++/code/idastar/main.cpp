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

    time_t start_time = time(NULL);
    idastar_search<Manhattan>(puzzle, path);
    time_t end_time = time(NULL);

    cout << "Time Used: " << end_time - start_time << " sec" << endl;
    cout << "An optional solution " << path.size() << " moves" << endl;
    for (auto it = path.rbegin(); it != path.rend(); ++it) {
        cout << *it << ' ';
    }
    cout << endl;
    return 0;
}