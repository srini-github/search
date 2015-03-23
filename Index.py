__author__ = 'srini'
from nltk.stem.snowball import SnowballStemmer
from stop_words import get_stop_words
from collections import defaultdict
import math
import string
import json
import time
import re


class Search:

    token_list = defaultdict()
    doc_list = defaultdict()
    stop_words = get_stop_words('en')
    stemmer = SnowballStemmer("english")
    regex = re.compile('[%s]' % re.escape(string.punctuation))  # To remove punctuations from tokenized terms

    def __init__(self, library_name):
        self.doc = library_name
        #TODO: Create index file name based on given library_name

    def index_document(self, document_name=None, doc=None):
        """
        :param document_name: a name for the document. suppose to be unique
        :param doc: full path of the document on the local disk
        :return: True if successful, else False
        """

        if document_name is None or doc is None:
            return False

        #TODO: check of <doc> exists before proceeding

        print "-------------"
        print "Indexing started... for <"+document_name+">"
        start = time.time()
        result = self.__tokenize(document_name, doc)
        end = time.time()

        if result:
            print "Indexing finished for <%s>. Time taken = %s secs " % (document_name, str(end-start))
            Search.doc_list[document_name] = doc
        else:
            print "Error: Indexing failed for <%s>" % document_name

    def __tokenize(self, document_name=None, doc=None, delimiter=None):
        """
        :param doc: full path of the document
        :param delimiter: default is single space
        :return: True if tokenization was successful else False
        """
        try:
            if doc is None or document_name is None:
                return False
            if delimiter is None:
                delimiter = ' '

            offset = 0
            line_count = 0
            prev_count = 0
            with open(doc, 'r') as f:
                for line in f:
                    prev_count = line_count
                    for word in line.split(delimiter):
                        #word = filter(lambda x: x in string.printable, word)
                        if offset == 0:
                            offset = line_count + 1
                            prev_count = len(word)+1
                        else:
                            offset = prev_count+1
                            prev_count = prev_count+len(word)+1

                        word = word.rstrip('\n').rstrip('\r').strip(' ')  # Step1 - stop words
                        word = Search.regex.sub('', word)  # Step2 - remove punctuations
                        word = Search.stemmer.stem(unicode(word, 'utf8'))  # Step3 - stemming
                        if word not in Search.stop_words:
                            if word in Search.token_list:
                                if document_name in Search.token_list[word]:
                                    Search.token_list[word][document_name].append(offset)
                                else:
                                    Search.token_list[word][document_name] = list()
                                    Search.token_list[word][document_name].append(offset)
                            else:
                                doc = dict()
                                doc[document_name] = list()
                                doc[document_name].append(offset)
                                Search.token_list[word] = doc

                    line_count += len(line)

            return True
        except Exception as e:
            print "Exception" + str(e)
            return False

    def term_frequency(self, term=None, document_name=None):
        """
        term freq of (term t1 in a doc d1) = 1 + log(freq of t1 in d1)
        A log normalization weighted scheme ref: http://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency
        :param term:
        :param document_name:
        :return:
        """
        try:
            ret_val = 1

            term = str(term)
            document_name = str(document_name)

            if term is None or document_name is None:
                return 1

            return 1 + math.log(len(Search.token_list[term][document_name]), 10)

        except Exception as e:
            #print "Error: Exception"+str(e)
            return 1

    def inverse_doc_frequency(self, term=None, document_name=None):
        '''
        inverse doc freq of (term1 in collection of documents D) = Total docs in the collection / Number of docs where the term1 appears
        :param term:
        :param document_name:
        :return:
        '''
        try:
            ret_val = 0

            term = str(term)
            document_name = str(document_name)

            if term is None or document_name is None:
                return 0

            #
            return 1 + math.log(len(Search.doc_list) / len(Search.token_list[term]), 10)

        except Exception as e:
            print "Error: Exception"+str(e)
            return 0

    def tf_idf(self, term=None, document_name=None):
        '''
        (term frequency) *  (inverse document frequency)
        Ref: http://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html
        :param term:
        :param document_name:
        :return:
        '''
        try:
            ret_val = 0

            term = str(term)
            document_name = str(document_name)

            if term is None or document_name is None:
                return 0

            return self.term_frequency(term, document_name) * self.inverse_doc_frequency(term, document_name)

        except Exception as e:
            print "Error: Exception"+str(e)
            return 0

    def search(self, search_terms=None):
        '''
        We tokenize given search term and calculate a score sum(term freq * inverse doc freq) for each term per doc.
        Higher the value more is the relevance.
        Ref: http://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html
        :param search_terms:
        :return:
        '''
        try:
            if search_terms is None:
                return []

            ret_list = defaultdict()
            split_list = search_terms.split()

            #First extract list of documents which match the given search terms after tokenizing and stemming each term
            document_match_list = set()
            search_tokenized_list = list()

            for term in split_list:
                term = Search.stemmer.stem(unicode(term, 'utf8'))
                if term in Search.token_list:
                    search_tokenized_list.append(term)
                    # The term exist in some doc, so peek and get doc list.
                    for doc in Search.token_list[term]:
                        document_match_list.add(doc)

            #Calculate sum(tf_idf of each team for each doc)
            for doc in document_match_list:
                rating = 0
                term_offset_list = defaultdict()
                #Iterate over each term of tokenized search terms
                for token_term in search_tokenized_list:
                    rating += self.term_frequency(token_term, doc)
                    try:
                        if doc in Search.token_list[token_term]:
                            term_offset_list[token_term] = Search.token_list[token_term][doc]
                    except:
                        print "exception...***"
                        term_offset_list[token_term] = []

                ret_list[doc] = {'score': int(round(rating)),
                                 'document_position': term_offset_list}

            return json.dumps(ret_list)
        except Exception as e:
            #raise
            #print "Exception" + str(e)
            return []

if __name__ == "__main__":

    lib1 = Search("library1")
    lib1.index_document("book.txt", "./tmp/book.txt") # http://www.gutenberg.org/cache/epub/2554/pg2554.txt
    lib1.index_document("wiki.txt", "./tmp/wikileaks.txt")  # http://mirror.wikileaks.info/files/messages_2001_09_11-10_55_2001_09_11-10_59.txt
    lib1.index_document("test.txt", "./tmp/test.txt")
    lib1.index_document("organic.txt", "./tmp/organic.txt")

    print "-------------\n"
    print "Total documents in the collection = %s " % str(len(Search.doc_list))
    for key, value in Search.doc_list.iteritems():
        print "Document name=<%s>, doc path=<%s> " % (key, value)
    print "-------------\n"
    print "SEARCH \n"
    while True:
        data = raw_input("Enter search terms (example: terror doctor) :")
        print "-------------  Search Result List  ------------ \n"
        result = json.loads(lib1.search(data))
        print json.dumps(result, indent=4, sort_keys=True)