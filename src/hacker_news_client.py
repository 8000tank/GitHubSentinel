import requests
from bs4 import BeautifulSoup
from logger import LOG

class HackerNewsClient:
    def __init__(self):
        self.base_url = 'https://news.ycombinator.com/'

    def fetch_top_stories(self):
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            stories = soup.find_all('tr', class_='athing')

            top_stories = []
            for story in stories:
                if title_tag := story.find('span', class_='titleline').find('a'):
                    title = title_tag.text
                    link = title_tag['href']
                    top_stories.append({'title': title, 'link': link})

            return top_stories
        except Exception as e:
            LOG.error(f"Error fetching HackerNews stories: {e}")
            return [] 