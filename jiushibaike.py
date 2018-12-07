import requests
import re

def parse_page(url):
    """解析网页并获取数据"""
    headers = {
        "User-Agent":'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    respose = requests.get(url,headers=headers)
    text = respose.text

    # 发布者列表
    Commentators = re.findall('<h2>(.*?)</h2>',text,re.DOTALL)
    Com = []
    for Commentator in Commentators:
        Com.append(Commentator.strip())

    #内容列表
    contents = re.findall('<div\sclass="content">.*?<span>(.*?)</span>',text,re.DOTALL)
    cons = []
    for x in contents:
        cons.append(re.sub('<.*?>',"",x).strip())

    #实现一一对应关系列表
    Completes = []
    for value in zip(Com,cons):
        Commentator,content = value
        all = {
            "Commentator":Commentator,
            "content":content
        }
        Completes.append(all)

    #遍历输出
    for x in Completes:
        for k,v in x.items():
            print(k,v)
        print("***" * 30)

def main():
    """提供网页地址"""
    url = "https://www.qiushibaike.com/text/page/5/"
    for x in range(1 ,10):
        url = url = "https://www.qiushibaike.com/text/page/%s/" % x
        parse_page(url)

if __name__ == '__main__':
    main()
