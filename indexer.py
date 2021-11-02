#!/usr/bin/python3
'''
===================================================================================================================================================
Project:Information Retrieval- Crawl and Index
Author:Andrew Murray
Student number:100214063
===================================================================================================================================================
'''
#!/usr/bin/python3	indexer.py -d ./LookingGlass 5

import sys
import os
import re
import json
import math
#from UEAlite import stem_doc # added Oct 2015 DJS
from bs4 import BeautifulSoup


# global declarations for docids, lengths, postings, vocabulary
docids = []
doclength = {}
postings = {}
vocab = []


def main():
    # code for testing offline
    max_files = 32000;
    if len(sys.argv) == 1:
        print ('usage: ./indexer.py file | -d directory [maxfiles]')
        sys.exit(1)
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 3:
        if re.match('-d', sys.argv[1]):
            dirname = sys.argv[2]
            dir_index = True
        else:
            print ('usage: ./indexer.py file | -d directory [maxfiles]')
            sys.exit(1)
    elif len(sys.argv) == 4:
        if re.match('\d+', sys.argv[3]):
            max_files = int(sys.argv[3])
        else:
            print ('usage: ./indexer.py file | -d directory [maxfiles]')
            sys.exit(1)
    else:
        print ('usage: ./indexer.py file | -d directory [maxfiles]')

    if len(sys.argv) == 2:
        index_file(filename)
    elif re.match('-d', sys.argv[1]):
        for filename in os.listdir(sys.argv[2]):
            if re.match('^_', filename):
                continue
            if max_files > 0:
                max_files -= 1
                filename = sys.argv[2]+'/'+filename
                index_file(filename)
            else:
                break
                
    write_index_files(1)
            
def index_file(filename):           
        try:
            input_file = open(filename, 'rb')
        except (IOError) as ex:
            print('Cannot open ', filename, '\n Error: ', ex)
        else:
            page_contents = input_file.read() # read the input file
            url = 'http://www.'+filename+'/'
            print (url, page_contents)
            make_index(url, page_contents)   
            input_file.close()
                
def write_files(n):
# 
    # n can be 0,1
    # declare refs to global variables
    global docids
    global postings
    global vocab
    global doclength
    # decide which files to open
    # there are 2 sets, written to on alternate calls
    if (n):
        nn = 1
    else:
        nn = 2
    # open files
    out_d = open('docids'+str(nn)+'.txt', 'w')
    out_l = open('doclength'+str(nn)+'.txt', 'w')
    out_v = open('vocab'+str(nn)+'.txt', 'w')
    out_p = open('postings'+str(nn)+'.txt', 'w')
    # write to index files: docids, vocab, postings
    # use JSON as it preserves the dictionary structure (read/write treat it as a string)
    json.dump(docids, out_d)
    json.dump(doclength, out_l)
    json.dump(vocab, out_v)
    json.dump(postings, out_p)
    # close files
    out_d.close()
    out_l.close()
    out_v.close()
    out_p.close()
    
    d = len(docids)
    v = len(vocab)
    p = len(postings)
    print ('===============================================')
    print ('Indexing: ', d, ' docs ', v, ' terms ', p, ' postings lists written to file')
    print ('===============================================')
    
    return
def read_index_files():

    # declare refs to global variables
    global docids
    global postings
    global vocab
    global doclength

    # reads existing data into index files: docids, lengths, vocab, postings
    in_d = open('docids'+str(nn)+'.txt', 'r') 
    in_l = open('doclength'+str(nn)+'.txt', 'r')
    in_v = open('vocab.txt'+str(nn)+'', 'r')
    in_p = open('postings'+str(nn)+'.txt', 'r')
    
    docids = json.load(in_d)
    doclength = json.load(in_l)
    vocab = json.load(in_v)
    postings = json.load(in_p)

    in_d.close()
    in_l.close()
    in_v.close()
    in_p.close()
    
    return
        
def clean_html(html):

    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"\t", " ", cleaned) 
    cleaned = re.sub(r"[ ]+", " ", cleaned) 
    # and blank lines 
    cleaned = re.sub(r"[ ]*\n", "\n", cleaned)
    cleaned = re.sub(r"\n+", "\n", cleaned)
    cleaned=re.sub(r"[^\w\s]", " ",cleaned)
    #cleaned=html
    return cleaned.strip()


def make_index(url, page_contents):
    # declare refs to global variables
    global docids
    global postings
    global vocab
    global doclength
    
    #extract the words from the page contents
    
    if (isinstance(page_contents, bytes)): # convert bytes to string if necessary
        page_contents = page_contents.decode('utf-8', 'ignore')
    terms = clean_html(page_contents)
    print ('===============================================')
    print ('make_index: url = ', url)
######################################## FOR CONTENT TESTING:
    #print ('make_index1: page_text = ', page_text) # for testing

###Handle different protocol
    if (re.search('https:..', url)):# match and remove https://
        domain_url = re.sub('https://', '', url)
    elif (re.search('http:..', url)):# match and remove http://
        domain_url = re.sub('http://', '', url)
    else:
        print ("make_index: no match for protocol url=", url)
    if (re.search('www.', domain_url)):	# match and remove www.
        domain_url = re.sub('www.', '', domain_url)

### append the url to the list of documents
    if (domain_url in docids): # return if we've seen this before
        return
    else:
        docids.append(domain_url)# add url to docids table
        docid = str(docids.index(domain_url))# creates an index for each docid

#### stemming and other processing goes here #####
### split text to words:
    termlist = terms.split()
    doclength[docid] = len(termlist)
### end of stemming and other processing   #####
###################################################
    terms = re.sub("(\w+)n't", "\1 not", page_contents)		# replace n't with not
    terms = re.sub(r"-", r" ", terms)						# remove hyphen
    terms = re.sub(r"(\w)'s", r"\1", terms)					# remove apostrophes
    terms = re.sub(r'&\w+;', '', terms)
    terms = re.sub(r'[,.;:()"!]', '', terms)
### initialise docfreq for this document
### list contains counts for each term in the document
    docfreq = {}

### add the vocab counts and postings
    for word in termlist:
        if (word.lower() in vocab):
            wordid = vocab.index(word.lower()) ##making wordid the index in vocab if word in dictionary
        else:
            vocab.append(word.lower()) ## add lowercase word to vocab if not seen before
            wordid = vocab.index(word.lower()) ## new words assigned wordid
            
####### keep the counts of words in docfreq
        if (wordid in docfreq):
            docfreq[wordid] += 1
        else:
            docfreq[wordid] = 1
        

### to add term frequencies to the postings need docid+count for each term in the document
    for wordid in docfreq:
        docf=docid+','+str(docfreq[wordid])
        #print("DOCF ",docf)
        #print("word"+word+"docfreq"+docf)
        if (not wordid in postings):
            postings[wordid]=[docf] ##postings hold the docids in respect to the word wordid 
        else:
            postings[wordid].append(docf) ##add docid to the list od docids where the wordid appears
   
    #print(postings[3])
#### testing each crawl
    print("postings:", postings) ##testingggggggg
    #print("----------------------------------------------------------------------------")
    print ("Docfreq = ", docfreq)
    #print("----------------------------------------------------------------------------")
    #print("vocab= ", vocab)
    return
#### save the index after every 100 documents ####
    if (len(doclength)%100 == 0): # 
        n = int(len(doclength)/100)%2
        write_index_files(n)
    return


# Standard boilerplate to call the main() function
if __name__ == '__main__':
    main()