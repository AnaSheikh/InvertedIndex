from collections import OrderedDict


class Term(object):
    def __init__(self,id):
        self.id=id
        self.docs={}
class documents(object):
    def __init__(self,id):
        self.id=id
        self.positions={}

def inverted_index():
    f=open("D:\LastSemester\IR\PycharmProjects\docindex.txt",'r', encoding='utf-8')
    f1=open("D:\LastSemester\IR\PycharmProjects\\termindex.txt",'w', encoding='utf-8')
    f2=open("D:\LastSemester\IR\PycharmProjects\\term_info.txt",'w',encoding='utf-8')
    terms={}
    data=f.read()
    f.close()
    data1= data.split("\n")
    writing_count=0
    # this loop read the line and then add term and its respective document line by line and set all the positions in
    # that document
    for line in range(0,len(data1)-1,1):
        docid=-1
        index=-1
        termid=-1
        index1=-1
        index2=-1
        # getting the docids when \t comes the previous number is docid
        for i in range(0,len(data1[line]),1):
            if data1[line][i] == "\t":
                docid=int(data1[line][0:i])
                index=i
                break
        #getting the termids by checking when \t comes and the next number is term
        for i in range(index+1,len(data1[line]),1):
            if data1[line][i] == "\t":
                termid=int(data1[line][index+1:i])
                index1=i
                break
        index2=index1+1
        # if term is not in terms
        if termid not in terms:
            terms[termid]=Term(termid)
        #if docid is not listed
        if docid not in terms[termid].docs:
            terms[termid].docs[docid] = documents(docid)
        #getting all the positions for specific term in a single document id
        for i in range(index1+1,len(data1[line]),1):
            if data1[line][i] == "\t":
                terms[termid].docs[docid].positions[int(data1[line][index2:i])]=(int(data1[line][index2:i]))
                index2=i+1
            if data1[line][i] == "\n":
                terms[termid].docs[docid].positions[int(data1[line][index2:i])]=(int(data1[line][index2:i]))
                break
            if i == len(data1[line])-1:
                terms[termid].docs[docid].positions[int(data1[line][index2:])]=(int(data1[line][index2:]))
                break

    for t in terms:
        print (terms[t].id)
        no_of_documents=0
        no_of_terms=0
        no_of_terms_in_document = 0
        new_doc_new_pos=True
        new_doc=False
        temp_docid=-1
        temp_pos=-1
        temp = dict(OrderedDict(sorted(terms[t].docs.items())))
        terms[t].docs = temp
        for pos in terms[t].docs:
            temp = dict(OrderedDict(sorted(terms[t].docs[pos].positions.items())))
            terms[t].docs[pos].positions = temp
        f2.write(str(terms[t].id))
        f2.write("\t")
        f2.write(str(f1.tell()))
        f2.write("\t")
        f1.write(str(terms[t].id))
        f1.write("\t")
        writing_count=writing_count+len(str(terms[t].id))+1
        for d in terms[t].docs:
            no_of_documents=no_of_documents+1
            f1.write(str(terms[t].docs[d].id))
            f1.write(":")
            for p in terms[t].docs[d].positions:
                no_of_terms_in_document = no_of_terms_in_document + 1
                no_of_terms=no_of_terms+1
            f1.write(str(no_of_terms_in_document))
            f1.write("\t")
            no_of_terms_in_document = 0
        f1.write("\n")
        writing_count=writing_count+1
        f2.write(str(no_of_terms))
        f2.write("\t")
        f2.write(str(no_of_documents))
        f2.write("\n")
        terms[t].docs.clear()
    f1.close()
    f2.close()


