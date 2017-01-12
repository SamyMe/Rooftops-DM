#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import pickle
import csv
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from operator import itemgetter
import random
from utils_json import *
i = 0

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def read_data(file_name):
    # Tokenize
    tokenizer = RegexpTokenizer(r'\w+')

    # Read ads Data
    with open(file_name, 'rt') as f:
        ads = json.loads(f.read())

        descriptions = []
        tags = []

        for ad in ads:

            desc = ads[ad]['description']
            tags.extend([tag.lower() for tag in ads[ad]['tags'] if not has_numbers(tag)])

            # Before Filtering
            desc_filtered = [
                            word.lower() for word in tokenizer.tokenize(desc) if
                                (
                                word.lower() not in stopwords.words('french')
                                and len(word) > 2
                                and not has_numbers(word)
                                )
                            ]

            # After Filtering
            descriptions.extend(desc_filtered)

    # Save the data
    f = open('data/processed_descr.pkl','wb')
    pickle.dump((descriptions, tags), f)
    f.close()


# Extracting words and bigrams frequences
def extract_freq():
    f = open('data/processed_descr.pkl', 'rb')
    desc, tags = pickle.load(f)
    f.close()

    # Freq.Dest of words in descriptions
    fd = FreqDist(tags+desc)

    # Discovering word collocations
    bcf = BigramCollocationFinder.from_words(desc)
    # Top 4 bigrams
    best = bcf.nbest(BigramAssocMeasures.likelihood_ratio, 4)

    print("Number of unique words")
    print(fd.B())
    print("Number of unique bigrams")
    print(bcf.ngram_fd.B())

    # Don't forget to Pickle cleaned data once done
    result = dict(fd)
    result.update(dict(bcf.ngram_fd))

    print("Sum:")
    print(len(result))

    f = open("data/freqs_descr.pkl",'wb')
    pickle.dump(result,f)
    f.close()


# Exporting to CSV
def convert_CSV(input_file, threshold=1):
    f = open(input_file, 'rb')
    fd = pickle.load(f)

    with open("data/all_freqs.csv", 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["word", "freq"])
        for item in sorted(fd.items(), key=itemgetter(1), reverse=True):
            key = item[0]
            if fd[key] > threshold:
                w = key
                if len(key) == 2:
                    w = key[0]+" "+key[1]
                csv_writer.writerow([w, fd[key]])


# Compute average price per words and export it to a json file
def extract_words_prices(file_name, price_threshold=1,regenerate=False) :

    if regenerate:
        # Tokenize
        tokenizer = RegexpTokenizer(r'\w+')

        # Read ads Data
        with open(file_name, 'rt') as f:
            ads = json.loads(f.read())

            words_prices = {}

            for ad in ads:

                desc = ads[ad]['description']

                tags= [tag.lower() for tag in ads[ad]['tags'] if not has_numbers(tag)]

                # Description Filtering
                desc_filtered = [
                                word.lower() for word in tokenizer.tokenize(desc) if
                                    (
                                    word.lower() not in stopwords.words('french')
                                    and len(word) > 2
                                    and not has_numbers(word)
                                    )
                                ]

                # Extracting Bigrams
                bcf = BigramCollocationFinder.from_words(desc_filtered)

                all_words = desc_filtered+tags
                all_words +=[ w1+' '+w2  for w1,w2 in bcf.ngram_fd.keys()]

                # After Filtering
                for w in desc_filtered:
                    price_p_surf = float(ads[ad]['surface'].replace(',','.')) if ads[ad]['surface']!='' else 1
                    price_p_surf = ads[ad]['price'] / price_p_surf

                    if w in words_prices:
                        words_prices[w][0] += 1
                        words_prices[w][1] += ads[ad]['price']
                        words_prices[w][2] += price_p_surf
                        words_prices[w][3] += ads[ad]['price'] / price_p_surf

                    else:
                        words_prices[w] = [ 1 , 
                                            ads[ad]['price'], 
                                            price_p_surf,
                                            ads[ad]['price'] / price_p_surf]

            # Calculating the mean
            for w in words_prices:
                for i in range(1, 4):
                    words_prices[w][i] = words_prices[w][i] / words_prices[w][0] 

        f = open('data/words_prices.pkl', 'wb')
        pickle.dump(words_prices, f)
        f.close()

    else:
        f = open('data/words_prices.pkl', 'rb')
        words_prices = pickle.load(f)
        f.close()

    i = 0
    # print(words_prices)
    def to_dict(w_p):
        global i
        i+=1
        result_dict = {
            "name": w_p[0]
            ,"price": w_p[1][1]
            ,"surface": w_p[1][2]
            ,"price_p_surf": w_p[1][3]
            ,"id": i
            ,"count": w_p[1][0]
            ,"k":w_p[1][1]
            ,"bias":0.4
            ,"index":i
            }
        

        return result_dict

    words_100 = {"topics": [ to_dict(elem) for elem in sorted(words_prices.items(), reverse=True, key=lambda x: x[1][1])[:50:2]]}

    # Write to JSON
    with open("../d3/bubbles-viz/prices_100_words.json", "wt") as f:
        f.write(json.dumps(words_100))


# Transform a crwaled add to an embedding (binary vector)
def transform_ads(file_name, descriptive_words):
    # Tokenize
    tokenizer = RegexpTokenizer(r'\w+')

    embeddings = {}
        
    # Read ads Data
    with open(file_name, 'rt') as f:
        ads = json.loads(f.read())

        for ad in ads:
            # Discripton iExtraction
            desc = ads[ad]['description']

            # Tags Extraction
            tags= [tag.lower() for tag in ads[ad]['tags'] if not has_numbers(tag)]

            # Description Filtering
            desc_filtered = [
                            word.lower() for word in tokenizer.tokenize(desc) if
                                (
                                word.lower() not in stopwords.words('french')
                                and len(word) > 2
                                and not has_numbers(word)
                                )
                            ]

            # Extracting Bigrams
            bcf = BigramCollocationFinder.from_words(desc_filtered)

            all_words = desc_filtered+tags
            all_words +=[ w1+' '+w2  for w1,w2 in bcf.ngram_fd.keys()]

            in_ad = lambda word : 1 if word in all_words else -1

            embeddings[ad] = [ in_ad(word) for word in descriptive_words ]

    print(len(embeddings))

    with open("data/embeddings.json", "wt") as f:
        f.write(json.dumps(embeddings, separators=(',', ':')))
    

if __name__ == "__main__":

    file_name = "../crawlers/data_full/03_seloger_ads_compressed.json"

    # read_data(file_name)
    # extract_freq()
    # convert_CSV("data/freqs_descr.pkl", 100)
    extract_words_prices(file_name)

    descriptive_words = sorted(
                        [ element[0] for element in csv.reader(
                            open('data/all_freqs.csv','rt'), delimiter=',') 
                        ])
    
    # transform_ads(file_name, descriptive_words)
