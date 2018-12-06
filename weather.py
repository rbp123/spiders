import  requests
from bs4 import BeautifulSoup
from pyecharts import Bar

ALL_DATA = []
def prase_url(url):
    """解析网页并获取数据"""
    headers ={
        "User_Agent":'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    #请求网页数据
    response = requests.get(url,headers=headers)
    test = response.content.decode('utf-8')
    #解析网页，使用了lxml解析器
    soup = BeautifulSoup(test,'html5lib')
    #获取数据
    conMidtab = soup.find('div',class_="conMidtab")
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            temp= list(temp_td.stripped_strings)[0]
            ALL_DATA.append({"city":city,"temp":int(temp)})

def main():
    """给定原始url并调用函数完成可视化"""
    #url
    # url ='http://www.weather.com.cn/textFC/gansu.shtml'
    # prase_url(url)
    urls = [
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml'
     ]
    #循环遍历url
    for url in urls:
        prase_url(url)

    #以ALL_DATA列表的temp排序
    ALL_DATA.sort(key=lambda data:data["temp"])
    # print(len(ALL_DATA))
    data = ALL_DATA
    # print(data)
    #获取列表元素的对应值，并且cities和temp是--对应
    cities = list(map(lambda x:x["city"],data))
    temps = list(map(lambda x:x["temp"], data))

    #可视化
    chart = Bar("中国最低气温排行榜")
    chart.add(" ",cities,temps)
    chart.render("mim_temp.html")


if __name__ == '__main__':
    main()