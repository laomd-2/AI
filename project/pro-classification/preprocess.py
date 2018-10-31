import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
from replacers import RegexReplacer


def SplitPhase(row):
    """ split paragraph to sentence """
    PunktTokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
    return PunktTokenizer.tokenize(row['review'])

def RemoveHTML(row):
    """ remove HTML tags """
    rc = re.compile(r"\<.*?\>")  
    return [rc.sub('',sentence) for sentence in row['review']]

def ReplaceAbbre(row):
    """ Replace abbreviation """
    replacer = RegexReplacer()
    return [replacer.replace(sentence) for sentence in row['review']]

def SplitSent(row):
    """ split sentence to words """
    pattern = r'[\d.,]+|[A-Z][.A-Z]+\b\.*|\w+|\S'
    tokenizer = RegexpTokenizer(pattern)
    return [tokenizer.tokenize(sentence) for sentence in row['review']]

def CleanWords(row):
    res = []
    stops = set(stopwords.words("english"))
    for sentence in row['review']:
        res.append([])
        for word in sentence:
            if len(word) >= 3 and word.isalpha() and word not in stops:
                res[-1].append(word.lower())
    return res

def ToStr(row):
    str=""
    for sentence in row['review']:
        for word in sentence:
            str += (word + " ")
    return str[:-1]