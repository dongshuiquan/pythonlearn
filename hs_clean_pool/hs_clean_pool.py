#coding:utf-8

import requests
from bs4 import BeautifulSoup
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

base_url = 'http://192.168.132.242:8082'
path = r"C:\Users\DELL\Desktop\jmx/"
# filter_url = '/ViewObjectRes//Administer+PoolA+manager+%3Aid%3DPool'  #/ViewObjectRes//Administer+PoolA+manager+%3Aid%3DPoolA
count = 1

pool_urls = []
action_urls = []

has_go_urls = []
action_has_go_urls = []

server_info = []


def get_pool_url(url):
    has_go_urls.append(url)
    try:
        r = requests.get(url, auth=("manager", "manager"))
        # print r.status_code
        if r.status_code is 200:
            html = r.content
            global count
            print (count, url)

            soup = BeautifulSoup(html, "html.parser")
            #print soup
            hrefs = soup.find_all("a")
            for h in hrefs:
                href = h["href"]
                if href not in pool_urls:
                    # if filter_url in href:
                        if "id=Pool" in h.text:
                            #print href
                            pool_urls.append(base_url + href)
    except:
        pass


def get_action_url(url):
    action_has_go_urls.append(url)
    try:
        r = requests.get(url, auth=("manager", "manager"))
        # print r.status_code
        if r.status_code is 200:
            html = r.content
            global count
            soup = BeautifulSoup(html, "html.parser")
            get_show_servers_action(soup)
            if pool_urls:
                u = pool_urls.pop()
                if u not in action_has_go_urls:
                    get_action_url(u)
    except:
        pass


def get_show_servers_action(soup):
    #print "get_show_servers_action"
    show_server_url = "action=Show_Servers"
    actions = soup.find_all('form')
    for ac in actions:
        u = ac['action']
        if u.endswith(show_server_url):
            action_urls.append(base_url + u + '?action=Show_Servers')


def get_action_page(url):
    try:
        r = requests.get(url, auth=("manager", "manager"))
        if r.status_code is 200:
            html = r.content
            global count
            print (count, url)
            #with open(path + str(count) + ".html", 'w') as f:
            #    count += 1
            #    f.write(html)

            soup = BeautifulSoup(html, "html.parser")
            parse_server_page(soup)
    except:
        pass


def parse_server_page(soup):
    table = soup.find('table')
    trs = table.find_all('tr')

    for tr in trs:
        tds = tr.find_all('td')

        if tds:
            info = []
            # print (type(tds))
            for i in range(len(tds)):
                if i is 0:
                    a = tds[i].find('a')
                    server = a['href']
                    info.append(base_url + server)
                elif i is 2:
                    user = tds[i].text
                    user = "" if user == " " else user
                    #print user
                    if user == "plm009":
                        # print "plm009"
                        shutdown_server(info[0])
                    # print "a" + user + "b"
                    info.append(user)

                elif i is 3:
                    mode = tds[i].text
                    info.append(mode)
                elif i is 4:
                    status = tds[i].text
                    info.append(status)
            #print info
            server_info.append(info)


def shutdown_server(url):
    try:
        r = requests.get(url, auth=("manager", "manager"))
        if r.status_code is 200:
            html = r.content
            soup = BeautifulSoup(html, "html.parser")
            shundown_server_action = "action=Shutdown_Server"
            actions = soup.find_all('form')
            for ac in actions:
                u = ac['action']
                # print u
                if u.endswith(shundown_server_action):
                    shundown_server_url = base_url + u + "?" + shundown_server_action
                    # print shundown_server_action
                    r = requests.get(shundown_server_url, auth=("manager", "manager"))
                    if r.status_code is 200:
                        print "success kill " + shundown_server_url
    except:
        pass


def main():
    #print 'start'
    get_pool_url(base_url)
    # print (pool_urls)
    while pool_urls:
        url = pool_urls.pop()
        get_action_url(url)

    # print action_urls
    while action_urls:
        url = action_urls.pop()
        get_action_page(url)
    # with open(path + "server_info.csv", 'w') as f:
    #     for info in server_info:
    #         for massage in info:
    #             f.write(massage);
    #             f.write(",")
    #         f.write('\n');

if __name__ == '__main__':
	while True:
	    main()
	    pool_urls = []
	    action_urls = []
	    has_go_urls = []
	    action_has_go_urls = []
	    server_info = []
	    time.sleep(60)



