# _*_ coding: utf-8 _*_
"""
__project__ = 'AUTOTAG'
__file_name__ = 'sampleDeal'
__author__ = 'sudoskys'
__time__ = '2022/2/13 上午10:55'
__product_name__ = 'PyCharm'
__version__ = '2月131055'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""

import logging.config
import os
import time

import pandas as pd
from matplotlib import colors

logging.config.fileConfig("logger.conf")
logger = logging.getLogger('justConsole')
from mods.Tool import useTool


class cloud(object):
    def __init__(self):
        pass

    @staticmethod
    def convert_html_to_pdf(source_html, output_filename):
        from xhtml2pdf.default import DEFAULT_FONT
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfbase import pdfmetrics
        from xhtml2pdf import pisa
        # open output file for writing (truncated binary)
        result_file = open(output_filename, "w+b")

        pdfmetrics.registerFont(TTFont('yh', 'SimHei.ttf'))
        DEFAULT_FONT['helvetica'] = 'yh'
        # convert HTML to PDF

        pisa_status = pisa.CreatePDF(
            source_html,  # the HTML to convert
            dest=result_file)  # file handle to recieve result

        # close output file
        result_file.close()  # close output file

        # return False on success and True on errors
        return pisa_status.err

    @staticmethod
    def jsonReader(file_dir):
        all_data_frame = None
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
                else:  # concatenate all json to a single dataframe, ignore index
                    all_data_frame = pd.concat([all_data_frame, single_data_frame], ignore_index=True)
        return all_data_frame

    @staticmethod
    def moodFind(file_dir, ids):
        from snownlp import SnowNLP
        con = cloud.jsonReader(file_dir)
        lists = list(con['reply_content'])
        for item in lists:
            point = SnowNLP(item).sentiments
            if point > 0.5:
                print(item + ' --GOOD-- ' + str(point))
            else:
                print(item + ' --BAD-- ' + str(point))

                # t-o-d-o--

    @staticmethod
    def drawCloud(file_dir, ids):
        import jieba.analyse
        from wordcloud import WordCloud, STOPWORDS
        from PIL import Image
        import numpy as np
        _dir = os.path.dirname(file_dir)
        con = cloud.jsonReader(file_dir)
        lists = list(con['reply_content'])
        text = (".".join(lists))
        text = jieba.analyse.textrank(text, topK=50, withWeight=True)
        result = {}
        color_list = ['#CD853F', '#DC143C', '#00FF7F', '#FF6347', '#8B008B', '#00FFFF', '#0000FF', '#8B0000', '#FF8C00',
                      '#1E90FF', '#00FF00', '#FFD700', '#008080', '#008B8B', '#8A2BE2', '#228B22', '#FA8072', '#808080']
        colormap = colors.ListedColormap(color_list)
        for lists in text:
            result[lists[0]] = lists[1]
        for line in open("stopwords.txt", "r").readlines():
            line = line.strip('\n')
            STOPWORDS.add(line)
        font = r'SimHei.ttf'
        image = Image.open('cloud.jpg')
        mask = np.array(image)
        wc = WordCloud(
            font_path=font,  # 使用的字体库
            margin=2,
            mask=mask,  # 背景图片
            background_color='white',  # 背景颜色
            max_font_size=150,
            # min_font_size=1,
            max_words=200,
            colormap=colormap,  # 设置文字颜色
            stopwords=STOPWORDS,  # 屏蔽的内容
            random_state=30,
        )
        wc.generate_from_frequencies(result)  # 制作词云
        wc.to_file(useTool().filesafer('data/poster/' + ids + '/clouder.jpg'))  # 保存到当地文件
        return useTool().filesafer('data/poster/' + ids + '/clouder.jpg')

    @staticmethod
    def mdPdf(input_filename,output_filename):
        from xhtml2pdf import pisa
        from markdown import markdown
        with open(input_filename, encoding='utf-8') as f:
            text = f.read()
        source_html = markdown(text, output_format='html')  # MarkDown转HTML
        pisa.showLogging()
        cloud.convert_html_to_pdf(source_html, output_filename)

    @staticmethod
    def mdPoster(file_dir, ids, tar):
        # 计算
        from datetime import datetime
        date01 = datetime.today()
        timedate = str(date01.year) + '-' + str(date01.month) + '-' + str(date01.day)

        all_data_frame = cloud.jsonReader(file_dir)
        totalreplyers = all_data_frame.drop_duplicates(subset=['reply_name'])
        totalreplys = len(all_data_frame)
        loc = all_data_frame['reply_name'].value_counts()
        loc40 = loc[:40]
        loc20 = loc[:20].keys()
        loc20d = loc[:20]
        lastsave = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() + 28800))
        path = useTool().filesafer('data/poster/' + ids + '/【' + timedate + '节奏分析】.md')
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
                    '  **' + ltop20['reply_name'].iloc[k] + '**  发表于  ' + str(
                        ltop20['reply_time'].iloc[k]) + '  **' + str(
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
            for i in range(len(tar)):
                f.write(("> - %s - %s" % (i + 1, tar[i])) + '\n\n')
            print("分析完毕....")
        return path


'''pdf
#!pip install xhtml2pdf
from xhtml2pdf import pisa             # import python module
#!pip install markdown
from markdown import markdown

input_filename = '/content/data/poster/V圈队列/【2022-2-15节奏分析】.md'

with open(input_filename, encoding='utf-8') as f:
    text = f.read()

source_html = markdown(text, output_format='html')  # MarkDown转HTML
# print(source_html)
# Define your data
# source_html = "<html><body><p>To PDF or not to PDF</p></body></html>"
output_filename = "stests.pdf"

# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")
    from xhtml2pdf.default import DEFAULT_FONT
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    pdfmetrics.registerFont(TTFont('yh', 'SimHei.ttf'))
    DEFAULT_FONT['helvetica'] = 'yh'
    # convert HTML to PDF
    
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err

# Main program
if __name__ == "__main__":
    pisa.showLogging()
    convert_html_to_pdf(source_html, output_filename)
'''


