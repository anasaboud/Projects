import nltk
import sqlite3
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, ISRIStemmer
from nltk.tokenize import sent_tokenize , wordpunct_tokenize
from bs4 import BeautifulSoup
from flask import Request
import glob
import re
import os
import numpy as np
import sys
Stopwords = set(stopwords.words('arabic'))


#finding the unique words and the frequency of words

def finding_all_unique_words_and_freq(words):
    words_unique = []
    word_freq = {}
    for word in words:
        if word not in words_unique:
            words_unique.append(word)
    for word in words_unique:
        word_freq[word] = words.count(word)
    return word_freq


def finding_freq_of_word_in_doc(word, words):
    freq = words.count(word)


def remove_special_characters(text):
    regex = re.compile('[^a-zA-Z0-9\s]')
    text_returned = re.sub(regex, '', text)
    return text_returned


class Node:
    def __init__(self, docId, freq=None):
        self.freq = freq
        self.doc = docId
        self.nextval = None


class SlinkedList:
    def __init__(self, head=None):
        self.head = head


all_words = []
dict_global = {}
file_folder = 'doucments_arabic/*'
idx = 1
files_with_index = {}
for file in glob.glob(file_folder):
    print(file)
    fname = file
    
    file = open(file, "r")
    text = file.read()
    #text = remove_special_characters(text)
    #text = re.sub(re.compile('\d'), '', text)
    #sentences = sent_tokenize(text)
    words = wordpunct_tokenize(text)
    words = [word for word in words if len(words) > 1]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in Stopwords]
    dict_global.update(finding_all_unique_words_and_freq(words))
    files_with_index[idx] = os.path.basename(fname)
    idx = idx + 1

unique_words_all = set(dict_global.keys())

linked_list_data = {}
for word in unique_words_all:
    linked_list_data[word] = SlinkedList()
    linked_list_data[word].head = Node(1,Node)
word_freq_in_doc = {}
idx = 1
for file in glob.glob(file_folder):
    file = open(file, "r")
    text = file.read()
    #text = remove_special_characters(text)
    #text = re.sub(re.compile('\d'),'',text)
    #sentences = sent_tokenize(text)
    words = wordpunct_tokenize(text)
    words = [word for word in words if len(words)>1]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in Stopwords]
    word_freq_in_doc = finding_all_unique_words_and_freq(words)
    for word in word_freq_in_doc.keys():
        linked_list = linked_list_data[word].head
        while linked_list.nextval is not None:
            linked_list = linked_list.nextval
        linked_list.nextval = Node(idx ,word_freq_in_doc[word])
    idx = idx + 1
def srch(query):
    query = wordpunct_tokenize(query)
    connecting_words = []
    cnt = 1
    different_words = []
    for word in query:
        if word != "و" and word != "أو" and word != "ليس":
            different_words.append(word)
        else:
            connecting_words.append(word)
    print(connecting_words)
    total_files = len(files_with_index)
    zeroes_and_ones = []
    zeroes_and_ones_of_all_words = []
    for word in (different_words):
        if word in unique_words_all:
            zeroes_and_ones = [0] * total_files
            linkedlist = linked_list_data[word].head
            print(word)
            while linkedlist.nextval is not None:
                zeroes_and_ones[linkedlist.nextval.doc - 1] = 1
                linkedlist = linkedlist.nextval
            zeroes_and_ones_of_all_words.append(zeroes_and_ones)
        else:
            print(word, " not found")
            sys.exit()
    print(zeroes_and_ones_of_all_words)
    for word in connecting_words:
        word_list1 = zeroes_and_ones_of_all_words[0]
        word_list2 = zeroes_and_ones_of_all_words[1]
        if word == "و":
            bitwise_op = [w1 & w2 for (w1, w2) in zip(word_list1, word_list2)]
            zeroes_and_ones_of_all_words.remove(word_list1)
            zeroes_and_ones_of_all_words.remove(word_list2)
            zeroes_and_ones_of_all_words.insert(0, bitwise_op);
        elif word == "أو":
            bitwise_op = [w1 | w2 for (w1, w2) in zip(word_list1, word_list2)]
            zeroes_and_ones_of_all_words.remove(word_list1)
            zeroes_and_ones_of_all_words.remove(word_list2)
            zeroes_and_ones_of_all_words.insert(0, bitwise_op);
        elif word == "ليس":
            bitwise_op = [not w1 for w1 in word_list2]
            bitwise_op = [int(b == True) for b in bitwise_op]
            zeroes_and_ones_of_all_words.remove(word_list2)
            zeroes_and_ones_of_all_words.remove(word_list1)
            bitwise_op = [w1 & w2 for (w1, w2) in zip(word_list1, bitwise_op)]
    zeroes_and_ones_of_all_words.insert(0, bitwise_op);

    files = []
    print(zeroes_and_ones_of_all_words)
    lis = zeroes_and_ones_of_all_words[0]
    print(lis)
    cnt = 1
    for index in lis:
        if index == 1:
            files.append(files_with_index[cnt].rsplit(".",1)[0]) 
        cnt = cnt + 1
    print(files)
    
   
    return files

     