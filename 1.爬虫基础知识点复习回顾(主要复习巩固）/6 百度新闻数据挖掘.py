# =============================================================================
# 3.1 百度新闻数据挖掘 by 王宇韬 代码更新&答疑交流微信：huaxz001
# =============================================================================

import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}


url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=阿里巴巴'  # 把链接中rtt参数换成4即是按时间排序，默认为1按焦点排序，3.4.1小节也有讲到
res = requests.get(url, headers=headers).text  # 加上headers用来告诉网站这是通过一个浏览器进行的访问
# print(res)

p_href = '<h3 class="news-title_1YtI1"><a href="(.*?)"'
href = re.findall(p_href, res)
p_title = '<h3 class="news-title_1YtI1">.*?>(.*?)</a>'
title = re.findall(p_title, res, re.S)

p_date = '<span class="c-color-gray2 c-font-normal">(.*?)</span>'
date = re.findall(p_date, res)
p_source = '<span class="c-color-gray c-font-normal c-gap-right">(.*?)</span>'
source = re.findall(p_source, res)

for i in range(len(title)):  # range(len(title)),这里因为知道len(title) = 10，所以也可以写成for i in range(10)
    title[i] = title[i].strip()  # strip()函数用来取消字符串两端的换行或者空格，不过这里好像不太需要了
    title[i] = re.sub('<.*?>', '', title[i])  # 核心，用re.sub()函数来替换不重要的内容
    print(str(i + 1) + '.' + title[i], source[i], date[i])  # print(1, 'hello') 这种写法，就是在同一行连续打印多个内容
    # print(str(i + 1) + '.' + title[i] + ' ' + source[i] + ' ' + date[i])  # 这个是纯字符串拼接
    print(href[i])

