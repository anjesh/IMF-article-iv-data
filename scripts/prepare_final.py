import re
import os
import csv

scriptpath = os.path.dirname(os.path.realpath(__file__))
dir_data_results = os.path.join(scriptpath, "../data-results")
file_article4 = os.path.join(dir_data_results, "pages_article_iv.csv")
dir_text_files = os.path.join(scriptpath, "../txt")
file_final_article4 = os.path.join(dir_data_results, "final_pages_article_iv.csv")

def get_meta_from_title(title):
    country = ""
    year = ""
    if len(document["title"].split(':')) > 1:
        country = document["title"].split(':')[0]
    elif len(document["title"].split(';')) > 1:
        country = document["title"].split(';')[0]

    years = re.findall("[0-9]{4}", title)
    if len(years):
        year = years[0]
    return {"country":country, "year":year}


with open(file_final_article4, "w") as fout:
    header = ["title", "page_link", "pdf_link", "txt_file", "country", "year", "size_kb"]
    csvwriter = csv.DictWriter(fout, header)
    csvwriter.writeheader()
    # read the article4 file rows to process each file
    with open(file_article4, "r") as fin:
        csvreader = csv.reader(fin)
        # ignore header
        next(csvreader)        
        documents = []
        for row in csvreader:
            document = {
                "pdf_link": row[0],
                "page_link": row[1],
                "title": row[2]
            }
            meta = get_meta_from_title(document["title"])
            document["country"] = meta["country"]
            document["year"] = meta["year"]
            text_filename = document["pdf_link"].split('/')[-1].split(".")[0] + ".pdf.txt"
            text_filepath = os.path.join(dir_text_files, text_filename)
            document["txt_file"] = text_filename
            document["size_kb"] = os.path.getsize(text_filepath)/1024
            csvwriter.writerow(document)
