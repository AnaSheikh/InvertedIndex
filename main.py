
import glob
import snowballstemmer as snowballstemmer
from bs4 import BeautifulSoup
import re

class Term(object):
    def __init__(self, id):
        self.id = id
        self.positions = {}


class document(object):
    def __init__(self, id):
        self.id = id
        self.terms = {}


terms = {}
termsid = {}
docs = {}
docsid = {}


def forward_index():
    stemmer = snowballstemmer.stemmer('english')
    files = 0
    f3 = open("D:\LastSemester\IR\PycharmProjects\docids.txt", 'w+', encoding='utf-8')
    f1 = open("D:\LastSemester\IR\PycharmProjects\\termids.txt", 'w+', encoding='utf-8')
    f2 = open("D:\LastSemester\IR\stoplist.txt", 'r', encoding='utf-8')
    f4 = open("D:\LastSemester\IR\PycharmProjects\doc_index.txt", 'w+', encoding='utf-8')
    present = False
    docid = 1
    termid = 1
    totalterms = 0
    stop_words = f2.read()
    f2.close()
    for path in glob.glob('D:\LastSemester\IR\corpus\*'):
        if path.endswith(".txt"):
            continue
        with open(path,'rb') as markup:                 # opening file in binary mode
            # Getting the document name from corpus and saving in file
            path1 = path.split("\\")
            docsid[path1[len(path1) - 1]] = str(docid)
            f3.write(str(docid))
            f3.write("\t")
            f3.write(path1[len(path1) - 1])
            f3.write("\n")
            docid = docid + 1

            id = docsid[path1[len(path1) - 1]]
            doc = document(id)
            position = 0

            soup = BeautifulSoup(markup.read(), "html.parser")
            para = soup.find_all('p')
            for p in para:
                text = p.text
                data = text.encode('utf-8')
                token_data =re.split("\\W+(\\.?\\W+)*", text)
                for tokens in token_data:
                    if tokens is None:
                        continue
                    elif stop_words.find(tokens) is -1:
                        tokens = tokens.lower()
                        word = stemmer.stemWord(str(tokens))
                    if stop_words.find(word) == -1:
                        # word is not in terms and updating the termsid.txt file
                        if str(word) not in termsid:
                            terms[str(termid)] = str(word)
                            termsid[str(word)] = str(termid)
                            f1.write(str(termid))
                            f1.write("\t")
                            f1.write(str(word))
                            f1.write("\n")
                            termid = termid + 1
                        # word doesn't exist in document terms
                        if str(word) not in doc.terms:
                            termm = Term(termsid[str(word)])
                            # assigning the whole Term object(termm) to terms of document object(doc)
                            doc.terms[str(word)] = termm
                            termm.positions[position] = str(position)
                        else:
                            present = False
                            doc.terms[str(word)].positions[position] = str(position)
                        position = position + 1
            # updating the doc_index with DOCID TERMID Positions
            for t in doc.terms:
                f4.write(doc.id)
                f4.write("\t")
                f4.write(doc.terms[t].id)
                for pos in doc.terms[t].positions:
                    totalterms += 1
                    #f4.write("\t")
                    #f4.write(doc.terms[t].positions[pos])
                f4.write("\t")
                f4.write(str(totalterms))
                f4.write("\n")
                totalterms = 0
            print(docid)
    f1.close()
    f3.close()
    f4.close()


if __name__ == '__main__':
    forward_index()
