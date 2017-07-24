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
user_list_file = r"D:\workspace\creeper\simboob\user_list_file1.txt"
user_list = open(user_list_file,"r",encoding="utf-8").readlines()
# user_list = [875164]
out_file = open(r"D:\workspace\creeper\simboob\out_file.txt","w")

# 遍历用户列表并更新子字典
def makeDict(url,url_new,new_dict):
    print(url_new)
    driver.get(url_new)
    html = driver.page_source
    bsObj = BeautifulSoup(html,"lxml")

    for link in bsObj.findAll("div",class_="booklist-item"):
        name = link.findAll("div",class_="title")[0].findAll("a")[0].get_text()
        if link.findAll("div",class_="abstract")[0].findAll("span",class_="num2star"):
            mark = link.findAll("div",class_="abstract")[0].findAll("span",class_="num2star")[0].findAll("i",style="color:#4D7BD6")
            new_dict[name] = len(mark)

    if bsObj.findAll("a",class_="btn btn-primary btn-block"):
        for button in bsObj.findAll("a",class_="btn btn-primary btn-block"):
            if button.get_text() == "点击加载下一页":
                str = button.get("onclick")
                number = re.findall(r'[^()]+',str)[1][5:-1]
                url_new = url+"?t=%s"%number
                makeDict(url,url_new,new_dict)

# 判断算法，根据用户对该书的评价，判断该用户的价值；最后更新字典
def judgement(new_dict):
    mean = sum(new_dict.values())/len(new_dict.values())
    list_value = list(new_dict.values())
    var = sum([(a-mean)*(a-mean) for a in list_value])/len(list_value)+0.1
    length = len(new_dict.values())
    if new_dict[book_name] == 5:
        return 5*var*(5-mean)
    elif new_dict[book_name] == 4:
        if length > 30:
            return 3*var*(4-mean)
        else:
            return 4*var*(5-mean)
    else:
        return 0

def refreshDict(new_dict,dict,parameter):
    if parameter != 0:
        for key in new_dict.keys():
            if key in dict.keys():
                dict[key] += parameter*new_dict[key]
            else:
                dict[key] = parameter*new_dict[key]

# 主函数
if __name__ == '__main__':
    for user in user_list:
        # 这个换行符差点坑死老子
        url = user.rstrip('\n')
        url_new = user
        new_dict = {}
        # try:
        makeDict(url,url_new,new_dict)
        parameter = judgement(new_dict)
        refreshDict(new_dict,dict,parameter)
        # except:
        #     print("error",url)
        dict_sort = sorted(dict.items(),key=lambda item:item[1])
    print(dict_sort)
    for key in dict_sort:
        out_file.write(key[0].replace(u'\xa0', u' ') + ' ' + str(key[1]).replace(u'\xa0', u' ') + '\n')
