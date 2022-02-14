# _*_ coding: utf-8 _*_
"""
__project__ = 'AUTOTAG'
__file_name__ = 'Diana'
__author__ = 'sudoskys'
__time__ = '2022/2/11 下午9:14'
__product_name__ = 'PyCharm'
__version__ = '2月112114'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""
# 模型
# 消极 BV1tB4y1c7F7
'''积极
BV1SF411z7HT
BV1kq4y1u7h7
BV1C3411b7Gg
BV1ca411k77e
BV1BZ4y1d7NY
'''

import logging.config
logging.config.fileConfig("logger.conf")
logger = logging.getLogger('justConsole')

from mods.tasker import tasker
from mods.Tool import useTool
from Hunter02 import dog
from mods.deal import second
from mods.sampleDeal import cloud



# Star = useTool().rData("data/queue_rank.yaml")
# if Star:
#     for k, item in (Star.items()):
#         road = str(item)
#         logging.info("启动任务 " + k + " --" + road)
#         info = {"path": road}
#         path, idlist, iserror = dog().run(k, **info)
#         if path:
#             print("完成")
#             # result_md = second(useTool().filesafer(path), idlist)
#             # tasker().cancelTask(k) # 取消任务
#         else:
#             logging.info("不通过")




# id = "k"
# fileDir = cloud.drawCloud("data/comment/202202122318/636443862-4.json", id)
# logging.debug(fileDir)


id = "k"
fileDir = cloud.moodFind("data/comment/202202122318/636443862-4.json", id)
logging.debug(fileDir)


# js = cloud.jsonReader("data/comment/asoul/asoul-4.json")
# lists = list(js['reply_content'])
# str = '\n'
# f=open("pos.txt","w")
# f.write(str.join(lists))
# f.close()


# 筛选后的结果
# tasker().clearTask(folder='doData')
# tasker().clearTask()
