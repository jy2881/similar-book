#-*-coding:utf-8 -*-
__author__ = 'Jy2881'

from bs4 import BeautifulSoup
import re
from selenium import webdriver


# 输入参数
user_list_file = r""
book_name = "顾道长生"

# 固定参数
dict ={}
driver = webdriver.PhantomJS(executable_path=r"C:\Python27\phantomjs-2.1.1-windows\bin\phantomjs.exe")
# user_list = open(user_list_file).read().split(",")
user_list = [875164]

# 遍历用户列表并更新总字典
def makeDict(url,url_new):
    print(url_new)
    driver.get(url_new)
    html = driver.page_source
    bsObj = BeautifulSoup(html,"lxml")

    for link in bsObj.findAll("div",class_="booklist-item"):
        name = link.findAll("div",class_="title")[0].findAll("a")[0].get_text()
        mark = link.findAll("div",class_="abstract")[0].findAll("span",class_="num2star")[0].findAll("i",style="color:#4D7BD6")
        new_dict[name] = len(mark)

    if bsObj.findAll("a",class_="btn btn-primary btn-block"):
        for button in bsObj.findAll("a",class_="btn btn-primary btn-block"):
            if button.get_text() == "点击加载下一页":
                str = button.get("onclick")
                print(str)
                number = re.findall(r'[^()]+',str)[1][5:-1]
                url_new = url+"?t=%s"%number
                return makeDict(url,url_new)

# 判断算法，根据用户对该书的评价，判断该用户的价值；最后更新字典
def judgement(new_dict):
    mean = sum(new_dict.values())/len(new_dict.values())
    list_value = list(new_dict.values())
    var = sum([(a-mean)*(a-mean) for a in list_value])/len(list_value)+0.1
    length = len(new_dict.values())
    if new_dict[book_name] == 5:
        return 100*var*(5-mean)
    elif new_dict[book_name] == 4:
        if length > 30:
            return 40*var*(4-mean)
        else:
            return 80*var*(5-mean)

def refreshDict(new_dict,dict,parameter):
    for key in new_dict.keys():
        if key in dict.keys():
            dict[key] += parameter
        else:
            dict[key] = parameter

# 主函数
if __name__ == '__main__':
    for i in user_list:
        url = "http://www.yousuu.com/user/%d/comments"%i
        url_new = url
        new_dict = {}
        makeDict(url,url_new)
        parameter = judgement(new_dict)
        refreshDict(new_dict,dict,parameter)
