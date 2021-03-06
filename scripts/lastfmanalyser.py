import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import AutoMinorLocator
import matplotlib.font_manager as fm
import os
import calendar
import sys

class GraphSettings:
    def __init__(self):
        family = 'sans-serif'
        self.title_font = fm.FontProperties(family=family, style='normal', size=20, weight='normal', stretch='normal')
        self.label_font = fm.FontProperties(family=family, style='normal', size=16, weight='normal', stretch='normal')
        self.ticks_font = fm.FontProperties(family=family, style='normal', size=12, weight='normal', stretch='normal')
        self.ticks_font_h = fm.FontProperties(family=family, style='normal', size=10.5, weight='normal',
                                              stretch='normal')


class GraphGeneratorForGivenMonth: #Generates Graph using every month from every year
    def __init__(self, month):
        self.scrobbles = pd.read_csv('data/last-fm-all-songs.csv', encoding='utf-8')
        self.month = month
        self.graph_settings = GraphSettings()
        self.month_name = calendar.month_name[self.month]
        path = os.getcwd() + '\images'
        if not os.path.exists(path + '\\' + self.month_name):
            print(self.month_name + ' Directory does not exist! Attempting to create directory...')
            _path = path + '\\' + self.month_name
            os.makedirs(_path, exist_ok=True)
            print('Directory created successfully!')
        self.path_to_use = path + '\\' + self.month_name + '\\'

    def tracks_by_hour(self):
        _scrobbles = self.scrobbles.query('month == ' + str(self.month))
        hour_counts = _scrobbles['hour'].value_counts().sort_index()
        new_index = list(range(0, 24))
        hour_counts_reindex = hour_counts.reindex(new_index, fill_value=0)
        ax = hour_counts_reindex.plot(kind='line', figsize=[10, 5], linewidth=4, alpha=1, marker='o', color='#ce6c31',
                                      markerfacecolor='w', markersize=8, markeredgewidth=2)
        ax.yaxis.grid(True)
        ax.xaxis.grid(True)
        ticklabels = ['%s:00' % i for i in range(24)]
        ax.set_xticks(hour_counts_reindex.index)
        ax.set_xticklabels(ticklabels, rotation=45)
        ax.set_title('Total song plays vs Time for the month of ' + str(self.month_name),
                     fontproperties=self.graph_settings.title_font)
        ax.set_ylabel('Song Plays', fontproperties=self.graph_settings.label_font)
        ax.set_xlabel('Hour', fontproperties=self.graph_settings.label_font)
        plt.savefig(self.path_to_use + 'lastfm-songs-per-hour_for_month of ' + self.month_name + '.png',
                    bbox_inches='tight', dpi=100)
        plt.close()

    def tracks_by_days_week(self):
        _scrobbles = self.scrobbles.query('month == ' + str(self.month))
        _scrobbles['text_timestamp'] = pd.to_datetime(_scrobbles['text_timestamp'])
        _scrobbles['dow'] = _scrobbles['text_timestamp'].map(lambda x: x.weekday())
        hour_counts = _scrobbles['dow'].value_counts().sort_index()
        days = 'Mon Tue Wed Thu Fri Sat Sun'.split()
        df = pd.DataFrame(list(dict(zip(days, hour_counts)).items()), columns=['Month', 'Count'])
        ax = df.plot(kind='bar', figsize=[11, 7], width=0.8, alpha=0.8, color='#ce6c31', edgecolor=None,
                     zorder=2)
        ax.yaxis.grid(True)
        ax.set_xticklabels(df.Month)
        ax.set_xticks(df.index)
        ax.set_title('Total song plays vs Day of week for the month of ' + self.month_name,
                     fontproperties=self.graph_settings.title_font)
        ax.set_ylabel('Song Plays', fontproperties=self.graph_settings.label_font)
        plt.savefig(self.path_to_use + 'lastfm-songs-per-weekday_for_month of ' + self.month_name + '.png',
                    bbox_inches='tight', dpi=100)
        plt.close()


class GraphGeneratorForAllTime:
    def __init__(self):
        self.scrobbles = pd.read_csv('data/last-fm-all-songs.csv', encoding='utf-8')
        self.graph_settings = GraphSettings()
        path = os.getcwd() + '\images\\All time'
        if not os.path.exists(path):
            print('Images directory does not exist! Aborting!')
            sys.exit("Images folder not found!")
        path = os.getcwd()
        if not os.path.exists(path + '\images'):
            print('Images directory does not exist! Aborting!')
            sys.exit("Images folder not found!")

    def all_time_top_artists(self):
        top_artists = pd.read_csv('data/last-fm-top-artists.csv', encoding='utf-8')
        top_artists = top_artists.set_index('artist')['play_count'].head(20)
        ax = top_artists.plot(kind='bar', figsize=[11, 7], width=0.8, alpha=0.8, color='#ce6c31', edgecolor=None,
                              zorder=2)
        ax.yaxis.grid(True)
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.set_xticklabels(top_artists.index, rotation=45, rotation_mode='anchor', ha='right',
                           fontproperties=self.graph_settings.ticks_font)
        ax.set_title('Top Artists', fontproperties=self.graph_settings.title_font)
        ax.set_xlabel('', fontproperties=self.graph_settings.label_font)
        for label in ax.get_yticklabels():
            label.set_fontproperties(self.graph_settings.ticks_font)
        ax.set_ylabel('Number of plays', fontproperties=self.graph_settings.label_font)
        plt.savefig('images/All time/lastfm-artists-played-most.png', bbox_inches='tight', dpi=100)
        plt.close()

    def all_time_top_tracks(self):
        top_tracks = pd.read_csv('data/last-fm-top-tracks.csv', encoding='utf-8')
        index = top_tracks.apply(make_label, args=('artist', 'track'), axis='columns')
        top_tracks = top_tracks.set_index(index).drop(labels=['artist', 'track'], axis='columns')
        top_tracks = top_tracks['play_count'].head(20)
        top_tracks.head()
        ax = top_tracks.sort_values().plot(kind='barh', figsize=[6, 10], width=0.8, alpha=0.6, color='#ce6c31',
                                           edgecolor=None, zorder=2)
        ax.xaxis.grid(True)
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.set_title('Top Tracks', fontproperties=self.graph_settings.title_font)
        ax.set_ylabel('Track', fontproperties=self.graph_settings.label_font)
        ax.set_xlabel('Playcount', fontproperties=self.graph_settings.label_font)
        plt.savefig('images/All time/lastfm-tracks-played-most.png', bbox_inches='tight', dpi=100)
        plt.close()

    def all_time_top_albums(self):
        top_albums = pd.read_csv('data/last-fm-top-albums.csv', encoding='utf-8')
        index = top_albums.apply(make_label, args=('artist', 'albums'), axis='columns')
        top_albums = top_albums.set_index(index).drop(labels=['artist', 'albums'], axis='columns')
        top_albums = top_albums['playcount'].head(20)
        top_albums.head()
        ax = top_albums.sort_values().plot(kind='barh', figsize=[6, 10], width=0.8, alpha=0.6, color='#ce6c31',
                                           edgecolor=None, zorder=2)
        ax.xaxis.grid(True)
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.set_title('Top Albums', fontproperties=self.graph_settings.title_font)
        ax.set_ylabel('Album', fontproperties=self.graph_settings.label_font)
        ax.set_xlabel('Playcount', fontproperties=self.graph_settings.label_font)
        plt.savefig('images/All time/lastfm-albums-played-most.png', bbox_inches='tight', dpi=100)
        plt.close()


    def total_song_plays_each_month(self):
        _scrobbles = self.scrobbles
        month_counts = _scrobbles['month'].value_counts().sort_index()
        months = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
        df = pd.DataFrame(list(dict(zip(months, month_counts)).items()), columns=['Month', 'Count'])
        ax = df.plot(kind='line', figsize=[10, 5], linewidth=4, alpha=1, marker='o', color='#ce6c31',
                     markerfacecolor='w',
                     markersize=8, markeredgewidth=2)
        ax.yaxis.grid(True)
        ax.xaxis.grid(True)
        ax.set_xticklabels(df.Month)
        ax.set_xticks(df.index)
        ax.set_title('Total song plays in 2018', fontproperties=self.graph_settings.title_font)
        ax.set_ylabel('Song Plays', fontproperties=self.graph_settings.label_font)
        plt.savefig('images/All time/lastfm-songs-per-month.png', bbox_inches='tight', dpi=100)
        plt.close()

    def all_time_song_plays_each_dayofweek(self):
        _scrobbles =self.scrobbles
        _scrobbles['text_timestamp'] = pd.to_datetime(_scrobbles['text_timestamp'])
        _scrobbles['dow'] = _scrobbles['text_timestamp'].map(lambda x: x.weekday())
        day_counts = _scrobbles['dow'].value_counts().sort_index()
        day_counts.index = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        ax = day_counts.plot(kind='bar', figsize=[11, 7], width=0.8, alpha=0.8, color='#ce6c31', edgecolor=None,
                             zorder=2)
        ax.yaxis.grid(True)
        ax.set_title('Total song plays vs Day of week they were played at', fontproperties=self.graph_settings.title_font)
        ax.set_ylabel('Song Plays', fontproperties=self.graph_settings.label_font)
        plt.savefig('images/All time/lastfm-songs-per-weekday.png', bbox_inches='tight', dpi=100)
        plt.close()


    def total_song_plays_each_hour(self):
        _scrobbles = self.scrobbles
        hour_counts = _scrobbles['hour'].value_counts().sort_index()
        ax = hour_counts.plot(kind='line', figsize=[10, 5], linewidth=4, alpha=1, marker='o', color='#ce6c31',
                              markerfacecolor='w', markersize=8, markeredgewidth=2)
        ax.yaxis.grid(True)
        ax.xaxis.grid(True)
        ticklabels = ['%s:00' % i for i in range(24)]
        ax.set_xticks(hour_counts.index)
        ax.set_xticklabels(ticklabels, rotation=45)
        ax.set_title('Total song plays vs Hours they were played at', fontproperties=self.graph_settings.title_font)
        ax.set_ylabel('Song Plays', fontproperties=self.graph_settings.label_font)
        ax.set_xlabel('Hour', fontproperties=self.graph_settings.label_font)
        plt.savefig('images/All time/lastfm-songs-per-hour.png', bbox_inches='tight', dpi=100)
        plt.close()


    def analyse_all(self):
        self.all_time_top_albums()
        self.all_time_top_artists()
        self.all_time_top_tracks()
        self.all_time_song_plays_each_dayofweek()
        self.total_song_plays_each_hour()
        self.total_song_plays_each_month()


def make_label(df, top, bot):
    maxlength = 30
    suffix = '...'
    top_value = df[top]
    bot_value = df[bot]
    if len(bot_value) > maxlength:
        bot_value = '{}{}'.format(bot_value[:maxlength - len(suffix)], suffix)
    return '{}\n{}'.format(top_value, bot_value)

class GraphGeneratorForYear:
    def __init__(self, year):
        self.scrobbles = pd.read_csv('data/last-fm-all-songs.csv', encoding='utf-8')
        self.year = year
        self.graph_settings = GraphSettings()
        path = os.getcwd() + '\images'
        if not os.path.exists(path + '\\' + self.year):
            print(self.year + ' Directory does not exist! Attempting to create directory...')
            _path = path + '\\' + self.year
            os.makedirs(_path, exist_ok=True)
            print('Directory created successfully!')
        self.path_to_use = path + '\\' + self.year + '\\'

    def work_top_artists(self):
        _scrobbles = self.scrobbles.query('year == ' + str(self.year))
        value_counts = _scrobbles['artist'].value_counts()
        _scrobbles = value_counts.rename_axis('artist').reset_index(name='play_count')

        top_artists = _scrobbles.set_index('artist')['play_count'].head(20)
        ax = top_artists.plot(kind='bar', figsize=[11, 7], width=0.8, alpha=0.8, color='#ce6c31', edgecolor=None,
                              zorder=2)
        ax.yaxis.grid(True)
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.set_xticklabels(top_artists.index, rotation=45, rotation_mode='anchor', ha='right',
                           fontproperties=self.graph_settings.ticks_font)
        ax.set_title('Top Artists', fontproperties=self.graph_settings.title_font)
        ax.set_xlabel('', fontproperties=self.graph_settings.label_font)
        for label in ax.get_yticklabels():
            label.set_fontproperties(self.graph_settings.ticks_font)
        ax.set_ylabel('Number of plays', fontproperties=self.graph_settings.label_font)
        plt.savefig(self.path_to_use + 'lastfm-artists-played-most for year of ' + self.year + '.png',
                    bbox_inches='tight', dpi=100)
        plt.close()

    def work_time_top_tracks(self):
        _scrobbles = self.scrobbles.query('year == ' + str(self.year))
        value_counts = _scrobbles['track'].value_counts()
        print(value_counts)
        _scrobbles = value_counts.rename_axis('track').reset_index(name='play_count')

        top_tracks = _scrobbles.set_index('track')['play_count'].head(20)
        ax = top_tracks.plot(kind='bar', figsize=[11, 7], width=0.8, alpha=0.8, color='#ce6c31', edgecolor=None,
                              zorder=2)
        ax.yaxis.grid(True)
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.set_xticklabels(top_tracks.index, rotation=45, rotation_mode='anchor', ha='right',
                           fontproperties=self.graph_settings.ticks_font)
        ax.set_title('Top Artists', fontproperties=self.graph_settings.title_font)
        ax.set_xlabel('', fontproperties=self.graph_settings.label_font)
        for label in ax.get_yticklabels():
            label.set_fontproperties(self.graph_settings.ticks_font)
        ax.set_ylabel('Number of plays', fontproperties=self.graph_settings.label_font)
        plt.savefig(self.path_to_use + 'lastfm-tracks-played-most for year of ' + self.year + '.png',
                    bbox_inches='tight', dpi=100)
        plt.close()

    def work_time_top_albums(self):
        _scrobbles = self.scrobbles.query('year == ' + str(self.year))
        value_counts = _scrobbles['album'].value_counts()
        print(value_counts)
        _scrobbles = value_counts.rename_axis('album').reset_index(name='play_count')

        top_albums = _scrobbles.set_index('album')['play_count'].head(20)
        ax = top_albums.plot(kind='bar', figsize=[11, 7], width=0.8, alpha=0.8, color='#ce6c31', edgecolor=None,
                              zorder=2)
        ax.yaxis.grid(True)
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.set_xticklabels(top_albums.index, rotation=45, rotation_mode='anchor', ha='right',
                           fontproperties=self.graph_settings.ticks_font)
        ax.set_title('Top Artists', fontproperties=self.graph_settings.title_font)
        ax.set_xlabel('', fontproperties=self.graph_settings.label_font)
        for label in ax.get_yticklabels():
            label.set_fontproperties(self.graph_settings.ticks_font)
        ax.set_ylabel('Number of plays', fontproperties=self.graph_settings.label_font)
        plt.savefig(self.path_to_use + 'lastfm-albums-played-most for year of ' + self.year + '.png',
                    bbox_inches='tight', dpi=100)
        plt.close()

def workout_years():
    scrobbles = pd.read_csv('data/last-fm-all-songs.csv', encoding='utf-8')
    year_list = scrobbles['year'].unique().tolist()
    year_list = list(map(str, year_list))
    return year_list


def analyse_all(graph_settings):
    for i in range(len(workout_years())):
        graph_gen = GraphGeneratorForYear(workout_years()[i])
        graph_gen.work_top_artists()
        graph_gen.work_time_top_tracks()
        graph_gen.work_time_top_albums()

    graph_generator_all_time = GraphGeneratorForAllTime()
    graph_generator_all_time.analyse_all()
    #for x in range(1, 13):
        #graph_generator_given_month = GraphGeneratorForGivenMonth(x)
        #graph_generator_given_month.tracks_by_days_week()
        #graph_generator_given_month.tracks_by_hour()


def main():
    print('This should be imported as a module')


if __name__ == "__main__":
    main()
