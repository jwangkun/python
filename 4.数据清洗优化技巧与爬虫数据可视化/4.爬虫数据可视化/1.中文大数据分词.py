# =============================================================================
# 6 第六讲：综合实战2 - 大数据分词与词云图绘制 by 王宇韬 代码更新&答疑交流微信：huaxz001
# =============================================================================

# 6.1 & 6.2 大数据分词与词频统计

import jieba  # 分词库，需要单独pip安装
from collections import Counter  # 自带的库，无需安装

# 1.读取文本内容，并利用jieba.cut功能来进行自动分词
report = open('信托行业报告.txt', 'r').read()  # 可以自己打印下report看一下，就是文本内容
words = jieba.cut(report)  # 将全文分割，获取到的是一个迭代器，需要通过for循环才能获取到里面的内容

# 2.通过for循环来提取words列表中4字以上的词语
report_words = []
for word in words:
    if len(word) >= 4:  # 将4字以上的词语放入列表
        report_words.append(word)
print(report_words)

# 3.获得打印输出高频词的出现次数
result = Counter(report_words).most_common(50)  # 取最多的50组
print(result)
