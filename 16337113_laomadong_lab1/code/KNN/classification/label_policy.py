from collections import Counter


def classification_label_policy(k_neighbors):
    label = None
    cur_max = 0
    counter = Counter()
    while k_neighbors:
        the_label = k_neighbors.get()[1]
        counter[the_label] += 1
        if counter[the_label] > cur_max:
            cur_max = counter[the_label]
            label = the_label
    return label
