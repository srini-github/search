# search
Simple text search engine

To use or test:

1.  Clone the repo
2.  Make sure all modules in `Index.py` are installed, if not use pip install them
3.  `Index.py` uses files under `tmp` directories ( 4 in total) to build the inverted index.
4. Run `$python Index.py'. The program will index 4 fiels one after the other and then prompt for search terms
5. Enter the search terms and it will produce output like below:
```
-------------
Indexing started... for <book.txt>
Indexing finished for <book.txt>. Time taken = 5.58883213997 secs 
-------------
Indexing started... for <wiki.txt>
Indexing finished for <wiki.txt>. Time taken = 1.74657297134 secs 
-------------
Indexing started... for <test.txt>
Indexing finished for <test.txt>. Time taken = 0.000795841217041 secs 
-------------
Indexing started... for <organic.txt>
Indexing finished for <organic.txt>. Time taken = 0.000811100006104 secs 
-------------

Total documents in the collection = 4 
Document name=<book.txt>, doc path=<./tmp/book.txt> 
Document name=<test.txt>, doc path=<./tmp/test.txt> 
Document name=<wiki.txt>, doc path=<./tmp/wikileaks.txt> 
Document name=<organic.txt>, doc path=<./tmp/organic.txt> 
-------------

SEARCH 

Enter search terms (example: terror doctor) :fruit
-------------  Search Result List  ------------ 

{
    "book.txt": {
        "document_position": {
            "fruit": [
                97215, 
                639358, 
                711686
            ]
        }, 
        "score": 1
    }, 
    "organic.txt": {
        "document_position": {
            "fruit": [
                16, 
                32
            ]
        }, 
        "score": 1
    }
}
```
