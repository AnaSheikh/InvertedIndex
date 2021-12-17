import snowballstemmer as snowballstemmer
from Tools.scripts.treesync import raw_input


class document(object):
    def __init__(self,id,distinct_words,total_words):
        self.id=id
        self.distinct_words=distinct_words
        self.total_words=total_words

class Termmm(object):
    def __init__(self, id, offset, no_of_words, no_of_documents):
        self.id=id
        self.offset=offset
        self.no_of_words=no_of_words
        self.no_of_documents=no_of_documents
docs={}
terms={}
termids={}
docids={}
f=open("D:\LastSemester\IR\PycharmProjects\\term_index.txt",'r', encoding='utf-8')
f1=open("D:\LastSemester\IR\PycharmProjects\docindex.txt",'r', encoding='utf-8')
f2=open("D:\LastSemester\IR\PycharmProjects\\termids.txt",'r', encoding='utf-8')
f3=open("D:\LastSemester\IR\PycharmProjects\docids.txt",'r', encoding='utf-8')
f4=open("D:\LastSemester\IR\PycharmProjects\\term_index.txt",'r', encoding='utf-8')
f5=open("D:\LastSemester\IR\PycharmProjects\\term_info.txt",'r', encoding='utf-8')
data=f1.read()
data1=data.split("\n")
for line in data1:
    data2=line.split("\t")
    if data2[0] not in docs:
        docs[data2[0]]=document(data2[0],0,0)
    docs[data2[0]].distinct_words = docs[data2[0]].distinct_words + 1
    for i in range(2,len(data2),1):
        docs[data2[0]].total_words = docs[data2[0]].total_words + 1

data=f2.read()
data1=data.split("\n")
for line in data1:
    data2=line.split("\t")
    if(len(data2)!=1):
        termids[data2[1]]=data2[0]

data=f3.read()
data1=data.split("\n")
for line in data1:
    data2=line.split("\t")
    if(len(data2)!=1):
        docids[data2[1]]=data2[0]

data=f5.read()
data1=data.split("\n")
for line in data1:
    data2=line.split("\t")
    if len(data2)==4:
        terms[data2[0]] = Termmm(data2[0],data2[1],data2[2],data2[3])

flag_term=False
flag_document=True
term=""
document=""
while 1:
    command=raw_input("Enter command:")
    #command="term wish doc clueweb12-0000wb-51-02043"
    input_words=command.split(" ")
    if len(input_words) == 4:
        for i in input_words:
            if i =="term":
                flag_term=True
            elif flag_term ==True:
                term=i
                flag_term=False
            elif i=="doc":
                flag_document=True
            elif flag_document==True:
                document=i
                flag_document=False
        stemmer = snowballstemmer.stemmer('english')
        term=term.lower()
        word = stemmer.stemWord(term)
        word = word.rstrip("\n")
        document = document.rstrip("\n")
        print ("Inverted list for term: "+ term)
        print ("In document: "+document)
        print ("Termid: "+termids[word])
        print ("Docid: "+docids[document])
        frequency=0
        pos=[]
        temp_doc=0
        ind=-1
        ind1=-1
        f4.seek(int(terms[termids[word]].offset))
        data=f4.readline()
        data1=data.split('\t')
        for i in range(1,len(data1),1):
            if data1[i]=="\n":
                break
            for j in range(0,len(data1[i]),1):
                if data1[i][j]==':':
                    ind=j
                    break
            temp_doc = temp_doc + int(data1[i][0:ind])
            if temp_doc==int(docids[document]):
                frequency+=1
                pos.append(int(data1[i][ind+1:]))
        print ("Term frequency in document:"+str(frequency))
        if len(pos)==0:
            print("Term does not exist in document")
        else:
            print ("Positions:")
            print(pos[0])
            for p in range(1,len(pos)):
                print(pos[p] + pos[p - 1])
    if len(input_words)==2:
        stemmer = snowballstemmer.stemmer('english')
        if input_words[0]=="term":
            word = stemmer.stemWord(input_words[1])
            word = word.rstrip("\n")
            print("Listing for term: " + str(word))
            print("Termid: " + termids.get(str(word)))
            print("Number of documents contaning term: " + str(terms[str(termids.get(word))].no_of_documents))
            print("Term frequency in corpus: " + str(terms[str(termids.get(word))].no_of_words))
            print("Inverted list offset: " + terms[str(termids.get(word))].offset)
        if input_words[0]=="doc":
            word = stemmer.stemWord(input_words[1])
            word = word.rstrip("\n")
            print("Listing for document: " + word)
            print("Docid: " + docids.get(str(word)))
            print("Distinct terms: " + str(docs[docids.get(str(word))].distinct_words))
            print("Total terms: " + str(docs[docids.get(str(word))].total_words))
