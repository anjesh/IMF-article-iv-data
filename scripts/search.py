import re
import os
import csv

scriptpath = os.path.dirname(os.path.realpath(__file__))
dir_data_results = os.path.join(scriptpath, "../data-results")
file_final_article4 = os.path.join(dir_data_results, "final_pages_article_iv.csv")
dir_text_files = os.path.join(scriptpath, "../txt")
file_pattern_count = os.path.join(dir_data_results, "pattern_count.csv")

search_words = ["discover", "oil", "gas", "mineral"]

"""
looks for search words in the text file and return the count of each word
"""
def find_words_in_txtfile(text_filename, search_words):
    count_words = {}
    for word in search_words:
        count_words[word] = 0
    with open(text_filename, "r") as fp:
        lines = fp.readlines()
        for line in lines:
            for word in search_words:
                if line.find(word) != -1:
                    count_words[word] += 1
    return count_words

with open(file_pattern_count, "w") as fout:
    header = ["country", "year", "title", "page_link", "pdf_link", "txt_file", "size_kb"]
    for word in search_words:
        header.append(word)
    csvwriter = csv.DictWriter(fout, header)
    csvwriter.writeheader()
    # read the article4 file rows to process each file
    with open(file_final_article4, "r") as fin:
        csvreader = csv.reader(fin)
        # ignore header
        next(csvreader)        
        documents = {}
        for row in csvreader:
            document = {
                "title": row[0],
                "page_link": row[1],
                "pdf_link": row[2],
                "txt_file": row[3],
                "country": row[4],
                "year": row[5],
                "size_kb": row[6],
            }
            text_filepath = os.path.join(dir_text_files, document["txt_file"])            
            count_words = find_words_in_txtfile(text_filepath, search_words)
            for word in search_words:
                document[word] = count_words[word] if word in count_words.keys() else 0            
            csvwriter.writerow(document)
