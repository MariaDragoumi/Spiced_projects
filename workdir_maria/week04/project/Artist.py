
import random
import time
import requests
from bs4 import BeautifulSoup

class Artist:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.cls = 'tal qx'
        self.subcls = 'lyric-body'
        self.headers = {"User-Agent": 
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

    def get_song_links(self):
        response = requests.get(self.url,headers=self.headers).text
        time.sleep(10)
        soup = BeautifulSoup(response)
        links = []
        soup_links = soup.find_all(class_ = self.cls)
        for link in soup_links:
            if link.a:
                ln = link.a['href']
                links.append(f'https://www.lyrics.com{ln}')
        return links
    
    def get_lyrics(self,link):   
        response = requests.get(link,headers=self.headers)
        time.sleep(10) 
        if response.status_code == 404: print('blocked')
        soup = BeautifulSoup(response.text)
        if soup.find(class_ = self.subcls):
            lyrics = soup.find(class_ = self.subcls) #
            return lyrics.text
        else:
            return ['\n']

    def get_lyrics_file(self, number_of_samples):
        # To Do: Check in here for repeated lines, also between songs. Maybe new function
        links = self.get_song_links()
        samples = random.sample(links, number_of_samples)
        for link in samples:
            song_lyrics = self.get_lyrics(link)
            with open(f'./{self.name}.txt','a') as my_file:
                my_file.write(f'\n\n{song_lyrics}') 

    def read_artist_file(self):
        with open(f'./{self.name}.txt','r') as my_file:
            lyrics = my_file.readlines()  
        return lyrics   