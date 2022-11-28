"""
Script for generating plots used for the final project
+ a few other plots
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
import pandas as pd
import os


palette = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4']

def plot_all_grid(df, figsize=(20, 10), normalize=True):
    """
    Plots the emotions of the tweets. One subplot for each emotion.
    """
    matplotlib.rcParams['font.family'] = 'serif'
    fig, axes = plt.subplots(2, 3, figsize=figsize, sharex=True, sharey=True)

    date_form = mdates.DateFormatter("%b-%Y")

    emotions = ['Afsky', 'Frygt', 'Glæde', 'Overraskelse', 'Tristhed', 'Vrede']

    for i, ax in enumerate(axes.flatten()):
        if normalize: #min max normalisation
            emotion = (df[emotions[i]] - df[emotions[i]].min()) / (df[emotions[i]].max() - df[emotions[i]].min())
        ax.plot(df['date_created'], emotion, color = palette[i], alpha=0.3)

        # plot smoothed line
        gaussian = emotion.rolling(window=20, win_type='gaussian', center=True, min_periods=1).mean(std = 1)
        ax.plot(df['date_created'], gaussian, color = palette[i], label = emotions[i], alpha=1)

        ax.xaxis_date()
        ax.xaxis.set_major_formatter(date_form)
        ax.set_title(emotions[i])

    fig.suptitle('Normalized emotions', fontsize=20)
    plt.savefig(os.path.join('fig', 'all_emotions.png'))

    plt.close()

def plot_fluxus(df, figsize=(20, 10), filename='fluxus.png'):
    """
    Plots transience, novelty and resonance
    """
    matplotlib.rcParams['font.family'] = 'serif'
    fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=True, sharey=True)

    date_form = mdates.DateFormatter("%b-%Y")

    for i, ax in enumerate(axes.flatten()):
        ax.plot(df['date'], df.iloc[:, 2+i], color = palette[i], alpha=0.3)

        # plot smoothed line
        gaussian = df.iloc[:, 2+i].rolling(window=20, win_type='gaussian', center=True, min_periods=1).mean(std = 1)
        ax.plot(df['date'], gaussian, color = palette[i], alpha=1)

        ax.xaxis_date()
        ax.xaxis.set_major_formatter(date_form)
        ax.set_title(df.columns[2+i])

    plt.savefig(os.path.join('fig', filename))



if __name__ == '__main__':
    df = pd.read_csv(os.path.join('data', 'preprocessed', 'dk_pol_data_emotions.csv'))
    df['date_created'] = pd.to_datetime(df['date_created'])
    plot_all_grid(df, normalize=True)

    df_fluxus_date = pd.read_csv(os.path.join('data', 'idmdl', 'emotions_summarized_date_W3.csv'))
    df_fluxus_date['date'] = pd.to_datetime(df_fluxus_date['date'])
    plot_fluxus(df_fluxus_date)

    df_fluxus_hour = pd.read_csv(os.path.join('data', 'idmdl', 'emotions_summarized_date_hour_W3.csv'))
    df_fluxus_hour['date'] = pd.to_datetime(df_fluxus_hour['date'])
    plot_fluxus(df_fluxus_hour, filename='fluxus_hour.png')


