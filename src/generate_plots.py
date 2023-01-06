"""
Script for generating plots used for the final project
+ a few other plots
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mtpl
import pandas as pd
import os


palette = ['#911eb4', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#e6194b']
emotions = ['Afsky', 'Frygt', 'Glæde', 'Overraskelse', 'Tristhed', 'Vrede']

mtpl.rcParams['font.family'] = 'serif'
mtpl.rcParams['figure.titlesize'] = 20
mtpl.rcParams['axes.labelsize'] = 14
mtpl.rcParams['xtick.labelsize'] = 10
mtpl.rcParams['ytick.labelsize'] = 10
mtpl.rcParams['legend.fontsize'] = 10
mtpl.rcParams['figure.dpi'] = 300

def plot_days(ax, election = True, udskrives = True, linestyle = '--', alpha = 0.5, color = 'black', text = True):

    if election:
        ax.axvline(x=pd.to_datetime('2022-11-01', format = '%Y-%m-%d'), color=color, linestyle=linestyle, alpha=alpha)
        if text:
            ax.text(pd.to_datetime('2022-11-01', format = '%Y-%m-%d'), 0.5, 'Election', rotation=90, color=color, alpha=alpha)
        
    if udskrives:
        ax.axvline(x=pd.to_datetime('2022-10-05', format = '%Y-%m-%d'), color=color, linestyle=linestyle, alpha=alpha)
        if text:
            ax.text(pd.to_datetime('2022-10-05', format = '%Y-%m-%d'), 0.5, 'Announcement', rotation=90, color=color, alpha=alpha)


    return ax


def plot_all_grid(df, figsize=(20, 10), normalize=True):
    """
    Plots the emotions of the tweets. One subplot for each emotion.
    """
    fig, axes = plt.subplots(2, 3, figsize=figsize, sharex=True, sharey=True)

    date_form = mdates.DateFormatter("%b-%Y")

    df = df.sort_values(by='date_created')
    df['date_created'] = pd.to_datetime(df['date_created'], format = '%Y-%m-%d')

    emotions = ['Afsky', 'Frygt', 'Glæde', 'Overraskelse', 'Tristhed', 'Vrede']

    for i, ax in enumerate(axes.flatten()):
        if normalize: #min max normalisation
            emotion = (df[emotions[i]] - df[emotions[i]].min()) / (df[emotions[i]].max() - df[emotions[i]].min())
        else:
            emotion = df[emotions[i]]
        ax.plot(df['date_created'], emotion, color = palette[i], alpha=0.2)

        # plot smoothed line
        gaussian = emotion.rolling(window=50, win_type='gaussian', center=True, min_periods=1).mean(std = 2)
        ax.plot(df['date_created'], gaussian, color = palette[i], label = emotions[i], alpha=1)

        ax.xaxis_date()
        ax.xaxis.set_major_formatter(date_form)
        # turn xticks 90 degrees
        plt.setp(ax.get_xticklabels(), rotation=90, ha='center')
        ax.set_title(emotions[i])
        ax = plot_days(ax, text=False)

    if not normalize:
        save_path = os.path.join('fig', 'all_emotions.png')
    else:
        save_path = os.path.join('fig', 'all_emotions_normalized.png')
    
    plt.savefig(save_path)

def plot_emotions(df, figsize=(10, 10), normalize=True):
    """ 
    Plots the emotions of the tweets. One plot for all emotions.
    """
    date_form = mdates.DateFormatter("%b-%Y")

    df = df.sort_values(by='date_created')
    df['date_created'] = pd.to_datetime(df['date_created'], format = '%Y-%m-%d')

    emotions = ['Afsky', 'Frygt', 'Glæde', 'Overraskelse', 'Tristhed', 'Vrede']

    fig, ax = plt.subplots(figsize=figsize)

    for i, emotion in enumerate(emotions):
        if normalize: #min max normalisation
            emotion = (df[emotion] - df[emotion].min()) / (df[emotion].max() - df[emotion].min())
            
        else:
            emotion = df[emotion]
            ax.plot(df['date_created'], emotion, color = palette[i], alpha=0.2)
            

        # plot smoothed line
        gaussian = emotion.rolling(window=50, win_type='gaussian', center=True, min_periods=1).mean(std = 2)
        ax.plot(df['date_created'], gaussian, color = palette[i], label = emotions[i], alpha=1)

        ax = plot_days(ax, text=False)

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(date_form)
    # turn xticks 90 degrees
    plt.setp(ax.get_xticklabels(), rotation=90, ha='center')
    ax.legend()

    if not normalize:
        save_path = os.path.join('fig', 'emotions.png')
    else:
        save_path = os.path.join('fig', 'emotions_normalized.png')
    
    plt.savefig(save_path)


def plot_fluxus(df, figsize=(10, 10), filename='fluxus.png'):
    """
    Plots transience, novelty and resonance
    """
    fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=True)

    date_form = mdates.DateFormatter("%b-%Y")
    #sort by date
    df = df.sort_values(by='date')

    for i, ax in enumerate(axes.flatten()):
        ax.plot(df['date'], df.iloc[:, 2+i], color = palette[3+i], alpha=0.3)

        # plot smoothed line
        gaussian = df.iloc[:, 2+i].rolling(window=20, win_type='gaussian', center=True, min_periods=1).mean(std = 1)
        ax.plot(df['date'], gaussian, color = palette[3+i], alpha=1)

        ax = plot_days(ax, text=False)

        ax.xaxis_date()
        ax.xaxis.set_major_formatter(date_form)
        ax.set_title(df.columns[2+i].capitalize())



    plt.savefig(os.path.join('fig', filename))


def plot_number_of_tweets_per_day(df):
    """Plots the number of tweets per day
    """
    df['date_created'] = pd.to_datetime(df['date_created'])
    df['date_created'] = df['date_created'].dt.date
    df['date_created'] = pd.to_datetime(df['date_created'])
    df['date_created'].value_counts().sort_index().plot()



if __name__ == '__main__':
    df = pd.read_csv(os.path.join('data', 'preprocessed', 'dk_pol_data_emotions.csv'))
    df['date_created'] = pd.to_datetime(df['date_created'])

    df = df.dropna(subset=['date_created'])
    df['date_created'] = pd.to_datetime(df['date_created'], utc=True).dt.strftime("%Y-%m-%d")


    # create a new dataframe with the average emotions per day
    df = df.groupby('date_created').mean().reset_index()

    plot_all_grid(df, normalize=True)
    plot_all_grid(df, normalize=False)

    plot_emotions(df, normalize=True)
    plot_emotions(df, normalize=False)

    df_fluxus_date = pd.read_csv(os.path.join('data', 'idmdl', 'emotions_summarised_date_W3.csv'))
    df_fluxus_date['date'] = pd.to_datetime(df_fluxus_date['date'])
    plot_fluxus(df_fluxus_date)

    

    #df_fluxus_hour = pd.read_csv(os.path.join('data', 'idmdl', 'emotions_summarized_date_hour_W3.csv'))
    #df_fluxus_hour['date_created'] = pd.to_datetime(df_fluxus_hour['date_created'])
    #plot_fluxus(df_fluxus_hour, filename='fluxus_hour.png')


