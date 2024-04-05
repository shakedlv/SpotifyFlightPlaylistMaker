from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pytube import YouTube
from tqdm import tqdm

import os


def print_output(info):
    print(f"[Spotify Scraper] : {info}")


def make_unique_folder(playlist, creator):
    i = 1
    folder_name = f"{playlist}_{creator}"
    while os.path.exists(folder_name):
        folder_name = f"{playlist}_{creator}_{i}"
        i += 1
    os.makedirs(f"{folder_name}")
    return folder_name


class SpotifyDriver:
    playlist_songs_info = []
    songs_failed = 0
    playlist_title = ""
    playlist_creator = ""

    def __init__(self, playlist_url, headless=False):
        self.options = webdriver.EdgeOptions()
        self.options.use_chromium = True
        self.options.add_argument("--profile-directory=Default")

        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument('--disable-default-apps')
        self.options.add_argument('--allow-silent-push')
        self.options.add_argument('--disable-notifications')
        self.options.add_argument('--suppress-message-center-popups')
        if headless:
            self.options.add_argument("headless")
            self.options.add_argument("disable-gpu")
        self.driver = webdriver.Edge(options=self.options, service=Service(EdgeChromiumDriverManager().install()))
        self.driver.get(f" https://open.spotify.com/playlist/{playlist_url}")
        self.playlist_title = self.driver.find_element(By.XPATH, './/span[@class="rEN7ncpaUeSGL9z0NGQR"]/h1').text
        self.playlist_creator = self.driver.find_element(By.XPATH,
                                                         './/div[@class="RANLXG3qKB61Bh33I0r2 '
                                                         'NO_VO3MRVl9z3z56d8Lg"]/span/a').text

        self.get_playlist_songs()

    def get_playlist_songs(self):
        playlist_items_container = '/html/body/div[3]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/main/div[' \
                                   '1]/section/div[2]/div[3]/div[1]/div[2]/div[2]'
        playlist_items_container_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, playlist_items_container)))
        playlist_items = playlist_items_container_element.find_elements(By.XPATH, "*")
        print_output(f"Found {len(playlist_items)} Songs")
        for song in playlist_items:
            try:
                song_title = WebDriverWait(song, 10).until(EC.presence_of_element_located((By.XPATH,  './/a[@class="t_yrXoUO3qGsJS4Y6iXX"]/div'))).text
                artists_element = WebDriverWait(song, 10).until(EC.presence_of_all_elements_located((By.XPATH, './/div[@class="iCQtmPqY0QvkumAOuCjr"]/span/div/a')))
                if len(artists_element) >= 1:
                    artist = artists_element[0].text
                    self.playlist_songs_info.append({
                        "title": song_title,
                        "artist": artist
                    })
                else:
                    self.songs_failed += 1
            except Exception as ex:

                self.songs_failed += 1

        print_output(f"Finish fetched {len(self.playlist_songs_info)}, failed {self.songs_failed}")
        self.download_songs(self.playlist_title, self.playlist_creator)

    def get_youtube_url_by_song(self, title, artist):
        search_query = f'https://www.youtube.com/results?search_query={title}+by+{artist}'
        self.driver.get(search_query)
        result = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-video-renderer')))
        return result[0].find_element(By.ID, "video-title").get_attribute('href')

    def download_songs(self, playlist, creator):
        folder_name = make_unique_folder(playlist, creator)

        with tqdm(total=len(self.playlist_songs_info)) as pbar:
            for index, song in enumerate(self.playlist_songs_info):
                url = self.get_youtube_url_by_song(song['title'], song['artist'])
                yt = YouTube(url)
                try:
                    yd = yt.streams.get_audio_only().download(
                        folder_name, f"{song['title']} by {song['artist']}.mp3", max_retries=5)
                except Exception as e:
                    print(f"Error downloading {song['title']}: {e}")
                    continue
                pbar.update()

        file_count = len([f for f in os.listdir(folder_name) if os.path.isfile(f)])
        self.driver.close()
