# _*_ coding: utf-8 _*_
"""
__project__ = 'AUTOTAG'
__file_name__ = 'snownlp'
__author__ = 'sudoskys'
__time__ = '2022/2/13 下午7:26'
__product_name__ = 'PyCharm'
__version__ = '2月131926'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""

from snownlp import SnowNLP
'''exp
确实是，魔怔网友比较多，以前看holo的mmr也喜欢冲，美其名曰我看holo不妨碍我骂罕见，v8主要冲的府系的
只是个画画的 视频内容其实也没有真的在评价什么 比起主播我还是dd更多 本质表达自己对于有实力的姑娘们的喜爱
第一步，去V8点个炮仗，第二步，抗压 啊对对对 你们网暴我！第三步 火了~
我什么时候D的三观这么正的V？能D你真是太好了[原神_喝茶]
v跟观众总得有个是巨婴才能火。人人都讨厌饭圈，但是人人又都是饭圈。
'''


text = u'''确实是，魔怔网友比较多，以前看holo的mmr也喜欢冲，美其名曰我看holo不妨碍我骂罕见，v8主要冲的府系的
只是个画画的 视频内容其实也没有真的在评价什么 比起主播我还是dd更多 本质表达自己对于有实力的姑娘们的喜爱
第一步，去V8点个炮仗，第二步，抗压 啊对对对 你们网暴我！第三步 火了~
我什么时候D的三观这么正的V？能D你真是太好了[原神_喝茶]
v跟观众总得有个是巨婴才能火。人人都讨厌饭圈，但是人人又都是饭圈。
'''

print(SnowNLP(u'').sentiments)




