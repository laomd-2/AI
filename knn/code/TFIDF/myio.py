def get_tf_idf_documents():
    my_doc_list = []
    with open("lab1_data/semeval.txt") as file:
        for line in file:
            line = line[line.rfind('\t') + 1: -1]
            if line:
                my_doc_list.append(line)
    return my_doc_list
