# =============================================================================
# 3. 新浪财经数据挖掘实战 by 王宇韬 代码更新&答疑交流微信：huaxz001
# =============================================================================

import requests
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

# 1.获取网页源代码
url = 'https://s.weibo.com/weibo?q=阿里巴巴'
res = requests.get(url, headers=headers).text
# print(res)

# 2.解析网页源代码提取信息
p_source = '<p class="txt" node-type="feed_list_content" nick-name="(.*?)">'
source = re.findall(p_source, res)
p_title = '<p class="txt" node-type="feed_list_content" nick-name=".*?">(.*?)</p>'
title = re.findall(p_title, res, re.S)

# 3.清洗 & 打印数据
for i in range(len(title)):
    title[i] = title[i].strip()
    title[i] = re.sub('<.*?>', '', title[i])
    print(str(i + 1) + '.' + title[i] + '-' + source[i])
