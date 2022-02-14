# _*_ coding: utf-8 _*_
"""
__project__ = 'AUTOTAG'
__file_name__ = 'jieba_test'
__author__ = 'sudoskys'
__time__ = '2022/2/13 上午11:18'
__product_name__ = 'PyCharm'
__version__ = '2月131118'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""

import logging.config

logging.config.fileConfig("logger.conf")
logger = logging.getLogger('justConsole')
from mods.sampleDeal import cloud

import jieba
import jieba.analyse

'''exp
确实是，魔怔网友比较多，以前看holo的mmr也喜欢冲，美其名曰我看holo不妨碍我骂罕见，v8主要冲的府系的
只是个画画的 视频内容其实也没有真的在评价什么 比起主播我还是dd更多 本质表达自己对于有实力的姑娘们的喜爱
第一步，去V8点个炮仗，第二步，抗压 啊对对对 你们网暴我！第三步 火了~
我什么时候D的三观这么正的V？能D你真是太好了[原神_喝茶]
v跟观众总得有个是巨婴才能火。人人都讨厌饭圈，但是人人又都是饭圈。
'''
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np



con = cloud.jsonReader("data/636443862-4.json")
list = list(con['reply_content'])
text = (".".join(list))

text = jieba.analyse.textrank(text, topK=50, withWeight=True)
result = {}
for list in text:
    result[list[0]] = list[1]

# sep = jieba.lcut(text, cut_all=False)
# sep_list=" ".join(sep) #转为字符串
# print(sep)

font = r'SimHei.ttf'
mask = np.array(Image.open('cloud.jpg'))
wc = WordCloud(
    font_path=font,  # 使用的字体库
    margin=2,
    mask=mask,  # 背景图片
    background_color='white',  # 背景颜色
    max_font_size=200,
    # min_font_size=1,
    max_words=200,
    # stopwords=STOPWORDS, #屏蔽的内容
)

wc.generate_from_frequencies(result)  # 制作词云
wc.to_file('clouder.jpg')  # 保存到当地文件

#
# for x, w in jieba.analyse.extract_tags(sep_list, withWeight=True):
#       print('%s %s' % (x, w))

'''
    text:为待提取的文本;
    topK:返回几个TF/IDF权重最大的关键字,默认值为20;
    withWeight:是否一并返回关键词权重值,默认False;
'''

#
# seg_list = jieba.cut("确实是，魔怔网友比较多，以前看holo的mmr也喜欢冲，美其名曰我看holo不妨碍我骂罕见，v8主要冲的府系的", cut_all=False)
# print("【精确模式】：" + "/ ".join(seg_list))
#
# s = "确实是，魔怔网友比较多，以前看holo的mmr也喜欢冲，美其名曰我看holo不妨碍我骂罕见，v8主要冲的府系的"
# for x, w in jieba.analyse.extract_tags(s, withWeight=True):
#      print('%s %s' % (x, w))


# import sys
# sys.path.append("../")
#
# import jieba
# import jieba.posseg
# import jieba.analyse
#
# print('='*40)
# print('1. 分词')
# print('-'*40)
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list))  # 默认模式
#
# seg_list = jieba.cut("他来到了网易杭研大厦")
# print(", ".join(seg_list))
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print(", ".join(seg_list))
#
# print('='*40)
# print('2. 添加自定义词典/调整词典')
# print('-'*40)
#
# print('/'.join(jieba.cut('如果放到post中将出错。', HMM=False)))
# #如果/放到/post/中将/出错/。
# print(jieba.suggest_freq(('中', '将'), True))
# #494
# print('/'.join(jieba.cut('如果放到post中将出错。', HMM=False)))
# #如果/放到/post/中/将/出错/。
# print('/'.join(jieba.cut('「台中」正确应该不会被切开', HMM=False)))
# #「/台/中/」/正确/应该/不会/被/切开
# print(jieba.suggest_freq('台中', True))
# #69
# print('/'.join(jieba.cut('「台中」正确应该不会被切开', HMM=False)))
# #「/台中/」/正确/应该/不会/被/切开
#
# print('='*40)
# print('3. 关键词提取')
# print('-'*40)
# print(' TF-IDF')
# print('-'*40)
#
# s = "此外，公司拟对全资子公司吉林欧亚置业有限公司增资4.3亿元，增资后，吉林欧亚置业注册资本由7000万元增加到5亿元。吉林欧亚置业主要经营范围为房地产开发及百货零售等业务。目前在建吉林欧亚城市商业综合体项目。2013年，实现营业收入0万元，实现净利润-139.13万元。"
# for x, w in jieba.analyse.extract_tags(s, withWeight=True):
#     print('%s %s' % (x, w))
#
# print('-'*40)
# print(' TextRank')
# print('-'*40)
#
# for x, w in jieba.analyse.textrank(s, withWeight=True):
#     print('%s %s' % (x, w))
#
# print('='*40)
# print('4. 词性标注')
# print('-'*40)
#
# words = jieba.posseg.cut("我爱北京天安门")
# for word, flag in words:
#     print('%s %s' % (word, flag))
#
# print('='*40)
# print('6. Tokenize: 返回词语在原文的起止位置')
# print('-'*40)
# print(' 默认模式')
# print('-'*40)
#
# result = jieba.tokenize('永和服装饰品有限公司')
# for tk in result:
#     print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))
#
# print('-'*40)
# print(' 搜索模式')
# print('-'*40)
#
# result = jieba.tokenize('永和服装饰品有限公司', mode='search')
# for tk in result:
#     print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))
