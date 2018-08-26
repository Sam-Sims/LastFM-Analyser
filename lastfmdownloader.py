import requests, json, time, pandas as pd

# Global API params (lastFM)
key = '0166716913bb82626c0e18402c46df62'
username = 'sam_sims'
url_to_format = 'https://ws.audioscrobbler.com/2.0/?method=user.get{}&user={}&api_key={}&limit={}&extended={}&page={}&format=json'
limit = 200  # Number of records per call (200 is max)
extended = 0  # api lets you retrieve extended data for each track, 0=no, 1=yes
page = 1  # page of results to start retrieving at

# Scraper Settings
mode = 'q'  # mode = q then run search query; mode = s then run specifc query (doesnt find genre sometimes)
last_fm_tag_data = 0  # 0 = use discogs genre; 1 = use lastFM tags
genre_data = 0

# Global API params (discogs)
key_discogs = 'EikgARuUWOIlzrvqOVDI'
secret_key_discogs = 'TqQwfsFbyisrVnUscTMPpRnVphvaBbtf'


def get_top_tracks():
    method = 'toptracks'
    request_url = url_to_format.format(method, username, key, limit, extended, page)
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
    return top_tracks


#  This is only run if last_fm_tag_data is set to 1 - time consuming, discog API is prefered
def get_tracks_genre_lastfm():
    local_top_tracks = get_top_tracks()
    tag_url_to_format = 'https://ws.audioscrobbler.com/2.0/?method=track.get{}&artist={}&track={}&autocorrect={}&api_key={}&format=json'
    method = 'info'
    autocorrect = '1'  # Transform misspelled artist and track names into correct artist and track names
    tags_spliced = []
    for index, row in local_top_tracks.iterrows():
        artist = row['artist']
        track = row['track']
        request_url = tag_url_to_format.format(method, artist, track, autocorrect, key)
        response = requests.get(request_url).json()
        print('Processing tag data: ', artist, ' - ', track)
        tags = []
        for item in response['track']['toptags']['tag']:
            tags.append(item['name'])
        tags_spliced.append(tags[:3])
    local_top_tracks['Tags'] = tags_spliced
    return local_top_tracks


def get_tracks_genre_discog():
    if mode == 'q':
        local_top_tracks = get_top_tracks()
        discogs_url_to_format = 'https://api.discogs.com/database/search?q={}&per_page=5&page=1&key={}&secret={}'
        genres = []
        for index, row in local_top_tracks.iterrows():
            artist = row['artist']
            track = row['track']
            search = artist + ' ' + track
            request_url = discogs_url_to_format.format(search, key_discogs, secret_key_discogs)
            response = requests.get(request_url).json()
            time.sleep(1)
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
        local_top_tracks['Genre'] = genres
        return local_top_tracks
    elif mode == 's':
        local_top_tracks = get_top_tracks()
        discogs_url_to_format = 'https://api.discogs.com/database/search?track={}&artist={}&per_page=5&page=1&key={}&secret={}'
        genres = []
        for index, row in local_top_tracks.iterrows():
            artist = row['artist']
            track = row['track']
            request_url = discogs_url_to_format.format(track, artist, key_discogs, secret_key_discogs)
            response = requests.get(request_url).json()
            print('Processing genre data: ', artist, ' - ', track)
            genres_temp = []
            for item in response['results']:
                genres_temp.append(item['style'])
            genres.append(genres_temp[:1])
        local_top_tracks['Genre'] = genres
        return local_top_tracks
    else:
        print("Error")


def get_top_artists():
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
    return top_artists

def get_top_albums():
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
    return top_albums


def output_data():
    if genre_data:
        if last_fm_tag_data == 0:
            get_tracks_genre_discog().to_csv('data/lastfm_top_tracks.csv', index=None, encoding='utf-8')
        elif last_fm_tag_data == 1:
            get_tracks_genre_lastfm().to_csv('data/lastfm_top_tracks.csv', index=None, encoding='utf-8')
        else:
            print("Set last_fm_tag_data to a value")
    elif genre_data == False:
        get_top_tracks().to_csv('data/lastfm_top_tracks.csv', index=None, encoding='utf8')
    get_top_artists().to_csv('data/lastfm_top_artists.csv', index=None, encoding='utf-8')
    get_top_albums().to_csv('data/lastfm_top_albums.csv', index=None, encoding='utf-8')


def main():
    output_data()

if __name__ == "__main__":
    main()
