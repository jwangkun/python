# =============================================================================
# 6 第六讲：综合实战2 - 大数据分词与词云图绘制 by 王宇韬 代码更新&答疑交流微信：huaxz001
# =============================================================================

# 6.3 词云图初步绘制

import jieba
from collections import Counter
from wordcloud import WordCloud

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

# 4.绘制词云图
content = ' '.join(report_words)  # 通过join()函数把列表转换成字符串(通过' '连接列表中的元素）
wc = WordCloud(font_path='simhei.ttf',  # 字体，simhei是黑体的意思，电脑默认都有该字体，simhei.ttf是黑体字体文件
               background_color='white',  # 背景颜色
               width=1000,  # 宽度
               height=600,  # 高度
               ).generate(content)  # 根据刚刚生成的content，generate成词云图
wc.to_file('词云图.png')  # 导出成png图片
