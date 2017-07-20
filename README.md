# similar-book
查找龙空优书网中与我喜欢的书籍类似的书，分为两个py脚本
1. user_list.py
获取感兴趣读者名单列表，要注意的是这个名单是所有评论该书的人而不是评价，优书网中评价的信息不知道怎么获取。

2. test.py
对list中的读者进行分析，找出相似书籍，思路是这样的：我喜欢这本书，那么同样喜欢这本书的人对我的参考意见权重较大。那么如何判断谁跟我同样喜欢这本书呢，要根据每一个读者的平均打分和打分方差来判断，部分代码如下：
if new_dict[book_name] == 5:
        return 100*var*(5-mean)
    elif new_dict[book_name] == 4:
        if length > 30:
            return 40*var*(4-mean)
        else:
            return 80*var*(5-mean)

3. user_multiprocessing.py
写的过程中顺带着写的一个全用户信息爬取脚本。100多万个用户，哪怕用了多进程也要跑不止一天。
