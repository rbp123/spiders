import  requests
from lxml import  etree

headers = {
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
    'Referer':"https://www.douban.com/"
}
url = 'https://movie.douban.com/'

response = requests.get(url,headers=headers)
# print(response.text)
test = response.text
html = etree.HTML(test)
ul = html.xpath("//ul[@class='ui-slide-content']")[0]
lis = ul.xpath('./li')
movies = []
for li in lis:
    title = li.xpath("@data-title")
    rate = li.xpath("@data-rate")
    trailer = li.xpath("@data-trailer")
    duration = li.xpath("@data-duration")
    region = li.xpath("@data-region")
    director = li.xpath("@data-director")
    actors =  li.xpath("@data-actors")
    image = li.xpath(".//img/@src")

    movie ={

        "title":title,
        "image": image,
        "rate":rate,
        "duration":duration,
        "region":region,
        "director":director,
        "actors":actors,
        "trailer": trailer
    }
    movies.append(movie)

for movie in movies:
    for k,v in movie.items():
        print(k , ":" ,v[0])
    print("\n")


