#include <ctime>
#include <iostream>
#include <fstream>
#include "puzzle.h"
#include "search.h"
using namespace std;

int main(int argc, const char* argv[])
{
    Puzzle puzzle(atoi(argv[1]));
    fstream fin(argv[2]);
    fin >> puzzle;
    vector<int> path;

    time_t start_time = time(NULL);
    int node_gen = astar_search(puzzle, path);
    time_t end_time = time(NULL);

    cout << puzzle;
    cout << "Time Used: " << end_time - start_time << " sec" << endl;
    cout << "Number of nodes generated: " << node_gen << endl;
    cout << "An optional solution " << path.size() << " moves" << endl;
    for (auto it = path.rbegin(); it != path.rend(); ++it) {
        cout << *it << ' ';
    }
    cout << endl;
    return 0;
}