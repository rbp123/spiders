import  requests
import time
import json
start_url = 'https://www.lagou.com/jobs/list_python?'
page_url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

def main():
    headers = {
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    session = requests.Session()
    session.get(url=start_url, headers=headers, timeout=3)
    cookie = session.cookies
    for x in range(1,100):
        data = {
        'first': 'false',
        'pn': str(x),
        'kd': 'python'
        }
        response = session.post(url=page_url, headers=headers,cookies=cookie,
        data=data,timeout=3)
        time.sleep(3)
        response.encoding = response.apparent_encoding
        datas_json = json.loads(response.text)
        print(datas_json)

        # keys = datas_json["content"]["hrInfoMap"].values()
        # for key in keys:
        #     print(key)
        #     datas = datas_json["content"]["hrInfoMap"]["key"]
        #     print(datas)

            # detail_url = 'https://www.lagou.com/jobs/' + key +'.html'
            # print(detail_url)

        break




if __name__ == '__main__':
    main()

