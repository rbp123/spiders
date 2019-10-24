from selenium import webdriver
from lxml import etree
import time,re,random,csv

driver_path = r'D:\chromedriver\chromedriver.exe'
class BossSpider(object):
    def __init__(self,writer):
        self.base_url = 'https://www.zhipin.com'
        self.url = 'https://www.zhipin.com/job_detail/?query=python&city=101010100&industry=&position='
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.writer = writer

    def run(self):
        self.driver.get(url=self.url)
        while True:
            page_source = self.driver.page_source
            self.request_catalog_page(page_source=page_source)
            next_btn = self.driver.find_element_by_xpath("//div["
                                                         "@class='page']//a[last()]")
            if "next disabled" in next_btn.get_attribute("class"):
                return
            else:
                next_btn.click()

    def request_catalog_page(self,page_source):
        html = etree.HTML(page_source)
        urls = html.xpath("//div[@class='info-primary']//a/@href")
        for url in urls:
            url = self.base_url + url
            self.request_detail_page(url=url)
            time.sleep(random.randint(1,3))

    def request_detail_page(self,url):
        self.driver.execute_script("window.open('%s')" %url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        detail_page_source = self.driver.page_source
        detail_html = etree.HTML(detail_page_source)
        self.prase_detail_page(detail_html=detail_html)

    def prase_detail_page(self,detail_html):
        all_datas = []
        job_status = detail_html.xpath("//div[@class='job-status']/text()")[0]
        job_name = detail_html.xpath("//div[@class='info-primary']//h1/text("
                                    ")")[0]
        salary = detail_html.xpath("//span[@class='salary']/text()")[0]
        salary = re.sub(r"[\s]","",salary)
        dates = detail_html.xpath("//div[@class='job-banner']//p/text()")
        city = dates[0]
        work_years = dates[1]
        education = dates[2]
        job_description = detail_html.xpath("//div[@class='job-sec']//div["
                                            "@class='text']//text()")
        job_description = "".join(list(map(lambda x:re.sub(r"(\n|●|  )","",x),
                                  job_description)))
        company_introduction = detail_html.xpath("//div[@class='job-sec company-info']//div["
                                            "@class='text']//text()")
        company_introduction = "".join(list(map(lambda x: re.sub(r"(\n|●| )", "", x),
                                          company_introduction)))
        com = detail_html.xpath("//div[@class='job-sec company-info']//a/@href")
        if len(com):
            company_url = self.base_url + com[0]
        else:
            company_url = self.base_url
        work_address = detail_html.xpath("//div["
                                         "@class='location-address']/text()")[0]
        map_url = detail_html.xpath("//div["
                                         "@class='job-location']//img/@src")[0]
        contacts = detail_html.xpath("//h2[@class='name']/text()")
        if len(contacts):
            contacts = contacts[0]
        datas_dict = {
           'job_name':job_name,
           'job_status':job_status,
           'salary':salary,
           'city':city,
           'work_years':work_years,
           'education':education,
           'job_description':job_description,
           'company_introduction':company_introduction,
           'company_url':company_url,
           'work_address':work_address,
           'map_url':map_url,
           'contacts': contacts
         }
        all_datas.append(datas_dict)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.writer.writerows(all_datas)
        print('保存成功！')

def writer_func():
    headers = ['job_name', 'job_status', 'salary', 'city', 'work_years',
               'education', 'job_description', 'company_introduction',
               'company_url', 'work_address', 'map_url', 'contacts']
    fp = open("boss.csv", 'a', newline='', encoding='utf-8')
    writer = csv.DictWriter(fp, headers)
    writer.writeheader()
    return writer

if __name__ == '__main__':
    writer = writer_func()
    bossspider = BossSpider(writer)
    bossspider.run()