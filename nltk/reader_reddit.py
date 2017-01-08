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

def read_data(file_name):
    # Tokenize
    tokenizer = RegexpTokenizer(r'\w+')

    # Read ads Data
    with open(file_name, 'rt') as f:
        ads = json.loads(f.read())

        descriptions = []

        for ad in ads:

            desc = ads[ad]['text']

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
            descriptions.extend(desc_filtered)

    # Save the data
    f = open('data/processed_descr.pkl','wb')
    pickle.dump(descriptions, f)
    f.close()

def extract_freq():
    f = open('data/processed_descr.pkl', 'rb')
    desc = pickle.load(f)
    f.close()

    # Freq.Dest of words in descriptions
    fd = FreqDist(desc)
    print(fd.elements)
    print("Number of occurence of <séjour>: %s" % fd["séjour"])
    print("Frequency: %s" % fd.freq("séjour"))

    # Discovering word collocations
    bcf = BigramCollocationFinder.from_words(desc)
    print("salle séjour: %s" % bcf.ngram_fd[("salle", "séjour")])
    # Top 4 bigrams
    best = bcf.nbest(BigramAssocMeasures.likelihood_ratio, 4)
    print("Top 4 bigrams: "+str(best))

    # print(fd.N )
    # print(len(dict(fd)) )
    # print(len(dict(bcf.ngram_fd)))

    # Don't forget to Pickle cleaned data once done
    f = open("data/freqs_descr.pkl",'wb')
    pickle.dump((fd,bcf),f)
    f.close()


def convert_CSV(input_file, word_threshold=1, bigram_threshold=1):
    f = open(input_file, 'rb')
    fd, bcf = pickle.load(f)

    with open("data/words_freqs.csv", 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["word", "freq"])
        for key in fd.keys():
            if fd[key] > word_threshold:
                csv_writer.writerow([key, fd[key]])

    with open("data/bigrams_freqs.csv", 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["word", "freq"])
        bfd = dict(bcf.ngram_fd)
        for key in bfd.keys():
            if bfd[key] > bigram_threshold:
                csv_writer.writerow([key[0]+" "+key[1], bfd[key]])


def extract_words_prices(file_name, price_threshold=1):
    # Tokenize
    tokenizer = RegexpTokenizer(r'\w+')

    # Read ads Data
    with open(file_name, 'rt') as f:
        ads = json.loads(f.read())

        words_prices = {}

        for ad in ads:

            desc = ads[ad]['text']

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


if __name__ == "__main__":

    file_name = "../crawlers/data/tmp_seloger_desc.json"

    # read_data(file_name)
    # extract_freq()
    # convert_CSV("data/freqs_descr.pkl", 1, 1)
    extract_words_prices(file_name)
