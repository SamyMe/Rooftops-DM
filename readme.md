# Rooftops

### Context

The goal here is to build, visualize and analyse a dataset of apartment renting ads in Paris. The result of this study can be found [here](https://rooftopscorp.github.io/).

### How to use the files

This repo contains all the necessary files the redo the whole thing.

* First, don't forget all the requirements (listed below) to avoid quite a few headaches.

* Then, use the listing crawler (`seloger_listing_crawler.py`) to get a list of urls (from [seloger.com](http://www.seloger.com/)) of apartment renting ads in Paris. (Please use this in [moderation](http://softwareengineering.stackexchange.com/a/91781)).

* Before going any further, you can produce a few curves and histograms about the prices of the apartments with `visualize_json_distribution.py`

* Once you have the links of all the ads, get the _content_ of the ads with `seloger_ads_crawler.py` (again, [moderation](http://softwareengineering.stackexchange.com/a/91781)). This should take 4 to 6 hours and result in 1.5 to 2 Go of data.

* Parse the ads with `seloger_ads_parser.py` to extract the text description of each ad, as well as the price of the apartment, its area, agency, id, location... etc.

* Use `nltk_ads_reader.py` to generate the "embeddings" of each ad. In background, the 800 or so most frequent words are extracted, and each ad is assigned to a binary vector representing the presence (or absence) of each of these words.

* Use `dump_price_per_area.py` to generate a simple scatter plot of apartments with prices on the X axis and areas on the Y axis. (This step does not require the embeddings). Here is an example:
      python3 dump_price_per_area.py
          --json "./data/main/seloger_ads_compressed.json"

* Reduce the number of dimensions of the embeddings with `dump_tsne_on_ads.py`. Here is a link to the website of the [hero](https://lvdmaaten.github.io/tsne/) that came up with this. And [here](http://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html) is the official documentation in sklearn.
```bash
python3 dump_tsne_on_ads.py --json "./data/main/words_embeddings.json"
```

* At this point, you can have a general idea of what your visualizations will look like with `visualize_embeddings.py`.
```bash
python3 visualize_embeddings.py --data "./data/plots/"
```

* You can then produce the datasets to be visualized in d3 with `dump_final_datasets.py`.
```bash
python3 dump_final_datasets.py --data "./data/plots/"
```

* Finally, you should obtain something like [this](https://rooftopscorp.github.io/). :D


### Requirements

* __For the crawl__:
  * tor
  * requests + socks5
  * beautifulsoup


* __For data analysis__:
  * numpy
  * matplotlib
  * sklearn

### Structure of the repository

* `javascript/` contains the visualization in d3.  
  * `javascript/viz_bubbles/` contains the code of a visualization of words as a bubble chart (see [here](https://rooftopscorp.github.io/) to see the result).  
  * `javascript/viz_tsne/` contains the code of several visualizations of ads as bubble charts (see [here](https://rooftopscorp.github.io/) to see the results).  

* `python/` contains most the core code used to get the data and process it (crawling, parsing, natural language processing, dimensionality reduction, plotting with matplotlib).  
  * `python/main_data/` contains the results of the crawl (with `seloger_full_listing.json` first and `seloger_ads_compressed.json` second).  
  * `python/nltk_data/` contains the results of the natural language processing treatments to get the bag-of-words and therefore the "embeddings" of the ads in `embeddings.json.zip`.  
  * `python/nltk_data/` contains the results of dimensionality reduction with tsne and mds. The files that start with `data_` contain only the coordinates of the points (aka the ads). And the files that start with `final_data_` contain the coordinates of the points as well as additional information about the ads.

### Requirements

* __For the crawl__:
  * tor
  * requests + socks5
  * beautifulsoup


* __For data analysis__:
  * numpy
  * matplotlib
  * sklearn
