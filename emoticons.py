import requests
from urllib import  request
from lxml import etree
import  os
import re
import threading
from queue import Queue

class Prouder(threading.Thread):
    """生产者"""
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Prouder, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.prase_page(url)

    def prase_page(self,url):
        """解析网页并获取图片地址数据"并加入到img_queue队列中"""
        response = requests.get(url,headers=self.headers)
        text = response.text
        html = etree.HTML(text)
        imags= html.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')
        for imag in imags:
            imag_url = imag.get('data-original')
            alt = imag.get('alt')
            alt = re.sub(r'[\?？.。！\'！·\/]','',alt)
            suffixs = os.path.splitext(imag_url)[1]
            suffixs = re.sub(r'[!dta]','',suffixs)
            name = alt + suffixs
            self.img_queue.put((imag_url,name))


class Consumer(threading.Thread):
    """消费者"""
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        """实现Thread的父类方法run()并下载图片"""
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            imag_url,name = self.img_queue.get()
            request.urlretrieve(imag_url,'images/' + name)
            print(name + " 下载完成!" )

def main():
    page_queue = Queue(100)
    img_queue = Queue(1000)

    for x in range(1,100):
        url = 'https://www.doutula.com/photo/list/?page=%d' % x
        page_queue.put(url)

    for x in range(5):
        t1 = Prouder(page_queue,img_queue)
        t1.start()

    for x in range(5):
        t2 = Consumer(page_queue,img_queue)
        t2.start()

if __name__ == '__main__':
    main()