import requests
import threading
import csv
from lxml import etree
from queue import Queue

glock = threading.Lock()
class DJ_P(threading.Thread):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    def __init__(self,download_queue,save_queue,*args,**kwargs):
        super(DJ_P, self).__init__(*args,**kwargs)
        self.download_queue = download_queue
        self.save_queue = save_queue

    def run(self):
        while True:
            if self.download_queue.empty():
                return
            page_url = self.download_queue.get()
            response = requests.get(page_url, self.headers)
            html = etree.HTML(response.text)
            lis = html.xpath('//div[@class="j-r-list"]//li')
            author, content, detail_url = '', '', ''
            for li in lis:
                author = li.xpath('//div[@class="u-txt"]/a/text()')
                content = li.xpath('//div[@class="j-r-list-c-desc"]/a/text()')
                detail_urls = li.xpath(
                    '//div[''@class="j-r-list-c-desc"]//a/@href')
                detail_url = []
                for x in detail_urls:
                    detail_url.append('http://www.budejie.com' + x)
            self.save_queue.put((author, content, detail_url))

class DJ_C(threading.Thread):
    def __init__(self,download_queue,save_download,*args,**kwargs):
        super(DJ_C, self).__init__(*args,**kwargs)
        self.download_queue = download_queue
        self.save_queue = save_download
    def run(self):
       while True:
           if self.download_queue.empty() and self.save_queue.empty():
               return
           datas = []
           author, content, detail_url = self.save_queue.get()
           for x in zip(author, content, detail_url):
               data = {
                   'author': x[0],
                   'content': x[1],
                   'url': x[2]
               }
               glock.acquire()
               datas.append(data)

               headers = ['author', 'content', 'url']
               with open('DJ.csv', 'a', encoding='utf-8', newline='') as fp:
                   writer = csv.DictWriter(fp, headers)
                   writer.writeheader()
                   writer.writerows(datas)
               glock.release()


def main():
    download_queue = Queue(100)
    save_queue = Queue(100)

    for x in range(1,100):
        url = 'http://www.budejie.com/text/' + str(x)
        download_queue.put(url)

    for x in range(5):
        t = DJ_P(download_queue,save_queue)
        t.start()
    for x in range(3):
        t = DJ_C(download_queue,save_queue)
        t.start()

if __name__ == '__main__':
    main()