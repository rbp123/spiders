from lxml import  etree
import requests

BASE_DOMAIN = 'https://www.dytt8.net'
url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_1.html'
HEADERS = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        "Referer": 'https://www.dytt8.net/'
    }
def get_datil_url(url):
    """请求网页数据"""
    response = requests.get(url, headers=HEADERS)
    test = response.text
    html = etree.HTML(test)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    for detail_url in detail_urls:
       full_urls =  map(lambda url:BASE_DOMAIN + detail_url,detail_urls)
       return full_urls


def parse_detail_page(url):
    """每一页的解析及数据获取"""
     movie = { }
     response  = requests.get(url,headers=HEADERS)
     text = response.content.decode('gbk')
     html  = etree.HTML(text)
     title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
     movie['title'] = title
     # print(title)
     zoomE = html.xpath('//div[@id="Zoom"]')[0]
     images= zoomE.xpath('.//img/@src')
     cover = images[0]
     screenshot = images[1]
     movie['cover'] = cover
     movie['screenshot'] = screenshot

     infos = zoomE.xpath(".//text()")
     for index,info in enumerate(infos):
         if info.startswith("◎译　　名"):
             info = info.replace("◎译　　名","").strip()
             movie["译名"] = info
         elif info.startswith("◎片　　名"):
             info = info.replace("◎片　　名","").strip()
             movie["片名"] = info
         elif info.startswith("◎年　　代"):
             info = info.replace("◎年　　代", "").strip()
             movie["年代"] = info
         elif info.startswith("◎产　　地"):
             info = info.replace("◎产　　地", "").strip()
             movie["产地"] = info
         elif info.startswith("◎类　　别"):
             info = info.replace("◎类　　别", "").strip()
             movie["类别"] = info
         elif info.startswith("◎语　　言"):
             info = info.replace("◎语　　言", "").strip()
             movie["语言"] = info
         elif info.startswith("◎导　　演"):
             info = info.replace("◎导　　演", "").strip()
             movie["导演"] = info
         elif info.startswith("◎主　　演"):
             data = info.replace("◎主　　演", "").strip()
             for x in range(index+1,len(infos)):
                 actors = []
                 actor = infos[x].strip()
                 if actor.startswith("◎"):
                     break
                 actors.append(actor)
                 movie["actors"] = actors
         elif info.startswith("◎简　　介 "):
             info = info.replace("◎简　　介 ", "").strip()
             for x in range(index+1,len(infos)):
                 profile = infos[x].strip()
                 movie["profile"] = profile
     download_url = html.xpath("//td[@style='WORD-WRAP: break-word']//@href")[0]
     movie["download_url"] = download_url
     return movie

def spider():
    """循环爬取1-8页"""
    url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    movies = []
    for x in range(1,8):
        base_url = url.format(x)
        #填充url
        detail_urls = get_datil_url(base_url)
        for detail_url in detail_urls:
            movie =  parse_detail_page(detail_url)
            movies.append(movie)

    for movie in movies:
        print(movie)

if __name__ == '__main__':
    spider()
