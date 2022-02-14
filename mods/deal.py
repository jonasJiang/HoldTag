# _*_ coding: utf-8 _*_
"""
__project__ = 'AUTOTAG'
__file_name__ = 'deal'
__author__ = 'sudoskys'
__time__ = '2022/2/12 下午9:45'
__product_name__ = 'PyCharm'
__version__ = '2月122145'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""
import os
import time

import pandas as pd

targetnow = False  # 定义即时分析，自动切换目录
githubvesion = 1103  # 此参数定义一天之中的提交版本，防止重复分析

# ---------------------------
# 时间拼接判定

from datetime import datetime

date01 = datetime.today()
timedate = str(date01.year) + '-' + str(date01.month) + '-' + str(date01.day)

import logging.config
logging.config.fileConfig("logger.conf")
logger = logging.getLogger('justConsole')
from mods.Tool import useTool


# ---------------------------------
def second(file_dir, target_list):
    print("开始分析...." + file_dir)
    if os.path.exists(file_dir):
        file_dir = os.path.dirname(file_dir)
    all_json_list = os.listdir(file_dir)  # get json list
    for single_json in all_json_list:
        if single_json.endswith('.json'):
            logging.debug(os.path.join(file_dir, single_json))
            single_data_frame = pd.read_json(useTool().filesafer(os.path.join(file_dir, single_json)))
            if single_json == all_json_list[0]:
                all_data_frame = single_data_frame
            else:  # concatenate all json to a single dataframe, ingore index
                all_data_frame = pd.concat([all_data_frame, single_data_frame], ignore_index=True)
    totalreplyers = all_data_frame.drop_duplicates(subset=['reply_name'])
    totalreplys = len(all_data_frame)
    loc = all_data_frame['reply_name'].value_counts()
    loc40 = loc[:40]
    loc20 = loc[:20].keys()
    loc20d = loc[:20]
    lastsave = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() + 28800))
    path = useTool().filesafer('data/poster/' + file_dir + '【' + timedate + '节奏分析】.md')
    with open(path.encode('utf-8'), 'w', encoding='utf-8') as f:
        f.write('# ' + timedate + '节奏分析\n\n')
        f.write('> # **本文件最后更新于' + str(lastsave) + '** \n\n')
        f.write('本次节奏，共有 **' + str(len(totalreplyers)) + '** 人参与，发表了 **' + str(totalreplys) + '** 个回复。\n\n\n')
        if int(totalreplys) < 20:
            num = int(totalreplys)
        else:
            num = 20

        if int(len(totalreplyers)) < 20:
            numer = int(len(totalreplyers))
        else:
            numer = 20

        f.write('# 按照回复次数进行划分，与人数的对应关系如下表所示：\n\n')
        loccount = loc.value_counts(bins=10)
        loccount.name = '人数'
        loccount.index.name = '回复次数'
        f.write(loccount.to_markdown() + '\n\n')
        f.write('# 其中，最活跃的人(<41)相关回复次数如下表所示：\n\n')
        loc40.name = '回复次数'
        loc40.index.name = '昵称'
        f.write(loc40.to_markdown() + '\n\n')
        f.write('## 按照点赞数排序，这' + str(len(totalreplyers)) + '人的回复中，被点赞前' + str(num) + '条分别是： \n\n')
        top40 = all_data_frame.loc[all_data_frame['reply_name'].isin(loc40.index)]
        top40likes = top40.sort_values(by='reply_like', ascending=False)
        top40likes20 = top40likes[:20]
        for k in range(num):
            f.write('  **' + top40likes20['reply_name'].iloc[k] + '**  发表于  ' + str(
                top40likes20['reply_time'].iloc[k]) + ' **' + str(
                top40likes20['reply_like'].iloc[k]) + '** 赞：' + '\n\n')
            f.write('<blockquote> ' + top40likes20['reply_content'].iloc[k] + '</blockquote>\n\n\n')
            f.write('-----\n\n')
        f.write('# 接下来，让我们看看前 ' + str(numer) + ' 回复者的具体动态：\n\n')
        for i in range(numer):
            person = all_data_frame.loc[all_data_frame['reply_name'] == loc20[i]]
            plikes = person.sort_values(by='reply_like', ascending=False)
            plikes5 = plikes[:5]
            f.write('## 第' + str(i + 1) + '名： **' + loc20[i] + '** \n\n')
            f.write('TA一共回复了 **' + str(loc20d[i]) + '** 条消息，在 **' + str(len(totalreplyers)) + '** 人中勇夺第 **' + str(
                i + 1) + '** ！ \n\n')
            if int(loc20d[i]) < 5:
                numm = int(loc20d[i])
            else:
                numm = 5

            f.write('### 按照点赞数排序，TA回复被点赞前' + str(numm) + '条分别是： \n\n')
            for k in range(numm):
                f.write(' 发表于' + str(plikes5['reply_time'].iloc[k]) + ' **' + str(
                    plikes5['reply_like'].iloc[k]) + '** 赞：' + '\n\n')
                f.write('<blockquote> ' + plikes5['reply_content'].iloc[k] + '</blockquote>\n\n\n')
                f.write('-----\n\n')
        f.write('# 最后，让我们来看一下点赞前' + str(numer) + '的评论：\n\n')
        ltop20 = all_data_frame.sort_values(by='reply_like', ascending=False)[:20]
        for k in range(numer):
            f.write(
                '  **' + ltop20['reply_name'].iloc[k] + '**  发表于  ' + str(ltop20['reply_time'].iloc[k]) + '  **' + str(
                    ltop20['reply_like'].iloc[k]) + '** 赞：' + '\n')
            f.write('<blockquote> ' + ltop20['reply_content'].iloc[k] + '</blockquote>\n\n\n')
            f.write('-----\n\n')
        f.write('# 特别颁发的奖项\n\n')
        f.write('## 抛砖引砖奖：\n\n')
        f.write('在楼中楼里被他人回复最多次。\n\n')
        rreply = all_data_frame[all_data_frame['reply_content'].str.contains('回复 @.+ ?')]
        rrstars = rreply['reply_content'].str.extract(r'(@.+:)')
        rrstar = rrstars.value_counts()[:10]
        rrstar.name = '回复次数'
        rrstar.index.name = '昵称'
        f.write(rrstar.to_markdown() + '\n\n')
        f.write('-----\n\n')
        f.write('## 你说你EMOJI呢奖：\n\n')
        f.write('被使用最多次的B站表情（不含emoji）。\n\n')
        emotes = all_data_frame[all_data_frame['reply_content'].str.contains('\[.+?\]')]
        emotes = emotes['reply_content'].str.extract(r'(\[.+?\])')
        emote = emotes.value_counts()[:10]
        emote.name = '使用次数'
        emote.index.name = '表情名称'
        f.write(emote.to_markdown() + '\n\n')
        f.write('-----\n\n')
        f.write('## 谈笑风生奖：\n\n')
        f.write('发送带表情的评论最多条数。\n\n')
        pemotes = all_data_frame[all_data_frame['reply_content'].str.contains('\[.+?\]')]
        pemote = pemotes['reply_name'].value_counts()[:10]
        pemote.name = '带表情评论条数'
        pemote.index.name = '昵称'
        f.write(pemote.to_markdown() + '\n\n')
        f.write('-----\n\n')
        f.write('# 本次数据统计的采样来源：' + '\n\n')
        for i in range(len(target_list)):
            f.write(("> - %s - %s" % (i + 1, target_list[i])) + '\n\n')
        print("分析完毕....")
    return path


'''
        for thread in threads:
            if(thread['mode'] == 'repost' or thread['mode'] == 'post'):
                f.write(' https://t.bilibili.com/'+str(thread['oid'])+'\n\n')
            elif(thread['mode'] == 'cv'):
                f.write(' https://www.bilibili.com/read/cv'+str(thread['oid'])+'\n\n')
            elif(thread['mode'] == 'av'):
                f.write(' https://www.bilibili.com/video/av'+str(thread['oid'])+'\n\n')
'''
