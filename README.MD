
# Spotify Flight Playlist Creator

This Python script automates downloading songs from Spotify playlists. It extracts song titles and artists from a Spotify playlist, searches YouTube for corresponding videos, and downloads them as MP3 files.

## Features

- Extracts song information from Spotify playlists
- Downloads songs from YouTube based on playlist data
- Saves downloaded songs as MP3 files

Note: Downloading copyrighted content without permission may be illegal. Use this script responsibly.


## Run Locally

Clone the project

```bash
  git clone https://github.com/shakedlv/SpotifyFlightPlaylistMaker
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
    pip install -r requirements.txt
```

Run main.py in terminal

```bash
python main.py playlistId
    or
python3 main.py playlistId
```


## Usage/Examples

### Get Playlist ID
1) Get Playlist Share Link
    * Right Click Playlist -> Share -> Copy link to playlist
![Get Playlist Link](https://github.com/shakedlv/SpotifyFlightPlaylistMaker/blob/master/photos/info.jpg?raw=true)
Example Link : https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=bd9695494bf04ac6

open.spotify.com/playlist/ [ID] ?si=bd9695494bf04ac6


```bash
python main.py playlistId
    or
python3 main.py playlistId
```

Example 
```bash
python main.py 37i9dQZF1DXcBWIGoYBM5M
    or
python3 main.py 37i9dQZF1DXcBWIGoYBM5M
```

## Roadmap
- Add threading for faster download
- Improve error handling
- Add more arguments
- Create New folder for same playlist or override existing one
  - Ignore existing song in the same playlist 

