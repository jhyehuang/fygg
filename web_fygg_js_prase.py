
# coding: utf-8

# In[1]:


from lxml import etree
import requests
import chardet
from urllib.parse import urlencode #Python内置的HTTP请求库 
from requests.cookies import RequestsCookieJar
import time
import os


# In[22]:


import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='/home/zhijiehuang/chromedriver', options=chrome_options)

driver.get('https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?noticeTypeCode=66')
webdriver.support.ui.WebDriverWait(driver, 1).until(lambda x: x.find_element_by_id("gg-list"))
content = driver.page_source
file_notice='%s\n'%(content)
import random
c=random.randint(1,6)
for i in range(c):
    file_notice=file_notice+file_notice
file_name = os.path.join(r'.','%s.txt'%('rmfygg'))
with open(file_name,'w') as fp:
    fp.write(file_notice)
driver.close()

