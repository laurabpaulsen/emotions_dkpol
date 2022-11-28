"""
Concatenates the data from the different files into a single file, cleans it for emotion classification and saves it to a csv file.
"""

import pandas as pd
import os
import re
from tqdm import tqdm


def clean_tweet(tweet):
    """Remove mentions, hashtags, URLs, emojis

    Args:
        tweet (str): Tweet to clean
    """
    clean_tweet = re.sub(r'@(\S*)\w', '', tweet) # remove mentions
    clean_tweet = re.sub(r'#\S*\w', '', clean_tweet) # remove hashtags
    url_pattern = re.compile(
        r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
    clean_tweet = re.sub(url_pattern, '', clean_tweet) # remove URLs
    clean_tweet = re.sub('\n', '', clean_tweet) # remove new line
    clean_tweet = re.sub('\t', '', clean_tweet) # remove tab
    clean_tweet = re.sub(r'\\u\S*\w', '', clean_tweet) # remove emojis
    
    return clean_tweet


if __name__ in '__main__':
    path = os.path.join('..', 'data', 'raw')
    files = os.listdir(os.path.join('data', 'raw'))
    df = pd.concat([pd.read_csv(os.path.join('data', 'raw', file)) for file in files], ignore_index=True)
    #df.drop_duplicates(inplace=True)
    
    df['clean_tweet'] = ''
    for i in tqdm(range(len(df))):
        df['clean_tweet'][i] = clean_tweet(df['tweets'][i])

    df.to_csv(os.path.join('data', 'preprocessed', 'dk_pol_data.csv'), index=False)
