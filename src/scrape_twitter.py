'''
Scrapes tweets from Twitter using the TwitterSearchScraper package and saves them to a csv file.
Uses multiple threads to speed up the process.

Usage: python scrape_twitter.py
'''
import snscrape.modules.twitter as sntwitter
import pandas as pd
import multiprocessing as mp
import json

def scrape(string, type, party):
    """Scrapes tweets from Twitter using the TwitterSearchScraper package and saves them to a csv file.
    
    Args:
        string (str): hashtag or mention to search for
        type (str): Type of search. Can be 'hashtag' or 'mention'
        party (str): Name of the party
    
    Returns:
        None
    """
    if type == '@':
        out_type = 'mentions'
    elif type == '#':
        out_type = 'hashtag'
    out_path = f'data/raw/{party}_{out_type}.csv'
    attributes_container = []

    for tweet in sntwitter.TwitterSearchScraper(f'{type}{string} since:2022-05-01 until:2022-11-27').get_items():
        if tweet.lang == 'da':
            attributes_container.append([tweet.username, tweet.date, tweet.likeCount, tweet.content, tweet.lang])
        
    # Creating a dataframe from the tweets list above 
    tweets_df = pd.DataFrame(attributes_container, columns=[ "username", "date_created", "number_of_likes", "tweets", "language"])
    tweets_df['party'] = party

    # save to csv
    tweets_df.to_csv(out_path, index=False)



if __name__ == '__main__':
    party_info = json.load(open('data/party_info.json'))

    inputs = []
    for party in party_info:
        if 'hashtag' in party_info[party]:
            inputs.append([party_info[party]['hashtag'], '#', party_info[party]['party']])
        if 'mention' in party_info[party]:
            inputs.append([party_info[party]['mention'], '@', party_info[party]['party']])

    inputs.append(['dkpol', '#', 'dkpol'])

    with mp.Pool(mp.cpu_count()) as pool:
        pool.starmap(scrape, inputs)

