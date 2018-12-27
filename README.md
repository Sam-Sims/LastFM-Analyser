# LastFM-Analyser
![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)

Scrapes lastFM to visualise your music tastes. The program has the ability to generate graphs based on your top artists, albums and songs.

## Main Features

* Retrieves your top artists, albums and tracks from lastFM and stored them in a easy to read CSV file.
* Retrieves all your scrobbles and stores them in an easy to read CSV file.
* Visulises the data, by plotting graphs of your top tracks, albums and artists.


## Installing

Ensure Python 3.7 is installed and up to date.

The program will create the required directories if they do not already exist.

Install dependencies.

```
pip install -r requirements.txt
```

Fill in the config file with your API keys,

```
API key for lastFM can be found here: https://www.last.fm/api
API keys for discogs can be found here: https://www.discogs.com/developers/
```

## Usage

Run the lastfm Downloader first to create the CSV files of your music data, stored in \data.

`python lastfmdownloader.py`

Run the analyser to create the graphs, stored in \images.

`python lastfmanalyse.py`

