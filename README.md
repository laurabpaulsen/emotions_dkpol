# emotions_dkpol
This repository holds the code for the final project for Cultural Data Science


## Project Organization
The organization of the project is as follows:

```
├── README.md                  <- The top-level README for this project.                        
├── data                       
│   ├── raw                    
│   └── preproccessed                       
├── src                        <- main scripts
│   ├── scrape_twitter.py
│   └── clean_data.py
```

## Pipeline

| Do | File| Output placement |
|-----------|:------------|:--------|
Scrape tweets | ```src/scrape_tweets.py````| ```../data/raw```
Summarize the emotion distributions | ```src/summarize_models.py``` | ```summarized_emo/```
Run newsFluxus pipeline | ```src/emotionsFluxus.py``` | ```idmdl/```
Smooth the signal | ```src/smoothing.py``` | ```idmdl/smoothed/```
Identify change points | ```src/changepoints.py``` | ```idmdl/changepoints/```
