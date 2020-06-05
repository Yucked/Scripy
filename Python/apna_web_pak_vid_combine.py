import requests
import urllib.request
import os
import subprocess
from bs4 import BeautifulSoup
import logging
import re

log = logging.getLogger(__name__)
logging.basicConfig(level='INFO')
part_map = {}

def create_dir(path):
    if os.path.exists(path):
        log.warning('Directory {} already exists!'.format(path))
        return

    os.mkdir(path)
    log.info('Created directory {}'.format(path))
    
def build_part_map(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    matches = soup.select('div[class*="bbWrapper"]')
    
    if len(matches) == 0:
        log.error('Could not find any element matching bbWrapper.')
        return

    get_information(soup)    
    match = matches[0]
    links = match.find_all('a')    
    log.info('Found {} links related to file.'.format(len(links)))
    
    for link in links:
        title = link.contents[0]
        url = link['href']
        part_map[title] = url

    log.info('Finished getting all links.')

def get_information(soup):
    description_property = soup.find("meta",  property="og:description")['content']
    episode_info = description_property.split('\n')[0].split('-')[0]    
    matches = re.search('(\w+)\s(Episode\s\d)', episode_info)
    
    global folder_name
    global episode_num
    global path
    folder_name = matches.group(1)
    episode_num = matches.group(2)
    path = '{}\{}'.format(os.getcwd(), folder_name)
    
    create_dir(folder_name)

def get_url(url, query, key):
    log.info('Reading page information for {}.'.format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    source = soup.find(query)[key]
    return source

def download_file(title, link):    
    extension = link[link.rindex('.') - len(link):]
    part = title[title.index('Online') + len('Online'):]
    file_name = '{} {}{}'.format(episode_num, part, extension)
    file_path = os.path.join(path, file_name)

    write_to_file(file_path)
    log.info('Downloading file {}'.format(file_name))
    urllib.request.urlretrieve(link, file_path)
    log.info('Finished downloading {}'.format(file_name))             

def write_to_file(video_path):
    with open('{}.txt'.format(episode_num), 'a+') as file:
        file.write('file \'{}\'\n'.format(video_path))
    
def combine_videos():
    cmd = 'ffmpeg -f concat -safe 0 -i "{}.txt" -c copy {}.mp4'.format(episode_num, episode_num).split()
    subprocess.call(cmd)
    
url = input('Please enter page url: ')
build_part_map(url)

for title in part_map:
    part_map[title] = get_url(part_map[title], 'iframe', 'src')
    part_map[title] = get_url(part_map[title], 'source', 'src')
    if 'Promo' in title:
        log.warning('Skipping promo ..')
        pass
    download_file(title, part_map[title])

log.info('Combining videos ...')
combine_videos()
