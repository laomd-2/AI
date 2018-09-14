from myio import get_tf_idf_documents
from TFIDF import get_tf_idf


if __name__ == '__main__':
    my_doc_list = get_tf_idf_documents()
    # my_doc_list = ["apple phone gooduse sale",
    #                "shimin buy phone phone",
    #                "shimin judge apple phone expensive gooduse"]
    words, TF, IDF = get_tf_idf(my_doc_list)

    with open("../../result/16337113_laomadong_TFIDF.txt", 'w') as result:
        for row in TF:
            for i in range(len(IDF)):
                print("%g" % (row[i] * IDF[i]), end='\t', file=result)
            print(file=result)
