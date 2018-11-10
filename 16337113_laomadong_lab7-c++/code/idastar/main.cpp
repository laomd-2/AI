#include <ctime>
#include <iostream>
#include <fstream>
#include "idastar.hpp"
using namespace std;

int main(int argc, const char* argv[])
{
    const char* numbers = argv[1];
    Puzzle<numbers> puzzle;
    fstream fin(argv[2]);
    fin >> puzzle;
    vector<int> path;

    time_t start_time = time(NULL);
    int node_gen = idastar_search<Manhattan>(puzzle, path);
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