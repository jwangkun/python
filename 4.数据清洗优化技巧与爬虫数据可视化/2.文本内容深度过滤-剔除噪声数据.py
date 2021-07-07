# =============================================================================
# 5.1 数据去重及清洗优化 by 王宇韬 代码更新：www.huaxiaozhi.com 资料下载区
# =============================================================================

import requests
import re
import pymysql
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}


def baidu(company):
    # 1.获取网页源代码
    url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + company  # 其中设置rtt=4则为按时间排序，如果rtt=1则为按焦点排序
    res = requests.get(url, headers=headers, timeout=10).text

    # 2.编写正则提炼内容
    p_href = '<h3 class="news-title_1YtI1"><a href="(.*?)"'
    href = re.findall(p_href, res, re.S)
    p_title = '<h3 class="news-title_1YtI1">.*?>(.*?)</a>'
    title = re.findall(p_title, res, re.S)
    p_date = '<span class="c-color-gray2 c-font-normal">(.*?)</span>'
    date = re.findall(p_date, res)
    p_source = '<span class="c-color-gray c-font-normal c-gap-right">(.*?)</span>'
    source = re.findall(p_source, res)

    # 3.数据清洗
    for i in range(len(title)):
        title[i] = title[i].strip()  # strip()函数用来取消字符串两端的换行或者空格，不过目前（2020-10）并没有换行或空格，所以其实不写这一行也没事
        title[i] = re.sub('<.*?>', '', title[i])  # 核心，用re.sub()函数来替换不重要的内容
        # 统一日期格式（参考5.1节）
        date[i] = date[i].split(' ')[0]  # 提取2020年11月15日 10:26:22前面的年月日信息
        date[i] = re.sub('年', '-', date[i])  # 换成2020-11-15格式，注意只需要换年和月即可，日换成空值即可
        date[i] = re.sub('月', '-', date[i])
        date[i] = re.sub('日', '', date[i])
        if ('小时' in date[i]) or ('分钟' in date[i]):
            date[i] = time.strftime("%Y-%m-%d")
        else:
            date[i] = date[i]

    # 4.正文爬取及数据深度清洗
    for i in range(len(title)):
        # 获取新闻正文
        try:
            article = requests.get(href[i], headers=headers, timeout=10).text
        except:
            article = '单个新闻爬取失败'

        # 正文信息再优化
        p_article = '<p.*?>(.*?)</p>'  # 有的时候p标签里可能还有class属性，例如<p class='main_content'>，通过.*?代替<p>标签中可能变化的内容
        article_main = re.findall(p_article, article)  # 获取<p>标签里的正文信息
        article = ' '.join(article_main)  # 将列表转换成字符串，通过空格连接

        # 数据深度清洗
        company_re = company[0] + '.{0,5}' + company[-1]  # 匹配“公司名称第一个字 + 0到5个任意字符 + 公司最后一个字”这样的匹配规则
        if len(re.findall(company_re, article)) < 1:
            title[i] = ''
            source[i] = ''
            href[i] = ''
            date[i] = ''
    while '' in title:
        title.remove('')
    while '' in href:
        href.remove('')
    while '' in date:
        date.remove('')
    while '' in source:
        source.remove('')

    # 5.打印清洗后的数据
    for i in range(len(title)):
        print(str(i + 1) + '.' + title[i] + '(' + date[i] + ' ' + source[i] + ')')
        print(href[i])


# 6.批量爬取多家公司
companys = ['华能信托', '阿里巴巴', '百度集团', '腾讯', '京东']
for company in companys:
    try:
        baidu(company)
        print(company + '数据爬取并导入数据库成功')
    except:
        print(company + '数据爬取并导入数据库失败')
