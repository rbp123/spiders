from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import re
import time

driver_path = r'D:\chromedriver\chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)

def page():
    start_url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
    driver.get(start_url)
    WebDriverWait(driver, 100).until(
            EC.url_to_be(
                'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=')
        )
    page_prase()
def page_prase():
    page = driver.page_source
    html = etree.HTML(page)
    urls = html.xpath("//a[@class='position_link']/@href")
    while True:
       for url in urls:
           detail_prase(url)
       next_btn = driver.find_element_by_xpath('//div[@class="pager_container"]/span[last()]')
       if 'pager_next_disabled' in next_btn.get_attribute('class'):
           return
       else:
           next_btn.click()
           page_prase()


def detail_prase(url):
    time.sleep(0.5)
    driver.execute_script("window.open('%s')" %url)
    # driver.get(url)
    driver.switch_to.window(driver.window_handles[1])

    soure = driver.page_source
    html = etree.HTML(soure)
    job_name = html.xpath('//div[@class="job-name"]/@title')[0]
    print(job_name)
    company = html.xpath('//div[@class="company"]/text()')[0]
    ps = html.xpath('//dd[@class="job_request"]/p/span/text()')
    salsry = ps[0].strip()
    addres = ps[1].replace('/','')
    years = ps[2].replace('/','')
    education = ps[3].replace('/','')
    quan = ps[4]

    zyh = html.xpath('//dd[@class="job-advantage"]/span/text()')[0]
    yh = html.xpath('//dd[@class="job-advantage"]//p/text()')[0]
    zms = html.xpath('//dd[@class="job_bt"]//h3/text()')[0]
    ms = html.xpath('//dd[@class="job_bt"]//div//text()')
    ms = "\n".join(list(map(lambda ms:ms.strip(),ms)))
    ms = re.sub(r'\n','',ms)
    address = html.xpath('//div[@class="work_addr"]//text()')
    address = "".join(list(map(lambda address: address.strip(),address)))
    address = re.sub(r'查看地图', '', address)
    driver.current_window_handle

    print(job_name,company,salsry,addres,years,education,quan,zyh,yh,zms,ms,address)
    print('******'*20)

    time.sleep(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


if __name__ == '__main__':
    page_prase()








