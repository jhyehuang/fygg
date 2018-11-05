
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




# In[26]:


def process_item( item):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    tdriver = webdriver.Chrome(executable_path='/home/zhijiehuang/chromedriver', options=chrome_options)
    print(item['url'])
    tdriver.get(item['url'])
    webdriver.support.ui.WebDriverWait(tdriver, 1).until(lambda x: x.find_element_by_id("noticeContent"))
    content = tdriver.page_source
    tosendPeople=tdriver.find_elements_by_id('tosendPeople')[0].text
    noticeContent=tdriver.find_elements_by_class_name('rmfy-content')[0].text
    contents_foot=tdriver.find_elements_by_class_name('rmfy-contents-foot')[0].text
    file_notice='%s\n%s\n%s\n'%(tosendPeople,noticeContent,contents_foot)
    file_name = os.path.join(r'.','%s-%s-%s.txt'%(item['name'][:40],item['file_type'],item['zx_data']))
    with open(file_name,'w') as fp:
        fp.write(file_notice)
    tdriver.close()


# In[27]:


allowed_domains = 'https://rmfygg.court.gov.cn'
for _ in range(5):
    root = etree.HTML(driver.page_source)
    all_gg = root.xpath('//tbody[@class="rmfy-table-tbody"]/tr')
    for pics in all_gg:
        pic=pics.xpath('.//td')
        item = {}
        fy_name=pic[0].xpath("./a/text()")[0]
        name = pic[1].xpath("./a/@title")[0]
        file_type = pic[2].xpath('./a/text()')[0]
        addr = pic[1].xpath("./a/@href")[0]
        url = 'https://rmfygg.court.gov.cn'+addr
        zx_data=pic[3].xpath("./a/text()")[0]
        item['fy_name'] = fy_name
        item['name'] = name
        item['url'] = url
        item['file_type'] = file_type
        item['zx_data'] = zx_data
        process_item(item)
    time.sleep(5)
    #driver.find_elements_by_id("noticeListTable_next")[0].click()
    driver.find_elements_by_class_name("paginate_button")[-2].click()
    webdriver.support.ui.WebDriverWait(driver, 1).until(lambda x: x.find_element_by_id("gg-list"))


# In[ ]:


driver.close()

