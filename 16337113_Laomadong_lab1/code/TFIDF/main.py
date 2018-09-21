from myio import get_tf_idf_documents
from IDF import IDF

if __name__ == '__main__':
    my_doc_list = get_tf_idf_documents()
    # my_doc_list = ["apple phone gooduse sale",
    #                "shimin buy phone phone",
    #                "shimin judge apple phone expensive gooduse"]
    idf = IDF(my_doc_list)
    words = idf.words

    with open("16337113_laomadong_TFIDF.txt", 'w') as result:
        for document in my_doc_list:
            tf_idf_doc = idf.get_tf_idf(document)
            for word in words:
                tfidf = 0
                if word in tf_idf_doc:
                    tfidf = tf_idf_doc[word]
                print("%g" % tfidf, end='\t', file=result)
            print(file=result)