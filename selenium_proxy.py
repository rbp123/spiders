from selenium import webdriver

driver_path =r'D:\chromedriver\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument("--proxy-server=http://218.24.16.198	:43454")
driver = webdriver.Chrome(executable_path=driver_path
,options=options)
driver.get("https://httpbin.org/ip")
