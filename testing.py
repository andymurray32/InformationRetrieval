#!/usr/bin/python3
# 
import sys
import math
import sys
import re
import json

docids = []
doclength = []
vocab = []
postings = {}

def main():
    # code for testing offline	
    if len(sys.argv) < 2:
        print ('usage: ./retriever.py term [term ...]')
        sys.exit(1)
    query_terms = sys.argv[1:]
    answer = []
    read_index_files()

    answer = retrieve_vector(query_terms)

    print ('Query: ', query_terms)
    i = -1
    for docid in answer:
        i += 1
        print (i, answer[i])

def read_index_files():
    ## reads existing data from index files: docids, vocab, postings
    # uses JSON to preserve list/dictionary data structures
    # declare refs to global variables
    global docids
    global postings
    global vocab
    global doclength
    # open the files
    in_d = open('docids1.txt', 'r')
    in_v = open('vocab1.txt', 'r')
    in_p = open('postings1.txt', 'r')
    in_c = open('doclength1.txt', 'r')

    # load the data
    docids = json.load(in_d)
    vocab = json.load(in_v)
    postings = json.load(in_p)
    doclength=json.load(in_c)
    # close the files
    in_d.close()
    in_v.close()
    in_p.close()
    in_c.close()
    
    return
    
def retrieve_vector(query_terms):
    ## a function to perform vector model retrieval with tf*idf weighting
    #
    global docids       # list of doc names - the index is the docid (i.e. 0-4)
    global doclength    # number of terms in each document
    global vocab        # list of terms found (237) - the index is the termid
    global postings # postings dictionary; the key is a termid
                        # the value is a list of postings entries, 
                        # each of which is a list containing a docid and frequency

    answer= []
    merge_list= []
    idf= {}
    scores= {}
    query_vector =[]
    
    query_set= set(query_terms) ##removes duplicates
    
    ##print("vocab= ", vocab)
    print("postings:", postings) ##testingggggggg
    ##print("doclength:", doclength) ##testingggggggg
    ##print("docids", docids)
    print("doclength 6: ",doclength[5])
    print("doclenth length", len(doclength))
    x= len(doclength)
    print("X IS",x)
    for term in query_set:
        try:
            wordid= vocab.index(term.lower())
        except: ##if not in vocab
            print("term",term," is not in vocab")
            continue
        print("postings for wordid:  ",postings.get(wordid))
        idf[wordid]= math.log(x)/len(postings.get(wordid)) ## log (number of docs/number containing word)
        print("TERM for retrieve_vector: ",term,"WORDID: ", wordid, "IDF: ",idf[wordid])
    i=-1
    
    for wordid in sorted(idf,key=idf.get,reverse=True):
        print("POSTINGS",postings.get(wordid))
        i+=1
        query_vector.append(idf[wordid])
        for post in postings.get(wordid):
            print("Docid= ",post[0],"Frequency= ",post[1],"idf= ",idf.get(wordid), "doclength= ",doclength.get(post[0])) ##post 0= docid post1= freq
            if post[0] in scores:
                scores[post[0]]+=(idf.get(wordid)*post[1])/doclength.get(post[0])*query_vector[i]
            else:
                scores[post[0]]=(idf.get(wordid)*post[1])/doclength.get(post[0])*query_vector[i]
            #print((idf.get(termid)*post[1])/doclength.get(post[0]))
            
    for docid in sorted(scores,key=scores.get,reverse=True):
        #print("retrieve vector(docid): ",docid,"score: ",scores.get(docid))
        answer.append([docids[docid],docid,scores.get(docid)])
    
    print("answers:", answer)
    return answer



    # Standard boilerplate to call the main() function
if __name__ == '__main__':
    main()
