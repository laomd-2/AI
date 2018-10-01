def validate(tree, validation_X, y):
    cnt = 0
    total = 0
    res = tree.predict(validation_X)
    for x, yy, y in zip(validation_X, res, y):
        print(x, yy, y)
        if y == yy:
            cnt += 1
        total += 1
    return cnt / total
