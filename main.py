from SpotifyScraper import SpotifyDriver
import  argparse

parser = argparse.ArgumentParser(description="Create offline playlist from Spotify")
parser.add_argument('playlist_id', metavar='Playlist-ID', type=str, help='Enter playlist id')
args = parser.parse_args()

playlist_id = args.id

spotify_client = SpotifyDriver(playlist_id)