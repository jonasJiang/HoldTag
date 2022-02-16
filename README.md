## HoldTag

[![](https://gitlab.com/45iron/holdtag/-/raw/main/cover.png)](https://gitlab.com/45iron/holdtag)


[![Apache License](https://img.shields.io/badge/LICENSE-Apache-ff69b4)](LICENSE)   ![u](https://img.shields.io/badge/USE-python-green)   [![s](https://img.shields.io/badge/Sponsor-Alipay-ff69b4)](https://afdian.net/@dosometh)

![v](https://img.shields.io/badge/Version-220215-9cf)




>About English Readme: This project lacks English documentation, contributions are welcome

>Q: why not use 爬虫框架? A:写完了才想到

## 目录

- 介绍
- 开始
- 实现逻辑
- TODO
- 鸣谢
- 附录(效果附)

## 介绍

注册多关键词监控组，多队列监控BiliBili的关键词搜索结果。

自动注册队列，唤醒爬取分析模块生成词云，情感判断，节奏分析报告。

多视频合并分析，快速分析节奏所在。

使用自训练情感模型，主要分析虚拟主播受众。

>项目仍在开发，出现问题请提交issue

### 特性

模块化功能，大量使用类，实际最短实现代码不超过十行。



### 注意

⚠ 爬取时请考虑Robot协议

⚠ 本项目仅仅用于提供舆情解决方案，不提供实际产品;如果违规项目使用本项目源代码，本项目不负责任。

⚠ 本项目样例数据为测试生成且仅供测试，仓库不提供服务。


## 开始
### 1. 安装要求

 **Python 3.7 或更高版本**
```
python -m pip install --upgrade pip

pip install -r requirements.txt
```


### 2. 准备

```
── clouder.jpg
├── cloud.jpg
├── data  //数据
│         ├── auto  //队列目录
│         ├── comment  //评论
│         ├── doData  //分析后总汇数据
│         ├── poster   //分析
│         ├── queue_rank.yaml   //队列索引
│         └── run.yaml  //任务器设置！
├── Runtask.py  //任务器
├── Diana.py    //分析器
├── Hunter01.py   //工具类
├── Hunter02.py   //工具类
├── logger.conf  //log moule
├── mods  //模块
│         ├── bili.py  //bili api tool
│         ├── deal.py  //no use
│         ├── __pycache__
│         ├── sampleDeal.py  //分析
│         ├── tasker.py  //任务队列
│         └── Tool.py   //通用类
├── note   //开发日志
│         └── soda.md
├── pos.txt
├── README.md
├── requirements.txt
├── running.log
├── sample  //训练数据源
│         ├── cloud.jpg.bak
│         ├── holoneg.txt
│         ├── only_vtuber
│         ├── pos2.txt
│         ├── sample.zip
│         └── vtuber_add_ylg
├── SimHei.ttf
├── snownlp  snownlp模块
│         ├── classification
│         ├── __init__.py
│         ├── normal
│         ├── __pycache__
│         ├── seg
│         ├── sentiment
│         ├── sim
│         ├── summary
│         ├── tag
│         └── utils
├── stopwords.txt 停用词


```



### 使用

填写并编写如下，目前仍在开发.....暂无提供成品部署
```
├── data  //数据
│         └── run.yaml  //任务器设置！
├── Runtask.py  //任务器
├── Diana.py    //分析器
```
设定完毕后运行器材即可，数据模块与分析模块是分割的，独立运行。

#### Colab运行
```commandline
!git clone https://gitlab.com/45iron/holdtag.git
!rsync -r /content/holdtag/* /content/
!python -m pip install --upgrade pip
!pip install -r requirements.txt

# 去修改文件

#可选
!pip install fake_useragent

!python /content/Runtask.py
!python /content/Diana.py

```


**关于情感模型训练**
情感模型训练为Snownlp自带的功能，语料库放在了sample文件夹。

负面语料取样来源为
- v吧(百度贴吧)
- 桐生会(BiliBili)

正面语料取样来源为
- Asoul二创
- Asoul混剪




## 实现逻辑


```
**猎人01**
读取设定，开始启动任务寻找。以对应{返回对象}
**猎人02**
爬取对象信息{返回对象}
**分发中心**
自检{接收对象，返回布尔值}（启动 01），插入任务队列，接收任务以及分拨任务对象（专栏或视频）。{接收对象，发送对象}
**数据中心**
接收日志信息，提供数据比对与任务队列功能
**分析中心**
分析上级对象，生成报告，存储档案（以个人为对象）
分析本身对象，生成成分报告，存储档案
```

[流程设计](note/soda.md)




## TODO
- [x] 实现数据模块
- [x] 实现队列
- [x] 实现多点监控
- [x] 实现独特数据模型
- [x] 实现猎人01/02
- [ ] 实现分析模块
- [ ] 实现完善的实例


## 鸣谢

- [节奏分析](https://github.com/TomoeMami/asoul-ttk-analysis)|pandas分析主类前身|
- [Snownlp](https://github.com/isnowfy/snownlp) |情感分析|
- [jieba](https://github.com/fxsjy/jieba) |Python 中文分词组件|


## 支持

THIS link: https://azz.net/ly233

[![s](https://img.shields.io/badge/Sponsor-Alipay-ff69b4)](https://afdian.net/@dosometh)



![counter](https://count.getloli.com/get/@45iron-gitlab-autotag?theme=moebooru)



------------------------------
## 附录

### 报告示例

请查看仓库内 sample/resultsample/ 文件夹


### 识别效果

```markdown
锐评很简单，想转回正常就难了[雪狐桑_吃桃] --GOOD-- 0.999962288490749
[珈乐Carol_哭哭]只是个画画的 视频内容其实也没有真的在评价什么 比起主播我还是dd更多 本质表达自己对于有实力的姑娘们的喜爱 --GOOD-- 0.9999999999559253
第一步，去V8点个炮仗，第二步，抗压 啊对对对 你们网暴我！第三步 火了~ --GOOD-- 0.6959719392264357
全给你玩明白了[tv_doge] --GOOD-- 0.7467406119698984
我超，有我捏[给心心] --GOOD-- 0.999978251062383
你可以一路黑到底 --GOOD-- 0.6731890684672779
[乃琳Queen_壁咚]三连了 我做的对嘛？[傲娇] --GOOD-- 0.9999999999412568
主播可不可以锐评我一下🥵🥵 --BAD-- 0.15272917154687504
太懂了[热词系列_知识增加] --GOOD-- 0.9999997904723056
的确是这样的， --GOOD-- 0.5619047619047621
这…实属是玩明白了[tv_doge] --GOOD-- 0.9668264665048504
爹！叠！跌！ --BAD-- 0.19382478492730904
玩明白了这是 --GOOD-- 0.7884917447996412
这互联网让你说明白了 --GOOD-- 0.9470845235007154
属于是把v圈玩明白了 --GOOD-- 0.9954899906622796
我什么时候D的三观这么正的V？能D你真是太好了[原神_喝茶] --GOOD-- 0.9994723161711713
哈哈哈哈 --GOOD-- 0.6909090909090911
桃太懂了也[热词系列_好活][热词系列_三连] --GOOD-- 1.0
叠buff是吧 --BAD-- 0.23663731966351875
属于是锐评了，但是评反了 --BAD-- 0.21166989890469257
你是懂V圈的 --GOOD-- 0.9564993673380858
既然玩明白了，什么时候再和妈妈一起直播一次哇[冰墩墩] --GOOD-- 0.9472503311758714
v跟观众总得有个是巨婴才能火。人人都讨厌饭圈，但是人人又都是饭圈。 --GOOD-- 0.9835222318474101
小贝😭😭我的小贝😭😭😭😭 --GOOD-- 0.9991243901277826
看到魔怔的v圈人我就想避而远之[脸红] --GOOD-- 0.9999653405756007
V87天天骂东雪莲罕见，结果自己推🌸👩🏻 --BAD-- 0.0002789030343807175
不汝不看[物述有栖_晚上好][物述有栖_晚上好] --GOOD-- 0.9999999999999285
错误的，不是v87骂的吧，不大多是mmr和魔怔人骂的嘛 --BAD-- 0.3693566297363653
最近v8比以前多了很多ylg --GOOD-- 0.9636711759116897
回复 @にゃる-闭翊白缳 :V8不好说，确实我观察了一段时间，对东雪莲有“滔天恨意”的都是魔怔网友跟ylg。 --BAD-- 0.03769690100492795
回复 @枝江知名网友 :确实是，魔怔网友比较多，以前看holo的mmr也喜欢冲，美其名曰我看holo不妨碍我骂罕见，v8主要冲的府系的 --BAD-- 0.000593677536100623
很抱歉以这种方式再次看到你，小贝😭😭，我的小贝😭😭 --GOOD-- 0.9826490886565317
小贝似了好久了[花园Serena2_哭] --GOOD-- 0.99785396268406
非常に不愉快です、そんな話をやめてください😤 --BAD-- 0.0021471968100283956
```

