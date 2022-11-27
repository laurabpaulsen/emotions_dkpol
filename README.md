# emotions_dkpol
This repository holds the code for the final project for Cultural Data Science


## Project Organization
The organization of the project is as follows:

```
├── README.md                                       
├── data
│   ├── party_info.json        <- information on each party (Twitter account, hashtag)   
│   ├── raw                    
│   └── preproccessed                       
├── src                        <- main scripts
│   ├── scrape_twitter.py
│   ├── clean_data.py
│   └── create_party_info.py
├── fig

```

## Pipeline

| Do | File| Output placement |
|-----------|:------------|:--------|
Scrape tweets | ```src/scrape_tweets.py```| ```../data/raw```
Clean tweets | ```src/clean_tweets.py``` | ```../data/preprocessed```
