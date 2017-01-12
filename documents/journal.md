161228
    Comparison of different websites in info.txt.
        We'll probably try seloger.com, immostreet.com and explorimmo.com
    Addition of a functional multithreaded crawler in demos_thenewboston/

161229
    First successful request of seloger.com.
        It did not work before because the header of the request was not correct.
    First successful crawling of the listing of seloger.com.
        We don't have the dataset yet. Only the listing has been crawled and not the ads themselves.
        For now, a partial list of the ads is already in seloger_listing.json.
            It contains about 7900 links out of about 8300.
        The reason why the list is not complete is because of a ban from the website
            To fight against that we'll have to torify the project.
    First t-sne try.
    First d3 map of Paris.
    First torification of the crawler.

161230
    The crawling of the listing is now complete! AND 2 LISTINGS ARE READY (01 is truncated, 02 is complete)
        Addition of visualize_json_distribution.py which gives interesting results on the truncated file listing (01).
        The crawler:
            - now has a better modularity
            - outputs the last html it received in last_html_before_break.html for debug
            - its tor system has been slightly modified (but it's not necessarily better)
            - and most importantly, it can restart where it was in case of interruption!

170107
    Analysing word distributions in descriptions :
    Extracting words and bigrams frequency  
    Now we can plot a histogram of "words prices" to see what we should avoid looking for if we want a cheap house ?


XX0107
    Getting inspired by Visualizing words used at the National Conventions 2012
    Plotting words in cercles with their frequency as a Radius and a color based on the mean price of the ads they appear in. 
    conclusion: vocabulary used between very different ads was also pretty different

XX0107
    Figure out an encoding for the data:


XX0107
    Use an effective dimensionality reduction technique (t-Sne)
    
    