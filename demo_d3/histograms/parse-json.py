import json
import csv

if __name__=="__main__":

    json_ads = 0
    with open("02_seloger_listing.json", 'rt') as f:
        json_ads = json.loads(f.read())

    prices = sorted([json_ads[ref]["price"] for ref in json_ads])

    with open("prices.csv", 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["id", "price"])
        for i in range(len(prices)):
            csv_writer.writerow([i, prices[i]])
