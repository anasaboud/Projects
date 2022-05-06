import operator                    #Importing the required libraries
import glob
import re
import math
import nltk
nltk.download('punkt')             # Remove pound sign if punkt package is not insallted on the machine
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, ISRIStemmer
import VSM_Preprocessing_arabic as p



def vsearch(query):
    
    query_line= query
    query_data=dict()
    count=1
    k= p.preprocess(query_line)
    query_data.update({1:k})

    qindex=dict()                       # This is used to calculate tf for each word in a document
    for key,value in query_data.items():
        for each in value:
            if each not in qindex:
                qindex.update({each:{key : 1}})
            else:
                if key not in qindex[each]:
                    qindex[each].update({key : 1})
                else:
                    qindex[each][key]=qindex[each][key]+1

    qidf=dict()                         # This is used to calculate the IDF for each word in queries w.r.t. documents.
    for key,value in qindex.items():
        id=math.log(10/(len(value)+1),10)
        qidf.update({key: id})

    q_tfidf=dict()                      #Following is used to calculate the TFIDF value for rach word in each document(TF*IDF).
    for key,value in qindex.items():
        for key1,value1 in value.items():
                if key1 not in q_tfidf:
                    q_tfidf.update({key1:{key:qidf[key]*value1}})
                else:
                    q_tfidf[key1].update({key:qidf[key]*value1})

    qdoc_len=dict()                     #Following is used to calculate the document length for each query.
    for key, value in q_tfidf.items():
        s=0
        for key1, value1 in value.items():
            s= s + pow(value1,2)
        qdoc_len.update({key: s}) 

    
    folder = glob.glob('doucments_arabic/*')
    data=dict()                         #Following is used to take data as input ans tokenize it.
    for file_list in folder:
        file_open=open(file_list,'r')
        file_read=file_open.read()
        k=p.preprocess(file_read)
        x=file_list[-13:]
        data.update({x: k})

    index=dict()                        #Following is used to calculate TF value for rach word in each document.
    for key,value in data.items():
        for each in value:
            if each not in index:
                index.update({each:{key : 1}})
            else:
                if key not in index[each]:
                    index[each].update({key : 1})
                else:
                    index[each][key]=index[each][key]+1

    idf=dict()                          #Here we calculate the IDF for rach document.
    for key,value in index.items():
        id=math.log(1400/(len(value)+1),10)
        idf.update({key: id})

    tfidf=dict()                        #Here we calculate the TFIDF for each word in each document.
    for key,value in index.items():
        for key1,value1 in value.items():
                if key1 not in tfidf:
                    tfidf.update({key1:{key:idf[key]*value1}})
                else:
                    tfidf[key1].update({key:idf[key]*value1})

    doc_len=dict()                      #This will calculate the leach of each document that helps in finding the cosine similarity.
    for key, value in tfidf.items():
        s=0
        for key1, value1 in value.items():
            s= s + pow(value1,2)
        doc_len.update({key: s})  

    relevant = dict()                   #Here we find out all the relevant documents to the specified queries.
    for key1,value1 in query_data.items():
        inter=dict()
        for key,value in data.items():
            common=[]
            for each in value1:
                if each in value:
                    common.append(each)
            inter.update({key:common})
        relevant.update({key1 : inter})

    cosine=dict()                       #Cosine similarity is calculated for each query w.r.t. each document.
    num=dict()
    for key, value in relevant.items():
        for key1, value1 in value.items():
            xf=0.0
            den=0.0
            for each in value1:
                a=q_tfidf[key][each]
                b=tfidf[key1][each]
                xf=xf+(a*b)
            den=math.sqrt(doc_len[key1]*qdoc_len[key])
            final_cosine=xf/den
            if key not in num:
                num.update({key : {key1 : final_cosine}})
            else:
                num[key].update({key1: final_cosine})

    sorted_val=dict()                   #Used to sort the documents in the descending order of their cosine similarity.
    for key, value in num.items():
        sorted_x = sorted(value.items(), key=operator.itemgetter(1), reverse=True)
        sorted_val.update({key: sorted_x})
    print("This is the output of query and relevant documents in descending order")
    output_list=[]
    for key, value in sorted_val.items():
        for i in range(0,len(value)):
            output_list.append(list(map(int, re.findall(r'\d+', value[i][0]))))
    numbers=[]
    for i in output_list:
        for w in i:
            numbers.append(w)
        

    print(numbers)
    return (numbers)

