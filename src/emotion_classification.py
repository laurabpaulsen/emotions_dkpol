"""
Classifies the emotions of the cleaned tweets.

Inspired by: emoDynamics (https://github.com/saraoe/emoDynamics)
"""

import pandas as pd
import os
from transformers import pipeline


def classify_emotions(df, nlp):
    """Classifies the emotions of the cleaned tweets.

    Args:
        df (pd.DataFrame): Dataframe containing the tweets to classify

    Returns:
        df (pd.DataFrame): Dataframe containing the classified tweets
    """
    print('Classifying emotions...')
    # get probabilities for each emotion
    
    df['emotion'] = [nlp(tweet) for tweet in df['clean_tweet']]

    # create a new column for each emotion
    for i in range(len(df['emotion'])):
        emotions = df['emotion'][i] # getting one row
        for emotion in range(6): # getting one emotion
            emo = emotions[0][emotion]
            label = emo['label']
            prob = emo['score']
            df.loc[i, label] = prob

    return df



if __name__ == '__main__':
    df = pd.read_csv(os.path.join('data', 'preprocessed', 'dk_pol_data.csv'))

    model_path = "NikolajMunch/danish-emotion-classification"
    nlp = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path, return_all_scores=True)
    
    df = classify_emotions(df, nlp=nlp)
    df.to_csv(os.path.join('data', 'preprocessed', 'dk_pol_data_emotions.csv'), index=False)


