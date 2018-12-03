import pandas as pd


def read_maze(file, delimiter=','):
    maze = pd.read_table(file, header=None)
    maze = maze.applymap(lambda x: delimiter.join(list(x)))[0]\
        .str.split(delimiter, expand=True).values
    return maze