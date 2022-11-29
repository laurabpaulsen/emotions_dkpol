"""
Classifies the emotions of the cleaned tweets.

Inspired by: emoDynamics (https://github.com/saraoe/emoDynamics)
"""
import multiprocessing as mp
import pandas as pd
import os
from transformers import pipeline
from tqdm import tqdm

model_path = "NikolajMunch/danish-emotion-classification"
nlp = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path, return_all_scores=True)

def split_dataframe(df, chunk_size = 10000): 
    chunks = list()
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(df[i*chunk_size:(i+1)*chunk_size])
    
    return chunks

def classify_emotions(df):
    """Classifies the emotions of the cleaned tweets.

    Args:
        df (pd.DataFrame): Dataframe containing the tweets to classify

    Returns:
        df (pd.DataFrame): Dataframe containing the classified tweets
    """
    print('Classifying emotions...')

    df = df.reset_index()
    df['emotion'] = [nlp(tweet) if type(tweet)=='str' else '' for tweet in tqdm(df['clean_tweet'])]

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
    #df['clean_tweet'] = df['clean_tweet'].astype(str)

    df_chunks = split_dataframe(df, chunk_size = 7500)

    p = mp.Pool(mp.cpu_count()-2)
    results = p.map(classify_emotions, df_chunks)
    df = pd.concat(results, axis=0)
    
    #df = classify_emotions(df, nlp=nlp)
    df.to_csv(os.path.join('data', 'preprocessed', 'dk_pol_data_emotions.csv'), index=False)


