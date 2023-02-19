import requests
import xml.etree.ElementTree as ET

rss_url = 'https://feeds.npr.org/510051/podcast.xml'

def get_feed():
    '''get the feed and create an ET object, which can then be called from other functions.'''
    header = {'User-Agent': 'Darth Vader'}  # usually helpful to identify yourself
    rssfeed = requests.get(rss_url, headers=header)
    rssfeed = rssfeed.text
    rssfeed = ET.fromstring(rssfeed)
    root = rssfeed.find('channel')
    return root

def get_items():
    items = get_feed().findall('item')
    episodes = []
    for item in items:
        episode = []

        title = item.find('title')
        title = title.text

        pubDate = item.find('pubDate')
        pubDate = pubDate.text

        enclosure = item.find('enclosure').attrib
        enclosure = enclosure.get('url')

        episode.append(title)
        episode.append(pubDate)
        episode.append(enclosure)

        episodes.append(episode)

    return episodes

def check_banner():
    try:
        banner = open('message.txt', 'r')
        banner = banner.read()
    except:
        banner = 'none'

    return banner