import argparse
from datetime import datetime
import os
import subprocess
import time
import xml.etree.ElementTree as ET

import boto3
import requests

def get_record_length():
        parser = argparse.ArgumentParser()
        parser.add_argument('--record_length', type=str, required=True)
        args = parser.parse_args()
        record_length = args.record_length
        return record_length


def delete_file(filename):
    s3 = boto3.resource('s3')
    s3.Object('wplnnewscast', f'rss/{filename}').delete()

def upload_file(filename):
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(f'{filename}', "wplnnewscast", f'rss/{filename}')
    except Exception as err:
        print(f'error uploading to S3: {err}')


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
        self.record_length = get_record_length()
        self.feed_file = download_feed()
        self.audio_filename = datetime.now().strftime('%a_%d_%b_%I%M_%p.mp3')
        self.guid = datetime.now().strftime('%a_%d_%b_%I%M_%p.mp3')
        self.episode_title = datetime.now().strftime('%A %d %b %I:%M %p')
    
    def pub_date(self):
        pub_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S -6000')
        return pub_date
    
    def enclosure(self, filename):
        url = f'https://wplnnewscast.s3.us-east-2.amazonaws.com/rss/{filename}'
        return url
    
    def size_in_bytes(self, filename):
        size_in_bytes = os.path.getsize(filename)
        size_in_bytes = str(size_in_bytes)
        return size_in_bytes

    def record_and_save(self, filename):
        subprocess.run(f'ffmpeg -f dshow -i audio="Line In (Realtek(R) Audio)" -t {self.record_length} {filename}')

    def add_new_episode(self, filename, episode_title):
        feed = ET.parse(self.feed_file)
        root = feed.getroot()
        root = root.find('channel')

        # make a new element, called 'item'
        item = ET.Element('item')

        # add elements to the item element
        title = ET.Element('title')
        title.text = episode_title
        item.append(title)

        pubDate = ET.Element('pubDate')
        pubDate.text = Episode.pub_date(self)
        item.append(pubDate)

        enclosure = ET.Element('enclosure')
        enclosure.set('url', Episode.enclosure(self, filename))
        enclosure.set('length', Episode.size_in_bytes(self, filename))
        enclosure.set('type', 'audio/mpeg')
        item.append(enclosure)

        guid = ET.Element('guid')
        guid.set('isPermaLink', 'false')
        guid.text = self.guid
        item.append(guid)

        last_build_date = root.find('lastBuildDate')
        last_build_date.text = Episode.pub_date(self)

        # insert the item element into the channel element, at index position x
        root.insert(6, item)

        ET.indent(feed) # makes the XML real pretty like
        feed.write(self.feed_file)
    
    def remove_old_episodes(self):
        feed = ET.parse(self.feed_file)
        root = feed.getroot()
        root = root.find('channel')
        number_of_items = root.findall('item')
        if len(number_of_items) > 50:
            guid_of_item = number_of_items[-1]
            guid = guid_of_item.find('guid').text
            root.remove(guid_of_item)
            delete_file(guid)
            ET.indent(feed)
            feed.write(self.feed_file)
        else:
            print('under 50')
    
    def delete_local_file(self, file_to_delete):
        os.remove(file_to_delete)

def main():
    try:
        episode = Episode()
        episode.record_and_save(filename=episode.audio_filename)
        download_feed()
        episode.add_new_episode(filename=episode.audio_filename, episode_title=episode.episode_title)
        episode.remove_old_episodes()
        upload_file(filename=episode.audio_filename) # upload audio
        upload_file(filename=episode.feed_file) # upload RSS
        episode.delete_local_file(file_to_delete=episode.audio_filename)
        episode.delete_local_file(file_to_delete=episode.feed_file)
    except Exception as asdf:
        print(asdf)
        os.remove(episode.audio_filename)

if __name__ == '__main__':
        main()