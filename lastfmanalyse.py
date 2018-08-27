import matplotlib.font_manager as fm
import pandas as pd, numpy as np, string, re, pytz
import matplotlib.pyplot as plt
from datetime import datetime as dt


class GraphSettings:
    def __init__(self):
        family = 'sans-serif'
        self.title_font = fm.FontProperties(family=family, style='normal', size=20, weight='normal', stretch='normal')
        self.label_font = fm.FontProperties(family=family, style='normal', size=16, weight='normal', stretch='normal')
        self.ticks_font = fm.FontProperties(family=family, style='normal', size=12, weight='normal', stretch='normal')
        self.ticks_font_h = fm.FontProperties(family=family, style='normal', size=10.5, weight='normal', stretch='normal')


def analyse_top_artists(graph_settings):
    top_artists = pd.read_csv('data/lastfm_top_artists.csv', encoding='utf-8')
    top_artists = top_artists.set_index('artist')['play_count'].head(20)
    ax = top_artists.plot(kind='bar', figsize=[11, 7], width=0.8, alpha=0.8, color='#ce6c31', edgecolor=None, zorder=2)
    ax.yaxis.grid(True)
    ax.set_xticklabels(top_artists.index, rotation=45, rotation_mode='anchor', ha='right', fontproperties=graph_settings.ticks_font)
    ax.set_title('Top Artists', fontproperties=graph_settings.title_font)
    ax.set_xlabel('', fontproperties=graph_settings.label_font)
    for label in ax.get_yticklabels():
        label.set_fontproperties(graph_settings.ticks_font)
    ax.set_ylabel('Number of plays', fontproperties=graph_settings.label_font)
    plt.savefig('images/lastfm-artists-played-most.png', bbox_inches='tight', dpi=100)
    plt.show()


def make_label(row, maxlength=30, suffix='...'):
    artist = row['artist']
    track = row['track']
    if len(track) > maxlength:
        track = '{}{}'.format(track[:maxlength-len(suffix)], suffix)
    return '{}\n{}'.format(artist, track)

def analyse_top_tracks(graph_settings):
    top_tracks = pd.read_csv('data/lastfm_top_tracks.csv', encoding='utf-8')

    index = top_tracks.apply(make_label, axis='columns')
    tracks_most = top_tracks.set_index(index).drop(labels=['artist', 'track'], axis='columns')
    tracks_most = tracks_most['play_count'].head(20)
    tracks_most.head()
    print(tracks_most)

    ax = tracks_most.sort_values().plot(kind='barh', figsize=[6, 10], width=0.8, alpha=0.6, color='#ce6c31', edgecolor=None, zorder=2)
    ax.xaxis.grid(True)
    ax.set_title('Top tracks', fontproperties=graph_settings.title_font)
    ax.set_xlabel('', fontproperties=graph_settings.label_font)
    ax.set_ylabel('Track', fontproperties=graph_settings.label_font)
    ax.set_xlabel('Playcount', fontproperties=graph_settings.label_font)
    plt.savefig('images/lastfm-tracks-played-most.png', bbox_inches='tight', dpi=100)
    plt.show()


def main():
    graph_settings = GraphSettings()
    #analyse_top_artists(graph_settings)
    analyse_top_tracks(graph_settings)


if __name__ == "__main__":
    main()