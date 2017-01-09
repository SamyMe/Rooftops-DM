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



def extract_words_prices(file_name, price_threshold=1):
    # Tokenize
    tokenizer = RegexpTokenizer(r'\w+')

    # Read ads Data
    with open(file_name, 'rt') as f:
        ads = json.loads(f.read())

        words_prices = {}

        for ad in ads:

            desc = ads[ad]['description']

            # Before Filtering
            desc_filtered = [
                            word.lower() for word in tokenizer.tokenize(desc) if
                                (
                                word.lower() not in stopwords.words('french')
                and len(word) > 1
                and not word.isdigit()
                                )
                            ]

            # After Filtering
            for w in desc_filtered:
                if w in words_prices:
                    words_prices[w][0] += 1
                    words_prices[w][1] += ads[ad]['price']

                else:
                    words_prices[w] = [1, ads[ad]['price']]

        # Making the mean
        for w in words_prices:
            words_prices[w] = words_prices[w][1] / words_prices[w][0] 

    print(words_prices)

    # Write to CSV
    with open("data/words_prices.csv", 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["word", "price"])
        for word in words_prices:
            if words_prices[word] > price_threshold:
                csv_writer.writerow([word, words_prices[word]])


def transform_ads(file_name, descriptive_words):
    # Tokenize
    tokenizer = RegexpTokenizer(r'\w+')

    embeddings = []

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

            embeddings.append([ in_ad(word) for word in descriptive_words ])

    print(len(embeddings))
    print(len(embeddings[0]))
    print(embeddings[0])

    f = open("data/embeddings.pkl",'wb')
    pickle.dump(embeddings,f)
    f.close()


if __name__ == "__main__":

    file_name = "../crawlers/data_full/03_seloger_ads_compressed.json"

    # read_data(file_name)
    # extract_freq()
    # convert_CSV("data/freqs_descr.pkl", 100)
    # extract_words_prices(file_name)

    descriptive_words = sorted(
                        [ element[0] for element in csv.reader(
                            open('data/all_freqs.csv','rt'), delimiter=',') 
                        ])
    
    transform_ads(file_name, descriptive_words)
