from stemming.porter2 import stem
import re
import os
import csv

scriptpath = os.path.dirname(os.path.realpath(__file__))
dir_data_results = os.path.join(scriptpath, "../data-results")
file_final_article4 = os.path.join(dir_data_results, "final_pages_article_iv.csv")
dir_text_files = os.path.join(scriptpath, "../txt")
file_pattern_count = os.path.join(dir_data_results, "pattern_count_boundary.csv")

search_words = {"discover":["oil", "gas", "mineral"], "discovery":["oil", "gas", "mineral"]}

"""
caches the stemmed words for better performance
Observe the performance by calling stem(xxx) vs cache_stem(xxx)
"""
caches = {}
def cache_stem(word):
    if word in caches:
        return caches[word]
    caches[word] = stem(word)
    return caches[word]

"""
function to stem words for the search_words for clarity as it contains list of a list
"""
def stem_search_words(search_words):
    stemmed_search_words = {}
    for w1 in search_words.keys():
        stemmed_search_words[stem(w1)] = []
        for w2 in search_words[w1]:
            stemmed_search_words[stem(w1)].append(stem(w2))
    return stemmed_search_words

"""
looks for search words in the text file and return the count of each word
"""
def find_words_in_proximity_in_txtfile(text_filename, search_words, proximi = 50):
    count_words = {}
    count_key_words = {}
    all_search_words = []
    with open(text_filename, "r") as fp:
        text_words = [cache_stem(word) for word in fp.read().lower().split()]
        # after stemming consultation becomes consult, discover becomes discov
        count = 0
        for w1 in text_words:
            count += 1
            # proximity word is found
            if w1 in search_words.keys():
                if not w1 in count_words:
                    count_words[w1] = {}
                for w2 in search_words[w1]:
                    # is the search word in proximity with the key word
                    if w2 in text_words[count - proximi: count + proximi]:
                        if w2 in count_words[w1]:
                            count_words[w1][w2] += 1
                        else:
                            count_words[w1][w2] = 1
    return count_words

search_words = stem_search_words(search_words)
with open(file_pattern_count, "w") as fout:
    header = ["country", "year", "title", "page_link", "pdf_link", "txt_file", "size_kb"]
    for word in search_words.keys():
        for w in search_words[word]:
            header.append(word+"-"+w)
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
            count_words = find_words_in_proximity_in_txtfile(text_filepath, search_words)
            if count_words.keys():
                for word in search_words.keys():
                    for w in search_words[word]:
                        document[word+"-"+w] = count_words[word][w] if word in count_words.keys() and w in count_words[word] else ""
            csvwriter.writerow(document)
