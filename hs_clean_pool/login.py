import requests
from bs4 import BeautifulSoup
import time

base_url = 'http://localhost:8082'
path = r"C:\Users\DELL\Desktop\jmx/"
count = 1
urls = []
has_go_urls = []


def get_url(url):
    has_go_urls.append(url)
    try:
        r = requests.get(url, auth=("manager", "manager"))
        # print r.status_code
        if r.status_code is 200:
            html = r.content
            global count
            print count, url
            with open(path + str(count) + ".html", 'w') as f:
                count += 1
                f.write(html)

            soup = BeautifulSoup(html, "lxml")
            get_a(soup)
            # get_form(soup)

            # time.sleep(2)
    except:
        pass


def add_url(url):
    if url not in urls:
        # if 'HelloAgent' not in url:
            urls.append(base_url + url)


def get_a(soup):
    hrefs = soup.find_all("a")
    for h in hrefs:
        url = h["href"]
        add_url(url)


def get_form(soup):
    actions = soup.find_all('form')
    for action in actions:
        url = action['action']
        add_url(url)

if __name__ == '__main__':
    get_url(base_url)

    while(urls):
        u = urls.pop()
        if u not in has_go_urls:
            get_url(u)
    print "url pool", len(urls)
    print "has_url", len(has_go_urls)




