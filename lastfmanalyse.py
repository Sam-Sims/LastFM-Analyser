import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import AutoMinorLocator


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
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xticklabels(top_artists.index, rotation=45, rotation_mode='anchor', ha='right', fontproperties=graph_settings.ticks_font)
    ax.set_title('Top Artists', fontproperties=graph_settings.title_font)
    ax.set_xlabel('', fontproperties=graph_settings.label_font)
    for label in ax.get_yticklabels():
        label.set_fontproperties(graph_settings.ticks_font)
    ax.set_ylabel('Number of plays', fontproperties=graph_settings.label_font)
    plt.savefig('images/lastfm-artists-played-most.png', bbox_inches='tight', dpi=100)
    plt.show()


def make_label(df, top, bot):
    maxlength = 30
    suffix = '...'
    top_value = df[top]
    bot_value = df[bot]
    if len(bot_value) > maxlength:
        bot_value = '{}{}'.format(bot_value[:maxlength-len(suffix)], suffix)
    return '{}\n{}'.format(top_value, bot_value)


def analyse_top_tracks(graph_settings):
    top_tracks = pd.read_csv('data/lastfm_top_tracks.csv', encoding='utf-8')

    index = top_tracks.apply(make_label, args=('artist', 'track'), axis='columns')
    top_tracks = top_tracks.set_index(index).drop(labels=['artist', 'track'], axis='columns')
    top_tracks = top_tracks['play_count'].head(20)
    top_tracks.head()

    ax = top_tracks.sort_values().plot(kind='barh', figsize=[6, 10], width=0.8, alpha=0.6, color='#ce6c31', edgecolor=None, zorder=2)
    ax.xaxis.grid(True)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.set_title('Top Tracks', fontproperties=graph_settings.title_font)
    ax.set_ylabel('Track', fontproperties=graph_settings.label_font)
    ax.set_xlabel('Playcount', fontproperties=graph_settings.label_font)
    plt.savefig('images/lastfm-tracks-played-most.png', bbox_inches='tight', dpi=100)
    plt.show()


def analyse_top_albums(graph_settings):
    top_albums = pd.read_csv('data/lastfm_top_albums.csv', encoding='utf-8')
    print(top_albums)
    index = top_albums.apply(make_label, args=('artist', 'albums'), axis='columns')
    top_albums = top_albums.set_index(index).drop(labels=['artist', 'albums'], axis='columns')
    top_albums = top_albums['playcount'].head(20)
    top_albums.head()
    print(top_albums)
    ax = top_albums.sort_values().plot(kind='barh', figsize=[6, 10], width=0.8, alpha=0.6, color='#ce6c31', edgecolor=None, zorder=2)

    ax.xaxis.grid(True)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.set_title('Top Albums', fontproperties=graph_settings.title_font)
    ax.set_ylabel('Album', fontproperties=graph_settings.label_font)
    ax.set_xlabel('Playcount', fontproperties=graph_settings.label_font)
    plt.savefig('images/lastfm-albums-played-most.png', bbox_inches='tight', dpi=100)
    plt.show()


def tracks_by_month(graph_settings):
    scrobbles = pd.read_csv('data/lastfm_all_scrobbles.csv', encoding='utf-8')
    month_counts = scrobbles['month'].value_counts().sort_index()
    months = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
    df = pd.DataFrame(list(dict(zip(months, month_counts)).items()), columns=['Month', 'Count'])
    ax = df.plot(kind='line', figsize=[10, 5], linewidth=4, alpha=1, marker='o', color='#ce6c31', markerfacecolor='w', markersize=8, markeredgewidth=2)
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    ax.set_xticklabels(df.Month)
    ax.set_xticks(df.index)
    ax.set_title('Total song plays in 2018', fontproperties=graph_settings.title_font)
    ax.set_ylabel('Song Plays', fontproperties=graph_settings.label_font)
    plt.savefig('images/lastfm-songs-per-month.png', bbox_inches='tight', dpi=100)
    plt.show()


def tracks_by_days_week(graph_settings):
    scrobbles = scrobbles = pd.read_csv('data/lastfm_all_scrobbles.csv', encoding='utf-8')
    scrobbles['text_timestamp'] = pd.to_datetime(scrobbles['text_timestamp'])
    scrobbles['dow'] = scrobbles['text_timestamp'].map(lambda x: x.weekday())
    day_counts = scrobbles['dow'].value_counts().sort_index()
    day_counts.index = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    ax = day_counts.plot(kind='bar', figsize=[11, 7], width=0.8, alpha=0.8, color='#ce6c31', edgecolor=None, zorder=2)
    ax.yaxis.grid(True)
    ax.set_title('Total song plays vs Day of week they were played at', fontproperties=graph_settings.title_font)
    ax.set_ylabel('Song Plays', fontproperties=graph_settings.label_font)
    plt.savefig('images/lastfm-songs-per-weekday.png', bbox_inches='tight', dpi=100)
    plt.show()


def tracks_by_hour(graph_settings):
    scrobbles = pd.read_csv('data/lastfm_all_scrobbles.csv', encoding='utf-8')
    hour_counts = scrobbles['hour'].value_counts().sort_index()
    ax = hour_counts.plot(kind='line', figsize=[10, 5], linewidth=4, alpha=1, marker='o', color='#ce6c31', markerfacecolor='w', markersize=8, markeredgewidth=2)
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    ticklabels = ['%s:00' % i for i in range(24)]
    ax.set_xticks(hour_counts.index)
    ax.set_xticklabels(ticklabels, rotation=45)

    ax.set_title('Total song plays vs Hours they were played at', fontproperties=graph_settings.title_font)
    ax.set_ylabel('Song Plays', fontproperties=graph_settings.label_font)
    ax.set_xlabel('Hour', fontproperties=graph_settings.label_font)
    plt.savefig('images/lastfm-songs-per-hour.png', bbox_inches='tight', dpi=100)
    plt.show()

def main():
    graph_settings = GraphSettings()
    #analyse_top_artists(graph_settings)
    #analyse_top_albums(graph_settings)
    #analyse_top_tracks(graph_settings)
    #tracks_by_month(graph_settings, '2018')
    #tracks_by_month(graph_settings)
    #tracks_by_days_week(graph_settings)
    tracks_by_hour(graph_settings)


if __name__ == "__main__":
    main()