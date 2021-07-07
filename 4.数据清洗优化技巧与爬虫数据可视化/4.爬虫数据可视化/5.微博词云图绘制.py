# =============================================================================
# 6 第六讲：综合实战2 - 大数据分词与词云图绘制 by 王宇韬 代码更新&答疑交流微信：huaxz001
# =============================================================================

# 6.4 微博词云图绘制，如果暂时看不懂没有关系，我们在第8-9讲会讲解爬虫，这里初步了解即可。

import jieba  # 这个库需要单独pip安装下
from collections import Counter  # 这个库是自带的
from wordcloud import WordCloud, ImageColorGenerator  # 这个库需要单独pip安装下
from PIL import Image  # 这个库是自带的，如果没有的话，就pip安装下：pip install pillow
import numpy as np  # 这个库是自带的
from imageio import imread  # 这个库是自带的，用来读取图像
import requests
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

# 1.获取网页源代码
url = 'https://s.weibo.com/weibo?q=阿里巴巴'
res = requests.get(url, headers=headers, timeout=10).text

# 2.解析网页源代码提取信息
p_source = '<p class="txt" node-type="feed_list_content" nick-name="(.*?)">'
source = re.findall(p_source, res)
p_title = '<p class="txt" node-type="feed_list_content" nick-name=".*?">(.*?)</p>'
title = re.findall(p_title, res, re.S)

# 3.清洗 & 打印 & 汇总数据
title_all = ''  # 创建一个空字符串，用来汇总数据
for i in range(len(title)):
    title[i] = title[i].strip()
    title[i] = re.sub('<.*?>', '', title[i])
    title_all = title_all + title[i]  # 通过字符串拼接，汇总数据
    print(str(i + 1) + '.' + title[i] + '-' + source[i])

# 4.读取文本内容，并利用jieba.cut功能俩进行自动分词
words = jieba.cut(title_all)  # 将全文分割，获取到的是一个迭代器，需要通过for循环才能获取到里面的内容

# 5.通过for循环来提取words列表中大于2个字的词语
report_words = []
for word in words:
    if len(word) >= 2:
        report_words.append(word)
print(report_words)

# 6.获得打印输出高频词的出现次数
result = Counter(report_words).most_common(50)  # 取最多的50组
print(result)

# 7.绘制词云图（加上形状和颜色)
# 7.1 获取词云图形状参数mask
blackgroud_pic = '微博.jpg'
images = Image.open(blackgroud_pic)
maskImages = np.array(images)

# 7.2 绘制词云图
content = ' '.join(report_words)
wc = WordCloud(font_path='simhei.ttf',  # 字体，simhei是黑体的意思，电脑默认都有该字体
               background_color='white',  # 背景颜色
               width=1000,  # width是宽度，
               height=600,  # height是高度
               mask=maskImages  # 设置图片形状
               ).generate(content)

# 7.3 修改词云图的底层颜色，这个blackgroud_pic就是之前的背景图片
back_color = imread(blackgroud_pic)  # 读取图片
image_colors = ImageColorGenerator(back_color)  # 获取颜色
wc.recolor(color_func=image_colors)  # 词云图加上颜色

wc.to_file('微博内容词云图.png')
