#-*-coding:utf-8 -*-
__author__ = 'Jy2881'

from bs4 import BeautifulSoup
import re
from selenium import webdriver

user_list = set()
user_list_file = open(r"D:\workspace\creeper\simboob\user_list_file1.txt","a")
driver = webdriver.Firefox()

def make_user_list(url):
    driver.get(url)
    for i in range(100):
        html = driver.page_source
        bsObj = BeautifulSoup(html,"lxml")
        for div1 in bsObj.findAll("div",class_="col-sm-6 col-lg-4 col-xs-12 needmasonry"):
            for a in div1.find_all_next("a",class_="pull-left"):
                user = re.findall(r'/user/\d+/comments',str(a))
                user_list.add("http://www.yousuu.com" + user[0])
        try:
            nextPage = driver.find_element_by_link_text("下一页")
            nextPage.click()
        except:
            print(i)
            break

    print(len(user_list))
    for line in user_list:
        user_list_file.write(line+"\n")
url = "http://www.yousuu.com/book/118403"
make_user_list(url)