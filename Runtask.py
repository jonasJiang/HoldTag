# _*_ coding: utf-8 _*_
"""
__project__ = 'AUTOTAG'
__file_name__ = 'Runtask'
__author__ = 'sudoskys'
__time__ = '2022/2/11 下午9:45'
__product_name__ = 'PyCharm'
__version__ = '2月112145'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""

print("第一次使用猎人请请修改此文件：data/run.yaml来指定队列，然后取消注释：Runtask.py：line 36-45")

import logging.config

from Hunter01 import checker
from mods.Tool import useTool
from mods.tasker import tasker

logging.config.fileConfig("logger.conf")
logger = logging.getLogger('justConsole')
# tasker().clearTask()


'''
dat = useTool().rData("data/run.yaml")
for k, item in (dat.items()):
    # dat['runset']['key'] =  # 过滤词汇
    setting = item.get('runset')
    logging.info(setting)
    result = checker().search_run(item.get('data'), setting)
    # result 数据和两个关键词
    if result:
       tasker().doData(result)
'''

'''
tasker api
'''
# 筛选后的结果
# tasker().clearTask(folder='doData')
