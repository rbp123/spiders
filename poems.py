import requests
import re
def prase_page(url):
    """解析网页并提取数据"""
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
    }
    response = requests.get(url,headers=headers)
    text= response.text

    #正则提取数据
    titles = re.findall(r'<div\sclass="sons">.*?<b>(.*?)</b>',text,re.DOTALL)
    Dynastys = re.findall(r'<p\sclass="source".*?<a.*?>(.*?)</a>',text,re.DOTALL)
    authors = re.findall(r'<p\sclass="source".*?<a.*?>.*?<a.*?>(.*?)</a>',text,re.DOTALL)
    contents = re.findall(r'<div\sclass="contson".*?>(.*?)</div>',text,re.DOTALL)
    # print(titles,Dynastys,authors,poetrys)

    #content的处理
    poems = []
    for content in contents:
        poe = re.sub(r"<.*?>","",content).strip()
        poems.append(poe)

    #各部分合为一个整体并输出
    poem = []
    for value in zip(titles,Dynastys,authors,poems):
        title,dynasty,author,poetry = value
        poemx = {
            "title":title,
            "dynasty":dynasty,
            "author":author,
            "content":poetry
        }
        poem.append(poemx)

    for k in poem:
        print(k)
        print("***"*30)

def main():
    """循环遍历网页"""
    url = "https://www.gushiwen.org/default_%s.aspx"
    for x in range(1,101):
        url = "https://www.gushiwen.org/default_%s.aspx"  % x
        prase_page(url)


if __name__ == '__main__':
    main()