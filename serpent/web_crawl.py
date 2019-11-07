"""simple web crawler and scraper"""

from bs4 import BeautifulSoup
import urllib.request
import csv
from datetime import datetime


def get_site():
    website = input("[+] Enter a website to scrape:\n>")
    resp = urllib.request.urlopen(website)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    
    for link in soup.find_all('a', href=True):
        # print(link['href'], " <=LINK | TEXT=> ", link.text)
        with open('index.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([link['href'], link.text, datetime.now()])
            print('[+] adding link...')


def main():
    get_site()


if __name__ == '__main__':
    main()
