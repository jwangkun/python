# =============================================================================
# 6 第六讲：综合实战2 - 大数据分词与词云图绘制 by 王宇韬 代码更新&答疑交流微信：huaxz001
# =============================================================================

# 6.3 词云图初步绘制 + 绘制特定形状

import jieba  # 这个库需要单独pip安装下
from collections import Counter  # 这个库是自带的
from wordcloud import WordCloud  # 这个库需要单独pip安装下
from PIL import Image  # 这个库是自带的，如果没有的话，就pip安装下：pip install pillow
import numpy as np  # 这个库是自带的

# 1.读取文本内容，并利用jieba.cut功能俩进行自动分词
report = open('信托行业报告.txt', 'r').read()
words = jieba.cut(report)  # 将全文分割，获取到的是一个迭代器，需要通过for循环才能获取到里面的内容

# 2.通过for循环来提取words列表中大于4个字的词语
report_words = []
for word in words:
    if len(word) >= 4:
        report_words.append(word)
print(report_words)

# 3.获得打印输出高频词的出现次数
result = Counter(report_words).most_common(50)  # 取最多的50组
print(result)

# 获取词云图形状参数mask
blackgroud_pic = '微博.jpg'
images = Image.open(blackgroud_pic)
maskImages = np.array(images)  # 将图片转为数字格式，感兴趣的可以打印它看看
print(maskImages)

content = ' '.join(report_words)
wc = WordCloud(font_path='simhei.ttf',  # 字体，simhei是黑体的意思，电脑默认都有该字体
               background_color='white',  # 背景颜色
               width=1000,  # width是宽度，
               height=600,  # height是高度
               mask=maskImages  # 设置图片形状（mask其实就面具的意思，所以类似于一个遮罩）
               ).generate(content)
wc.to_file('词云图+自定义形状.png')
