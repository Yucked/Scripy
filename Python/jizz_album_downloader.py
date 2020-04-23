import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import logging
import random
import string

log = logging.getLogger(__name__)
logging.basicConfig(level='DEBUG')

def create_dir(path):
    if os.path.exists(path):
        log.warning('Directory {} already exists!'.format(path))
        return

    os.mkdir(path)
    log.info('Created directory {}'.format(path))

def download_album(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    matches = soup.select('a[class*="envira-gallery-"]')
    if matches == 0:
        log.error('No matches found. Selector broken perhaps?')
        return

    link_map = {}
    for a in matches:
        a_title = a['title']
        title = a_title if len(a_title) != 0 else ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        link_map[title] = a['href']
        log.debug('Added {} to link map.'.format(a['href']))

    title = soup.find("meta",  property="og:title")['content']
    log.info('Found {} links for {}.'.format(len(matches), title))

    path = '{}\{}'.format(os.getcwd(), title)
    create_dir(path)

    count = 0
    for key in link_map:
        link = link_map[key]
        log.info('Downloading {}'.format(link))
        file_name = os.path.join(path, '{}.{}'.format(key, link[-3:]))

        if os.path.isfile(file_name):
            log.error('File {} already exists!'.format(file_name))
            continue
        
        urllib.request.urlretrieve(link_map[key], file_name)
        count += 1

    log.info('Downloaded {}/{} of {}.'.format(len(matches), count, title))

try:
    while True:    
        inpt = input('Please enter album link: ')
        if len(inpt) == 0:
            log.error('Input cannot be empty!')
            continue
        
        download_album(inpt.strip())
except KeyboardInterrupt:
    log.info('Have fun fella!')
