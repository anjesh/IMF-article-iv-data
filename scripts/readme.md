
### prepare final_pages_article_iv.csv file containing key metadata

$ cd scripts

$ python prepare_final.py

> reads pages_article_iv.csv and prepares final_pages_article_iv.csv with extra meta fields

manually fix the file for improper patterns if requird

### look for words in article4 document

$ cd scripts

> update the words to be searched in the text in search.py

> update the words in the following array (add, edit or remove)

> search_words = ["third", "process", "consult", "oil", "discovery", "nepal", "india"]

$ python search.py

> reads final_pages_article_iv.csv for the files, copies the metadat data and search for the words in the txt file.

> creates a file data-results/pattern_count.csv with the count for each search words 


### look for words in proximity with other word in article4 document

$ cd scripts

> update the words to be searched in the text in search.py

> update the words in the following array (add, edit or remove)

> search_words = {"discover":["oil", "gas", "mineral"]} will search for oil, gas, mineral in proximity to discover

$ python proximity_search.py

> reads final_pages_article_iv.csv for the files, copies the metadat data and search for the words in the txt file.

> creates a file data-results/pattern_count_boundary.csv with the count for each search words in proximity to other

> currently the proximity is 50 words, i.e. if oil is within 50 words distance to discover, then it is counted otherwise ignored