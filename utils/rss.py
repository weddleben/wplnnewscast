import requests
import xml.etree.ElementTree as ET

rss_url = 'https://wplnnewscast.s3.us-east-2.amazonaws.com/rss/feed.xml'

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
        episode = {}

        title = item.find('title')
        title = title.text

        enclosure = item.find('enclosure').attrib
        enclosure = enclosure.get('url')

        episode.update({'title': title})
        episode.update({'enclosure': enclosure})

        # separate bottom & top of hour
        top_of_hour = ':04'
        if top_of_hour in title:
            episode.update({'time':'top_of_hour'})
        
        bottom_of_hour = ':33'
        if bottom_of_hour in title:
            episode.update({'time':'bottom_of_hour'})
        
        if 'Monday' in title:
            episode.update({'day':'Monday'})
        if 'Tuesday' in title:
            episode.update({'day':'Tuesday'})   
        if 'Wednesday' in title:
            episode.update({'day':'Wednesday'})
        if 'Thursday' in title:
            episode.update({'day':'Thursday'})
        if 'Friday' in title:
            episode.update({'day':'Friday'})

        episodes.append(episode)

    return episodes

def check_banner():
    banner = open('message.txt', 'r')
    banner = banner.read()

    if banner == '':
        return False

    return banner