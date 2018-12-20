import requests, json, time, pandas as pd
from configparser import ConfigParser

# Global request url for lastFM API that can be manipulated
url_to_format = 'https://ws.audioscrobbler.com/2.0/?method=user.get{}&user={}&api_key={}&limit={}&extended={}&page={}&format=json'


class Config:
    # Reads the config file, to be created as a config object, allowing parameters to be read E.g (config.last_fm_api_key)
    def __init__(self):
        config = ConfigParser()
        config.read('config.ini')
        print('Config Loaded!')
        #  LastFM config
        self.last_fm_api_key = config.get('LASTFM_API_CONFIGURATION', 'api_key')
        self.last_fm_username = config.get('LASTFM_API_CONFIGURATION', 'username')
        self.last_fm_limit = config.get('LASTFM_API_CONFIGURATION', 'limit')
        self.last_fm_extended = config.get('LASTFM_API_CONFIGURATION', 'extended')
        self.last_fm_page = config.get('LASTFM_API_CONFIGURATION', 'page')

        #  Discogs config
        self.discogs_api_key = config.get('DISCOGS_API_CONFIGURATION', 'api_key')
        self.discogs_api_secret_key = config.get('DISCOGS_API_CONFIGURATION', 'api_secret_key')

        #  Scraping settings
        self.scrape_genre_data = config.get('SCRAPING_SETTINGS', 'scrape_genre_data')
        self.wait_time = config.get('SCRAPING_SETTINGS', 'wait_time')
        self.use_lastfm_tags = config.get('SCRAPING_SETTINGS', 'use_lastfm_tags')
        self.discog_scrape_mode = config.get('SCRAPING_SETTINGS', 'discogs_scrape_mode')


def get_top_tracks(username, api_key, limit, extended, page):
    print('Retrieving top tracks...')
    method = 'toptracks'
    request_url = url_to_format.format(method, username, api_key, limit, extended, page)
    artist_names = []
    track_names = []
    play_counts = []
    response = requests.get(request_url).json()
    for item in response[method]['track']:
        artist_names.append(item['artist']['name'])
        track_names.append(item['name'])
        play_counts.append(item['playcount'])
    top_tracks = pd.DataFrame()
    top_tracks['artist'] = artist_names
    top_tracks['track'] = track_names
    top_tracks['play_count'] = play_counts
    print('Done!')
    return top_tracks


#  This is only run if last_fm_tag_data is set to 1 - time consuming, discog API is prefered
def get_tracks_genre_lastfm(_top_tracks, api_key):
    print('Using lastFM tag data')
    tag_url_to_format = 'https://ws.audioscrobbler.com/2.0/?method=track.get{}&artist={}&track={}&autocorrect={}&api_key={}&format=json'
    method = 'info'
    autocorrect = '1'  # Transform misspelled artist and track names into correct artist and track names
    tags_spliced = []
    for index, row in _top_tracks.iterrows():
        artist = row['artist']
        track = row['track']
        request_url = tag_url_to_format.format(method, artist, track, autocorrect, api_key)
        response = requests.get(request_url).json()
        print('Processing tag data: ', artist, ' - ', track)
        tags = []
        for item in response['track']['toptags']['tag']:
            tags.append(item['name'])
        tags_spliced.append(tags[:3])
    _top_tracks['Tags'] = tags_spliced
    print('Done!')
    return _top_tracks


def get_tracks_genre_discog(_top_tracks, discog_scape_mode, key_discog, secret_key_discog, wait_time):
    print('Using discogs genre data')
    if discog_scape_mode == 'q':
        discogs_url_to_format = 'https://api.discogs.com/database/search?q={}&per_page=5&page=1&key={}&secret={}'
        genres = []
        for index, row in _top_tracks.iterrows():
            artist = row['artist']
            track = row['track']
            search = artist + ' ' + track
            request_url = discogs_url_to_format.format(search, key_discog, secret_key_discog)
            response = requests.get(request_url).json()
            time.sleep(wait_time)
            print('Processing genre data: ', artist, ' - ', track)

            genres_temp = []
            try:
                for item in response['results']:
                    genres_temp.append(item['style'])
                genres.append(genres_temp[:1])
            except Exception as e:
                print(e)
                genres.append("Error")
                pass
        _top_tracks['Genre'] = genres
        return _top_tracks
    elif discog_scape_mode == 's':
        discogs_url_to_format = 'https://api.discogs.com/database/search?track={}&artist={}&per_page=5&page=1&key={}&secret={}'
        genres = []
        for index, row in _top_tracks.iterrows():
            artist = row['artist']
            track = row['track']
            request_url = discogs_url_to_format.format(track, artist, key_discog, secret_key_discog)
            response = requests.get(request_url).json()
            print('Processing genre data: ', artist, ' - ', track)
            genres_temp = []
            for item in response['results']:
                genres_temp.append(item['style'])
            genres.append(genres_temp[:1])
        _top_tracks['Genre'] = genres
        print('Done!')
        return _top_tracks
    else:
        print("Error")


def get_top_artists(username, key, limit, extended, page):
    print('Retrieving top artists...')
    method = 'topartists'
    request_url = url_to_format.format(method, username, key, limit, extended, page)
    artist_names = []
    play_counts = []
    response = requests.get(request_url).json()
    for item in response[method]['artist']:
        artist_names.append(item['name'])
        play_counts.append(item['playcount'])
    top_artists = pd.DataFrame()
    top_artists['artist'] = artist_names
    top_artists['play_count'] = play_counts
    print('Done!')
    return top_artists


def get_top_albums(username, key, limit, extended, page):
    print('Retrieving top albums...')
    method = 'topalbums'
    request_url = url_to_format.format(method, username, key, limit, extended, page)
    album_names = []
    play_counts = []
    artist_name = []
    response = requests.get(request_url).json()
    for item in response[method]['album']:
        album_names.append(item['name'])
        artist_name.append(item['artist']['name'])
        play_counts.append(item['playcount'])
    top_albums = pd.DataFrame()
    top_albums['albums'] = album_names
    top_albums['artist'] = artist_name
    top_albums['playcount'] = play_counts
    print('Done!')
    return top_albums


def get_all_scrobbles(username, key, limit, extended, page):
    print('Retrieving all scrobbles...')
    method = 'recenttracks'
    request_url = url_to_format.format(method, username, key, limit, extended, page)
    response = requests.get(request_url).json()
    total_pages = response[method]['@attr']['totalPages']
    print(total_pages, ' pages found!')
    big_response = []
    for page_num in range(1, int(total_pages) + 1):  # int(total_pages)
        print('Processing page: ', int(page_num))
        request_url = url_to_format.format(method, username, key, limit, extended, page_num)
        big_response.append(requests.get(request_url).json())
    artist_name = []
    track_name = []
    album_name = []
    date_utc = []
    date_text = []
    for responses in big_response:
        for scrobble in responses[method]['track']:
            if 'date' in scrobble.keys():
                artist_name.append(scrobble['artist']['#text'])
                track_name.append(scrobble['name'])
                album_name.append(scrobble['album']['#text'])
                date_utc.append(scrobble['date']['uts'])
                date_text.append(scrobble['date']['#text'])
    scrobble_data = pd.DataFrame()
    scrobble_data['track'] = track_name
    scrobble_data['album'] = album_name
    scrobble_data['artist'] = artist_name
    scrobble_data['timestamp'] = date_utc
    scrobble_data['text_timestamp'] = date_text

    #scrobble_data['timestamp2'] = pd.to_datetime(scrobble_data['text_timestamp'])
    scrobble_data['text_timestamp'] = pd.to_datetime(scrobble_data['text_timestamp'])
    scrobble_data['year'] = scrobble_data['text_timestamp'].map(lambda x: x.year)
    scrobble_data['month'] = scrobble_data['text_timestamp'].map(lambda x: x.month)
    scrobble_data['day'] = scrobble_data['text_timestamp'].map(lambda x: x.day)
    scrobble_data['hour'] = scrobble_data['text_timestamp'].map(lambda x: x.hour)
    scrobble_data['minute'] = scrobble_data['text_timestamp'].map(lambda x: x.minute)
    print('Done!')
    return scrobble_data


def output_data(config):
    if config.scrape_genre_data == '1':
        print('Retrieving genre data...')
        if config.use_lastfm_tags == '0':
            get_tracks_genre_discog(get_top_tracks(config.last_fm_username, config.last_fm_api_key, config.last_fm_limit, config.last_fm_extended, config.last_fm_page), config.discog_scrape_mode, config.discogs_api_key, config.discogs_api_secret_key, config.wait_time).to_csv('data/lastfm_top_tracks.csv', index=None, encoding='utf-8')
        elif config.use_lastfm_tags == '1':
            print('Genre data will not be retrieved')
            get_tracks_genre_lastfm(get_top_tracks(config.last_fm_username, config.last_fm_api_key, config.last_fm_limit, config.last_fm_extended, config.last_fm_page), config.last_fm_api_key).to_csv('data/lastfm_top_tracks.csv', index=None, encoding='utf-8')
        else:
            print("Set last_fm_tag_data to a value")
    elif config.scrape_genre_data == '0':
        get_top_tracks(config.last_fm_username, config.last_fm_api_key, config.last_fm_limit, config.last_fm_extended, config.last_fm_page).to_csv('data/lastfm_top_tracks.csv', index=None, encoding='utf8')
    get_top_artists(config.last_fm_username, config.last_fm_api_key, config.last_fm_limit, config.last_fm_extended, config.last_fm_page).to_csv('data/lastfm_top_artists.csv', index=None, encoding='utf-8')
    get_top_albums(config.last_fm_username, config.last_fm_api_key, config.last_fm_limit, config.last_fm_extended, config.last_fm_page).to_csv('data/lastfm_top_albums.csv', index=None, encoding='utf-8')
    get_all_scrobbles(config.last_fm_username, config.last_fm_api_key, config.last_fm_limit, config.last_fm_extended,config.last_fm_page).to_csv('data/lastfm_all_scrobbles.csv', index=None, encoding='utf-8')

def main():
    config = Config()
    output_data(config)



if __name__ == "__main__":
    main()
