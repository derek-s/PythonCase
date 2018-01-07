#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests 
import urllib
import progressbar
from bs4 import BeautifulSoup
import os
import threading
import datetime
import queue

class spider():
    def __init__(self):
        self.header = {
            "Referer": "https://www.baidu.com/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36"
        }
        self.url = "http://tfr.org/"
        self.proxy = {
            "http": "http://127.0.0.1:1090",
            "https": "http://127.0.0.1:1090"
        }
    
    def request(self, url):
        fails = 1
        while fails < 31:
            try:
                r = requests.get(url, headers=self.header, timeout=10)
                return r.text
            except Exception as e:
                print e
                print 'error retry'
                fails += 1

    def page_source(self, pgstr, url):
        soup = BeautifulSoup(pgstr, "html.parser")
        for a_link in soup.select('a[href]'):
            link = a_link["href"]
            if link == "../":
                pass
            elif link.split('//')[-1].split('.')[-1].split('/')[-1] == "":
                link = url + link
                print link
                self.mkdir(link)
                self.download(link)
                self.page_source(self.request(link), link)
            else:
                link = url + link
                print link
                self.mkdir(link)
                self.download(link)

    def mkdir(self, url):
        if url == "":
            path = self.url.split('//')[-1]
            if not os.path.exists(path):
                os.makedirs(path)
                print path + "create"
            else:
                print path + "exists"
        else:
            path = str(url).split('//')[-1]
            if str(path).split('//')[-1].split('.')[-1].split('/')[-1] == "":
                if not os.path.exists(path):
                    os.makedirs(path)
                    print path + " is create"
                else:
                    print path + " is exists"
            else:
                print path + " is file"
        
    def download(self, url):
        path = str(url).split('//')[-1]
        filename = str(url).split('/')[-1]
        if filename.split('.')[-1] == '':
            filename = path + "index.html"
            self.indexdown(url, filename)
        else:
            filename = path
            filexists, length = self.isExists(url, filename)
            if filexists:
                self.filedown(url, filename, length)
            else:
                pass
                
    def indexdown(self, url, filename):
        try:
            print "downloading", url
            if not os.path.exists(filename):
                with open(filename, "wb") as down_write:
                    down_write.write(self.request(url).encode('utf-8'))
                print "done"
            else:
                print filename + " is exists"
        except Exception as e:
            print e

    def isExists(self, url, filename):
        r = requests.request(
            'GET', url, stream=True, headers=self.header, proxies=self.proxy)
        total_length = int(r.headers.get("Content-Length"))
        if os.path.exists(filename):
            print '%s is exists' % filename
            if os.path.getsize(filename) != total_length:
                return False, total_length
            else:
                return True, total_length
        else:
            return True, total_length

    def downproc(self, url, filename, start, end):
        headers = {
            "Referer": "https://www.baidu.com/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
            "Range": "bytes=%d-%d" % (start, end)
            }
        r = requests.get(url, stream=True, headers=headers)

        with open(filename, "r+b") as fp:
            fp.seek(start)
            var = fp.tell()
            for chunk in r.iter_content(chunk_size=1):
                if chunk:
                    fp.write(chunk)
                    fp.flush()


    def filedown(self, url, filename, total_length):
        nthreads = 1
        filename_temp = filename + ".temp"
        f = open(filename_temp, "wb")
        f.truncate(total_length)
        f.close()
        
        part = total_length // nthreads
        for i in range(nthreads):
            start = part * i
            if i == nthreads - 1:
                end = total_length
            else:
                end = start + part

        t = threading.Thread(target=self.downproc, kwargs={
            "start": start,
            "end": end,
            "url": url,
            "filename": filename_temp
        })
        t.setDaemon(True)
        t.start()

        mainthread = threading.current_thread()
        for t in threading.enumerate():
            if t is mainthread:
                continue
            t.join()
        print "download complete"
        os.rename(filename_temp, filename)

if __name__ == "__main__":
    testurl = "http://tfr.org/"
    spiders = spider()
    spiders.page_source(spiders.request(testurl), testurl)
    #spiders.download("http://tfr.org/cisco/")