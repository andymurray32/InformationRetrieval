#!/usr/bin/python3
# 
import sys
import math
import sys
import re
import json

docids = []
doclength = {}
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
    in_d = open('docids2.txt', 'r')
    in_v = open('vocab2.txt', 'r')
    in_p = open('postings2.txt', 'r')
    in_c = open('doclength2.txt', 'r')

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
    
    for term in query_set:
        try:
            termid= vocab.index(term)
        except: ##if not in vocab
            print("term",term," is not in vocab")
            continue
        idf[termid]= math.log(len(doclength))/len(postings.get(str(termid))) ## log (number of docs/number containing word)
        
        print("TERM for retrieve_vector: ",term,"TERMID: ", termid, "IDF: ",idf[termid])
        #tf[termid]=postings.get(str(termid))
        
    i=-1
    
    for termid in sorted(idf,key=idf.get,reverse=True):
        print("POSTINGS",postings.get(str(termid)))
        i+=1
        #print("docid postings"),postings.get(str(wordid))
        for post in postings.get(str(termid)):
            print("POST: ",post)
            print("Docid= ",post.split(',')[0],"Frequency= ",post.split(',')[1],"idf= ",idf[termid]) ##post 0= docid post1= freq
            #print("doclemngth",doclength[postings.get(str(termid))
            #print("QUERY VECTOR",query_vector[i])
            #print("IDF SCORING",idf[termid])
            if post.split(',')[0] in scores: 
                #print("docid!!!!! ",docid)
                #print("wordid!!!!",termid)
               #print("postings docid wordid",postings[termid])
                scores[post.split(',')[0]]+=(idf[termid])*int(post.split(',')[1])/doclength.get(str(post.split(',')[0]))
                print("DOCLENGTH",doclength.get(str(post.split(',')[0])))
            else:
                scores[post.split(',')[0]]=(idf[termid])*int(post.split(',')[1])/doclength.get(str(post.split(',')[0]))
                print("DOCLENGTH",doclength.get(str(post.split(',')[0])))
                #if post[0] in scores:
            #    scores[post[0]]+=(idf[termid]*post[1])/doclength[(post[0])]*query_vector[i]
            #else:
            #    scores[post[0]]=(idf[termid]*post[1])/doclength[(post[0])]*query_vector[i]
    for docid in sorted(scores,key=scores.get,reverse=True):
        #print("retrieve vector(docid): ",docid,"score: ",scores.get(docid))
        answer.append([docid,scores[docid]])
        #answer.append([docids[docid],docid,,scores[docid]])

        #print("answers:", answer)
    return answer



    # Standard boilerplate to call the main() function
if __name__ == '__main__':
    main()
