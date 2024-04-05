from SpotifyScraper import SpotifyDriver
import  argparse

parser = argparse.ArgumentParser(description="Create offline playlist from Spotify")
parser.add_argument('id', metavar='id', type=str, help='Enter playlist id')
args = parser.parse_args()

id = args.id

spotify_client = SpotifyDriver(id)