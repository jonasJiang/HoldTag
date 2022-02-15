# _*_ coding: utf-8 _*_
"""
__project__ = 'AUTOTAG'
__file_name__ = 'Hunter02'
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

from mods.Tool import useTool
from mods.bili import bili

logging.config.fileConfig("logger.conf")
logger = logging.getLogger('justConsole')

import time
import random
import requests
import math
import json
from tqdm import tqdm

num = 0


def add_num():
    global num
    num += 1
    # print(num)
    return str(num)


def random_sleep(mu=4, sigma=1.1):
    """正态分布随机睡眠
    :param mu: 平均值
    :param sigma: 标准差，决定波动范围
    """
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu  # 太小则重置为平均值
    time.sleep(secs)


class dog(object):
    def __init__(self,UA):
        self.fail = False
        self.END = False
        logging.debug(UA)
        if not UA:
           UA='Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'
        '''
        '''
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
            'User-Agent': UA, # 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
            'Cookie': '1P_JAR=2022-02-09-02;SEARCH_SAMESITE=CgQIv5QB;ID=CgQIsv5QB0',
        }

    def failed_do(self):
        self.fail = True

    def getId(self, urls):
        bili_id, bili_type = bili().get_bili_id(urls)
        oid, gettype = bili().get_oid_type(bili_id, bili_type)
        if gettype == 11:
            get_url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=%s' % oid
            response = requests.get(get_url, headers=self.header)
            oid = response.json()['data']['card']['desc']['rid']
        return oid, gettype

    def get_stored_name(self, fileD):
        """
        获取文件中的json
        """
        try:
            with open(fileD, "r") as file_obj:
                name_lt = json.load(file_obj)
        except json.decoder.JSONDecodeError:
            logging.debug("NONONONO")
            name_lt = []
        # file_obj.close()
        return name_lt

    def back_run(self, clist, b_oid, IDS):
        save_path = useTool().filesafer('data/comment/' + str(IDS) + '/' + IDS + '-4.json')  # 每中断一次更新一次
        listed = self.get_stored_name(save_path)
        if listed:  # 追加写入
            logging.debug("合并...extend list")
            newer = [item for item in clist if item not in listed]
            # 在clist而不是listed
            listed = listed+newer
        else:
            listed = clist
        with open(save_path, "w", encoding='utf-8') as f:
            json.dump(listed, f, ensure_ascii=False, indent=4, separators=(',', ':'))

    def ok(self, comment_url):
        random_sleep(4)
        response = requests.get(comment_url, headers=self.header)
        if response.status_code == 200:
            return response
        else:
            self.failed_do()
            return False

    def run(self, k, **data):
        logging.info('newTask  --' + k)
        path = data.get("path")
        # 容器ID
        IDS = k  # useTool().rData(useTool().filesafer("data/run.yaml")).get(k, dict()).get('runset',dict()).get('id')
        dictS = useTool().rData(useTool().filesafer(path))
        for key, con in dictS.items():
            '''分发任务
            '''
            logging.info('newTask  --' + con.get('bvid'))
            burl = 'https://www.bilibili.com/video/' + con.get('bvid')
            Goid, Gtype = self.getId(burl)
            comment_url = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=%s&oid=%s&sort=1' % (Gtype, Goid)
            response = self.ok(comment_url)
            if response:
                count = response.json()['data']['page']['count']  # 评论总数
                page_count = math.ceil(int(count) / 20)  # 总页数
                logging.info('总页数为 --' + str(page_count) + '页  --大约需要' + str(page_count * 9) + 's')
                dat = {"page_count": page_count, "Gtype": Gtype, "Goid": Goid, 'title': con.get('title')}
                # 启动sub页面数据请求
                self.runsub(IDS, **dat)
            else:
                self.failed_do()
        return useTool().filesafer('data/comment/' + IDS + '/' + IDS + '-4.json'), list(dictS.keys()), self.fail

    def runsub(self, IDS, **data):
        page_count = data.get("page_count")
        Gtype = data.get("Gtype")
        Goid = data.get("Goid")
        title = data.get("title")
        comment_list = []
        n = 0
        # 某个页面
        for pn in range(1, page_count + 1):
            logging.info(" --开始第" + str(pn) + '页')
            comment_url = 'https://api.bilibili.com/x/v2/reply?pn=%s&type=%s&oid=%s&sort=1' % (pn, Gtype, Goid)
            response = self.ok(comment_url)
            if response:
                if 'data' in response.json().keys():
                    replies = response.json()['data']['replies']
                    if replies is not None:
                        for reply in tqdm(replies):
                            n = n + 1
                            # print('处理数' + add_num() + ' -拉取第' + str(n) + '条评论....')

                            reply_info = {
                                'reply_id': reply['member']['mid'],  # 评论者id,
                                'reply_name': reply['member']['uname'],  # 评论者昵称
                                'reply_time': bili().timestamp_datetime(int(reply['ctime'])),  # 评论时间
                                'reply_like': reply['like'],  # 评论点赞数
                                'reply_content': reply['content']['message']  # 评论内容
                            }
                            comment_list.append(reply_info)
                            rcount = reply['rcount']  # 表示回复的评论数
                            # print(str(rcount))
                            page_rcount = math.ceil(int(rcount) / 10)  # 回复评论总页数
                            root = reply['rpid']
                            data = {"page_rcount": page_rcount, "root": root, "Gtype": Gtype, "Goid": Goid,
                                    'title': title}
                            usedata = self.runthird(n, **data)
                            if usedata:
                                comment_list = comment_list + usedata
                        self.back_run(comment_list, Goid, IDS)
            else:
                logging.info("NO 200")
        return 'data/comment/' + str(Goid) + '-4.json'

    def runthird(self, n, **data):
        # {"page_rcount": page_rcount, "root": root,}
        page_rcount = data.get("page_rcount")
        root = data.get("root")
        Gtype = data.get("Gtype")
        Goid = data.get("Goid")
        m = 0
        # 回复
        comment_list = []
        for reply_pn in range(1, page_rcount + 1):
            m = m + 1
            # print('处理数' + add_num() + ' -拉取第 ' + str(n) + ' 条评论中的第' + str(m) + '条子评论..')
            # time.sleep(1.1)
            reply_url = 'https://api.bilibili.com/x/v2/reply/reply?&pn=%s&type=%s&oid=%s&ps=10&root=%s' % (
                reply_pn, Gtype, Goid, root)
            # response = requests.get(reply_url, headers=self.header)
            response = self.ok(reply_url)
            if response.status_code == 200:
                if 'data' in response.json().keys():
                    rreplies = response.json()['data']['replies']
                    if rreplies is not None:
                        for reply in rreplies:
                            # reply_id = reply['member']['mid']  # 评论者id
                            # reply_name = reply['member']['uname']  # 评论者昵称
                            # reply_time = timestamp_datetime(int(reply['ctime']))  # 评论时间
                            # reply_like = reply['like']  # 评论点赞数
                            # reply_content = reply['content']['message']  # 评论内容
                            reply_info = {
                                'reply_id': reply['member']['mid'],  # 评论者id,
                                'reply_name': reply['member']['uname'],  # 评论者昵称
                                'reply_time': bili().timestamp_datetime(int(reply['ctime'])),
                                # 评论时间
                                'reply_like': reply['like'],  # 评论点赞数
                                'reply_content': reply['content']['message']  # 评论内容
                            }
                            comment_list.append(reply_info)
        return comment_list


'''
def run(self, items):
    itemS: str
    dictS = useTool().rData(useTool().filesafer(items))
    for key, con in dictS.items():
        burl = 'https://www.bilibili.com/video/' + con.get('bvid')
        Goid, Gtype = self.getId(burl)
        comment_url = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=%s&oid=%s&sort=1' % (Gtype, Goid)
        response = requests.get(comment_url, headers=self.header)
        random_sleep(2)
        if response.status_code == 200:
            # print(response.json())
            count = response.json()['data']['page']['count']  # 评论总数
            page_count = math.ceil(int(count) / 20)  # 总页数
            logging.info('总页数为 --' + str(page_count) + '页  --大约需要' + str(page_count * 9) + 's')
            comment_list = []
            # 执行页面
            # 追加模式
            for pn in range(1, page_count + 1):
                logging.info(" --开始第" + str(pn) + '页')
                comment_url = 'https://api.bilibili.com/x/v2/reply?pn=%s&type=%s&oid=%s&sort=1' % (pn, Gtype, Goid)
                response = requests.get(comment_url, headers=self.header)
                random_sleep(2)
                if response.status_code == 200:
                    if 'data' in response.json().keys():
                        replies = response.json()['data']['replies']
                        if replies is not None:
                            n = 0
                            tot = 0
                            # 具体评论
                            for reply in replies:
                                tot = tot + 1
                                n = n + 1
                                print('处理数' + str(tot) + ' -拉取第' + str(n) + '条评论....')
                                ####
                                # reply_id = reply['member']['mid']
                                # reply_name = reply['member']['uname']
                                # reply_time = timestamp_datetime(int(reply['ctime']))  # 评论时间
                                # reply_like = reply['like']  # 评论点赞数
                                # reply_content = reply['content']['message']  # 评论内容
                                reply_info = {
                                    'reply_id': reply['member']['mid'],  # 评论者id,
                                    'reply_name': reply['member']['uname'],  # 评论者昵称
                                    'reply_time': bili().timestamp_datetime(int(reply['ctime'])),  # 评论时间
                                    'reply_like': reply['like'],  # 评论点赞数
                                    'reply_content': reply['content']['message']  # 评论内容
                                }
                                comment_list.append(reply_info)
                                rcount = reply['rcount']  # 表示回复的评论数
                                # print(str(rcount))
                                page_rcount = math.ceil(int(rcount) / 10)  # 回复评论总页数
                                root = reply['rpid']
                                m = 0
                                # 回复
                                for reply_pn in range(1, page_rcount + 1):
                                    m = m + 1
                                    tot = tot + 1
                                    print('处理数' + str(tot) + ' -拉取第' + str(n) + '条评论中的第' + str(m) + '条子评论..')
                                    time.sleep(1.1)
                                    reply_url = 'https://api.bilibili.com/x/v2/reply/reply?&pn=%s&type=%s&oid=%s&ps=10&root=%s' % (
                                        reply_pn, Gtype, Goid, root)
                                    response = requests.get(reply_url, headers=self.header)
                                    random_sleep(2)
                                    if response.status_code == 200:
                                        if ('data' in response.json().keys()):
                                            rreplies = response.json()['data']['replies']
                                            if rreplies is not None:
                                                for reply in rreplies:
                                                    # reply_id = reply['member']['mid']  # 评论者id
                                                    # reply_name = reply['member']['uname']  # 评论者昵称
                                                    # reply_time = timestamp_datetime(int(reply['ctime']))  # 评论时间
                                                    # reply_like = reply['like']  # 评论点赞数
                                                    # reply_content = reply['content']['message']  # 评论内容
                                                    reply_info = {
                                                        'reply_id': reply['member']['mid'],  # 评论者id,
                                                        'reply_name': reply['member']['uname'],  # 评论者昵称
                                                        'reply_time': bili().timestamp_datetime(int(reply['ctime'])),
                                                        # 评论时间
                                                        'reply_like': reply['like'],  # 评论点赞数
                                                        'reply_content': reply['content']['message']  # 评论内容
                                                    }
                                                    comment_list.append(reply_info)
                            self.runto(comment_list, Goid)

        else:
            logging.info("NO 200")
    return 'data/comment/' + str(Goid) + '-4.json'
'''
