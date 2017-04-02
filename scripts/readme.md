
## convert all pdfs to text

cd ./pdfs
for f in *; do pdftotext $f "../txt/$f.txt" ;done

## prepare final_pages_article_iv.csv file containing key metadata

cd scripts
python prepare_final.py
> reads pages_article_iv.csv and prepares final_pages_article_iv.csv with extra meta fields

manually fix the file for improper patterns if requird

## look for words in article4 document

cd scripts
> update the words to be searched in the text in search.py
> update the words in the following array (add, edit or remove)
> search_words = ["third", "process", "consult", "oil", "discovery", "nepal", "india"]
python search.py
> reads final_pages_article_iv.csv for the files, copies the metadat data and search for the words in the txt file.
> creates a file data-results/pattern_count.csv with the count for each search words 