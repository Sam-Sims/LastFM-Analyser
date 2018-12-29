import os
from configparser import ConfigParser
from scripts import lastfmdownloader as lfmd
from scripts import lastfmanalyser as lfma


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


def run_downloader(config):
    if config.scrape_genre_data == '1':
        print('Retrieving genre data...')
        if config.use_lastfm_tags == '0':
            df = lfmd.get_tracks_genre_discog(lfmd.get_top_tracks(config.last_fm_username, config.last_fm_api_key, config.last_fm_limit, config.last_fm_extended, config.last_fm_page), config.discog_scrape_mode, config.discogs_api_key, config.discogs_api_secret_key, config.wait_time)
            lfmd.write_csv(df, 'data\last-fm-top-tracks.csv')
        elif config.use_lastfm_tags == '1':
            print('Genre data will not be retrieved')
            df = lfmd.get_tracks_genre_lastfm(lfmd.get_top_tracks(config.last_fm_username, config.last_fm_api_key, config.last_fm_limit, config.last_fm_extended, config.last_fm_page), config.last_fm_api_key)
            lfmd.write_csv(df, 'data\last-fm-top-tracks.csv')
        else:
            print("Set last_fm_tag_data to a value")
    elif config.scrape_genre_data == '0':
        df = lfmd.get_top_tracks(config.last_fm_username, config.last_fm_api_key, config.last_fm_limit, config.last_fm_extended, config.last_fm_page)
        lfmd.write_csv(df, 'data\last-fm-top-tracks.csv')
    df = lfmd.get_top_artists(config.last_fm_username, config.last_fm_api_key, config.last_fm_limit, config.last_fm_extended, config.last_fm_page)
    lfmd.write_csv(df, 'data\last-fm-top-artists.csv')
    df = lfmd.get_top_albums(config.last_fm_username, config.last_fm_api_key, config.last_fm_limit, config.last_fm_extended, config.last_fm_page)
    lfmd.write_csv(df, 'data\last-fm-top-albums.csv')
    df = lfmd.get_all_scrobbles(config.last_fm_username, config.last_fm_api_key, config.last_fm_limit, config.last_fm_extended, config.last_fm_page)
    lfmd.write_csv(df, 'data\last-fm-all-songs.csv')


def run_analyser():
    graph_settings = lfma.GraphSettings()
    lfma.analyse_all(graph_settings)


def check_directories():
    path = os.getcwd()
    if not os.path.exists(path + '\images'):
        print('Images directory does not exist! Attempting to create directory...')
        _path = path + '\images'
        os.makedirs(_path, exist_ok=True)
        print('Images directory created successfully!')
    if not os.path.exists(path + '\data'):
        print('Data directory does not exist! Attempting to create directory...')
        _path = path + '\data'
        os.makedirs(_path, exist_ok=True)
        print('Data directory created successfully!')

def check_menu_choice(ans, config):
    try:
        if ans == '1':
            run_downloader(config)
        elif ans == '2':
            run_analyser()
        elif ans == '3':
            print('Place Holder')
        elif ans == '4':
            print('Place Holder')
        else:
            print('Error, an answer was not supplied!')
    except Exception as e:
        print('An error occurred' + e)


def print_main_menu():
    print('''\

    ---------------------------------------------------------------------------------

      _               _   ______ __  __                        _                     
     | |             | | |  ____|  \/  |     /\               | |                    
     | |     __ _ ___| |_| |__  | \  / |    /  \   _ __   __ _| |_   _ ___  ___ _ __ 
     | |    / _` / __| __|  __| | |\/| |   / /\ \ | '_ \ / _` | | | | / __|/ _ \ '__|
     | |___| (_| \__ \ |_| |    | |  | |  / ____ \| | | | (_| | | |_| \__ \  __/ |   
     |______\__,_|___/\__|_|    |_|  |_| /_/    \_\_| |_|\__,_|_|\__, |___/\___|_|   
                                                                  __/ |              
                                                                 |___/               

    ---------------------------------------------------------------------------------
     ''')
    print('Please make a selection:')
    print('1: Download Data')
    print('2: Generate Graphs')
    print('3: Generate Report')
    print('4: Verify Config')

def main():
    config = Config()
    print_main_menu()
    ans = input()
    check_directories()
    check_menu_choice(ans, config)


if __name__ == "__main__":
    main()