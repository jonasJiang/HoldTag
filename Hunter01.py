# _*_ coding: utf-8 _*_
"""
__project__ = 'AUTOTAG'
__file_name__ = 'Hunter01'
__author__ = 'sudoskys'
__time__ = '2022/2/11 下午9:11'
__product_name__ = 'PyCharm'
__version__ = '2月112111'
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
import time
import random


def random_sleep(mu=4, sigma=1.7):
    """正态分布随机睡眠
    :param mu: 平均值
    :param sigma: 标准差，决定波动范围
    """
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu  # 太小则重置为平均值
    time.sleep(secs)


class checker(object):

    def __init__(self):
        self.END = False
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Referer': 'https://api.bilibili.com/',
            'Connection': 'keep-alive',
            'Host': 'api.bilibili.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
            'Cookie': '1P_JAR=2022-02-09-02;SEARCH_SAMESITE=CgQIv5QB;ID=CgQIsv5QB0',
        }

    def getThing(self, urls, dat):
        import json
        import requests
        response = requests.get(url=urls, params=dat, headers=self.header)
        if response.status_code == 200:
            content = response.text
            json_dicts = json.loads(content)
            # logger.debug(json_dict)
            if json_dicts.get('message') == "0":
                if json_dicts.get('data').get("result"):
                    return json_dicts.get('data').get("result")
                else:
                    logger.info("NO data" + str(json_dicts))
                    self.END = True
                    return False
            else:
                logger.debug("NO Data Code" + str(json_dicts))
                return False
        else:
            logger.debug("NET CODE  " + str(response.status_code))
            return False

    def search_run(self, datas, run_set):
        """
        :param run_set:
        :param datas:
        :return:
        """
        URL = "http://api.bilibili.com/x/web-interface/search/type"
        keywords = run_set.get("key")
        run_id = run_set.get("id")
        result = {}
        '''
        页数设置
        '''
        for i in range(1, 15):
            datas['page'] = i
            logging.info("working... --" + str(i))
            random_sleep(7)
            res = self.getThing(URL, datas)
            # 筛查
            if not res:
                print('fail to get page')
            for index, item in enumerate(res):
                video_object = {}
                title = item.get("title")
                titles = title.replace('<em class="keyword">', '').replace('</em>', '')
                char = '\:*?"<>|/'
                for acao in char:
                    titles = titles.replace(acao, "_")
                # logging.debug(titles)
                video_object['title'] = titles
                video_object['bvid'] = item.get("bvid")
                video_object['review'] = item.get("review")
                video_object['favorites'] = item.get("favorites")
                video_object['play'] = item.get("play")
                video_object['like'] = item.get("like")
                video_object['tag'] = item.get("tag")
                # 条件筛查
                atitle = {i for i in keywords if i in video_object['title']}
                atag = {i for i in keywords if i in video_object['tag']}
                if len(atitle) != 0 or len(atag) != 0:
                    # logging.debug("HI... --" + video_object['bvid'])
                    if video_object['review'] > 100:
                        result[video_object['bvid']] = video_object
                        logging.info("Insert... --" + video_object['title'] +" --" +video_object['bvid'])

        logger.debug(result)
        if result:
            resD = {'data': result, 'keyword': datas.get('keyword'), 'key': str(run_id), 'type': 'serach'}
            return resD
        else:
            return False
