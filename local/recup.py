from datetime import datetime
import os
import subprocess
import xml.etree.ElementTree as ET

import boto3
import requests


def delete_file(filename):
    s3 = boto3.resource('s3')
    s3.Object('wplnnewscast', f'rss/{filename}').delete()


def download_feed():
    '''get the feed and create an ET object, which can then be called from other functions.'''
    header = {'User-Agent': 'Darth Vader'}  # usually helpful to identify yourself
    with open ('feed.xml', mode='wb') as downloaded_file:
        a = requests.get('https://wplnnewscast.s3.us-east-2.amazonaws.com/rss/feed.xml', headers=header)
        downloaded_file.write(a.content)
        downloaded_file.close()
    # return the NAME of the file, otherwise we're returning something else ET doesn't understand. just point to the name of the file!
    return downloaded_file.name

class Episode():
    def __init__(self) -> None:
        pass

    def title(self):
        timestamp = datetime.now().strftime('%a %d %b %I:%M %p')
        return timestamp
    
    def filename(self):
        timestamp = datetime.now().strftime('%a_%d_%b_%I%M_%p.mp3')
        return timestamp
    
    def pub_date(self):
        pub_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S -6000')
        return pub_date
    
    def enclosure(self):
        url = Episode.filename(self)
        url = f'https://wplnnewscast.s3.us-east-2.amazonaws.com/rss/{url}'
        return url
    
    def upload_file(self):
        try:
            audio_filename = Episode.filename(self)
            xml_filename = 'feed.xml' # doesn't change

            s3_client = boto3.client('s3')
            s3_client.upload_file(f'{audio_filename}', "wplnnewscast", f'rss/{audio_filename}')
            s3_client.upload_file(f'{xml_filename}', "wplnnewscast", f'rss/{xml_filename}')
        except Exception as err:
            print(f'error uploading to S3: {err}')

    def record_and_save(self):
        filename = Episode.filename(self)
        subprocess.run(f'ffmpeg -t 20.5 -i http://npl.streamguys1.com/live {filename}')

    def add_new_episode(self):
        feed = download_feed()
        feed = ET.parse(feed)
        root = feed.getroot()
        root = root.find('channel')

        # make a new element, called 'item'
        item = ET.Element('item')

        # add elements to the item element
        title = ET.Element('title')
        title.text = Episode.title(self)
        item.append(title)

        pubDate = ET.Element('pubDate')
        pubDate.text = Episode.pub_date(self)
        item.append(pubDate)

        enclosure = ET.Element('enclosure')
        enclosure.set('url', Episode.enclosure(self))
        item.append(enclosure)

        # insert the item element into the channel element, at index position 5
        root.insert(5, item)

        ET.indent(feed) # makes the XML real pretty like
        feed.write('feed.xml')
    
    def delete_local_audio_file(self):
        filename = Episode.filename(self)
        os.remove(filename)


episode = Episode()

episode.record_and_save()
download_feed()
episode.add_new_episode()
episode.upload_file()
episode.delete_local_audio_file()
# need to add: delete the local feed as well after downloading