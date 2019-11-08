"""simple web crawler and scraper"""

from bs4 import BeautifulSoup
import requests
#import urllib.request
import csv
from datetime import datetime


def get_site():
    """
    get target and format for http request
    """

    website = input("[+] Enter a website to scrape:\n>")
    website = "https://{}".format(website)

    # quick check format
    good_url = input(
        "[?] Is {} the correct target address? y/n\n".format(website))
    if good_url == "y":
        return website
    else:
        get_site()  # like magic baby


def scrape_website(website, mode):
    """
    scrape single website and add data to serpent.csv file
    """

    if mode == "y":
        # single website
        r = requests.get(website)
        data = r.text
        soup = BeautifulSoup(data, features="html.parser")

        with open('serpent.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['WEBSITE SCRAPE', '  ', website])

        for link in soup.find_all('a', href=True):
            with open('serpent.csv', 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([link['href'], link.text, datetime.now()])
                print('[+] adding link to {} {}...'.format(website, link.text))
    else:
        # mode == "n" : multiple websites
        with open('serpent.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['WEBSITE SCRAPE', '  ', website])

        r = requests.get(website)
        data = r.text
        soup = BeautifulSoup(data, features="html.parser")

        # recurse call with last full(.com) link to scrape multiple websites
        last_link = ""
        for link in soup.find_all('a', href=True):
            with open('serpent.csv', 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([link['href'], link.text, datetime.now()])
                print('[+] adding link to {} {}...'.format(website, link.text))

                # check for external link -
                link_check = link['href'].split(".")
                if link_check[0][0:4] == "http" and link_check[0][-3:] != "www":
                    print("\n", link_check, "\n")
                    # input()
                    if len(link_check) == 2:
                        last_link = "{}.com".format(link_check[0])
                    elif len(link_check) == 3:
                        last_link = "{}.{}.com".format(
                            link_check[0], link_check[1])
                    else:
                        pass

        if len(last_link) > 0:
            print("\n[!] Web scrape moving to {}\n".format(last_link))
            if last_link == website:
                print("[?] Scrape same page twice? y/n\n")
                again = input(">")
                if again == "y":
                    scrape_website(last_link, "n")
                else:
                    scrape_website(get_site(), "n")
            else:
                scrape_website(last_link, "n")
        else:
            print(
                "[!] Web scrape complete! \nCheck serpent.csv for results! \nGoodbye!")
            exit(0)


def mode_selector():
    """
    user input selects scrape mode
    """
    mode = input("[?] Select single website scrape mode? y/n\n")
    if mode == "y" or "n":
        return mode
    else:
        mode_selector()


def main():
    target = get_site()
    mode = mode_selector()
    scrape_website(target, mode)


if __name__ == '__main__':
    main()
