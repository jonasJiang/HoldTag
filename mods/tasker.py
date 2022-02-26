# _*_ coding: utf-8 _*_
"""
__project__ = 'AUTOTAG'
__file_name__ = 'tasker'
__author__ = 'sudoskys'
__time__ = '2022/2/12 下午9:11'
__product_name__ = 'PyCharm'
__version__ = '2月122111'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""
import logging.config
from mods.Tool import useTool

logging.config.fileConfig("logger.conf")
logger = logging.getLogger('justConsole')


class tasker(object):
    def __init__(self):
        self.debug = True

    def clearTask(self, files=None, folder='auto/queue'):
        if files is None:
            files = []
        import os
        file_list = os.listdir(
            os.path.abspath(os.path.dirname(useTool().filesafer('data/' + folder + '/init.yaml'))))  # 获取当前文件夹内所有文件名
        for file in file_list[::-1]:  # 逆序遍历
            if file.endswith('.yaml'):  # 判断文件的扩展名
                pass
            else:
                file_list.remove(file)  # 过滤文件
        logging.debug(file_list)
        try:
            for i, k in enumerate(file_list):
                ok = useTool().filesafer('data/' + folder + '/' + k)
                files.append(ok)
                os.remove(ok)
            if folder == "auto/queue":
                os.remove(useTool().filesafer("data/queue_rank.yaml"))
        except Exception as err:
            logging.error(err)
        else:
            pass

    def raiseTask(self, deal, key):
        import time
        date = str(time.strftime("%Y%m%d%H%M", time.localtime()))
        date = key
        if deal:
            useTool().sData("data/auto/queue/" + date + ".yaml", deal)
            info = useTool().rData("data/queue_rank.yaml")
            if not info:
                info = {}
            info[date] = useTool().filesafer("data/auto/queue/" + date + ".yaml")
            useTool().sData("data/queue_rank.yaml", info)
        return date

    def cancelTask(self, keys, save=False):
        import os
        info = useTool().rData("data/queue_rank.yaml")
        if info:
            path = info.get(keys)
            if os.path.exists(path):
                if not save:
                    os.remove(path)
                if info.pop(keys):
                    useTool().sData("data/queue_rank.yaml", info)

    def doData(self, dat):
        """
        param newer: 'data'= result, 'key'= runSet.get("key"), 'type'= 'search'
        :return:
        """
        newer = dat.get('data')
        older = useTool().rData("data/doData/" + dat.get('key') + ".yaml")
        if not older:
            older = {}
        if isinstance(newer, dict):
            # logging.debug(older)
            if len(list(older)) != 0:
                deal = {i: newer.get(i) for i in newer.keys() if i not in older.keys()}
                older.update(newer)
                total = older
            else:
                total = newer
                deal = newer
            useTool().sData("data/doData/" + dat.get('key') + ".yaml", total)
            # logging.debug(deal)
            # 注册任务
            keys = self.raiseTask(deal, dat.get('key'))
            return keys
        else:
            logger.info("NEED DICT")
            return False
