# =============================================================================
# 5.3 舆情评分系统搭建 by 王宇韬 代码更新：www.huaxiaozhi.com 资料下载区
# =============================================================================

import requests  # 首先导入requests库和正则表达式re库
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}


'''舆情评分系统 - 通过新闻标题和新闻正文来进行评分'''
def baidu(company):
    url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + company  # 其中设置rtt=4则为按时间排序，如果rtt=1则为按焦点排序
    res = requests.get(url, headers=headers).text
    # print(res)

    # 正则表达式编写，这边为了代码简洁，只演示了标题和链接（正则更新）
    p_href = '<h3 class="news-title_1YtI1"><a href="(.*?)"'
    href = re.findall(p_href, res, re.S)
    p_title = '<h3 class="news-title_1YtI1">.*?>(.*?)</a>'
    title = re.findall(p_title, res, re.S)

    # 舆情评分版本2
    score = []
    keywords = ['违约', '诉讼', '兑付', '阿里', '百度', '京东', '互联网']  # 这个关键词列表可以自己定义，这里只是为了演示
    for i in range(len(title)):
        num = 0
        # 版本2:获取新闻正文
        try:
            article = requests.get(href[i], headers=headers, timeout=10).text
        except:
            article = '爬取失败'
        for k in keywords:
            if (k in article) or (k in title[i]):
                num -= 5  # 也可以写成 num = num -5
        score.append(num)

    for i in range(len(title)):
        title[i] = title[i].strip()  # strip()函数用来取消字符串两端的换行或者空格，不过目前（2020-10）并没有换行或空格，所以其实不写这一行也没事
        title[i] = re.sub('<.*?>', '', title[i])  # 核心，用re.sub()函数来替换不重要的内容
        print(str(i + 1) + '.' + title[i])
        print(company + '该条新闻舆情评分为' + str(score[i]))  # 这边注意，不要写score[i]，因为它是数字，需要通过str()函数进行字符串拼接
        print(href[i])
    print('——————————————————————————————')  # 这个是当分隔符使用


companys = ['阿里巴巴', '万科集团', '百度']
for i in companys:
    try:
        baidu(i)
        print(i + '该公司百度新闻爬取成功')
    except:
        print(i + '该公司百度新闻爬取失败')



