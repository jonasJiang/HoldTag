## HoldTag

![counter](https://count.getloli.com/get/@45iron-gitlab-autotag?theme=moebooru)

[![Apache License](https://img.shields.io/badge/LICENSE-Apache-ff69b4)](LICENSE)   ![u](https://img.shields.io/badge/USE-python-green)   [![s](https://img.shields.io/badge/Sponsor-Alipay-ff69b4)](https://azz.net/ly233)
![v](https://img.shields.io/badge/Version-220209-9cf)


## 介绍

多队列监控bilibli的关键词结果，注册队列，唤醒爬取分析模块生成词云，情感判断，节奏分析报告。
支持多视频合并分析，多关键词规则监控。
使用自训练情感模型，为V圈打造。



## 特性

模块化功能，大量使用类，实际最短实现代码不超过十行。



## 注意
⚠ 自行反爬


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
│   ├── auto  //队列目录
│   ├── comment  //评论
│   ├── doData  //分析后总汇数据
│   ├── poster   //分析
│   ├── queue_rank.yaml   //队列索引
│   └── run.yaml  //任务器设置！
├── Runtask.py  //任务器
├── Diana.py    //分析器
├── Hunter01.py   //工具类
├── Hunter02.py   //工具类
├── logger.conf  //log moule
├── mods  //模块
│   ├── bili.py  //bili api tool
│   ├── deal.py  //no use
│   ├── __pycache__
│   ├── sampleDeal.py  //分析
│   ├── tasker.py  //任务队列
│   └── Tool.py   //通用类
├── note   //开发日志
│   └── soda.md
├── pos.txt
├── README.md
├── requirements.txt
├── running.log
├── sample  //训练数据源
│   ├── cloud.jpg.bak
│   ├── holoneg.txt
│   ├── only_vtuber
│   ├── pos2.txt
│   ├── sample.zip
│   └── vtuber_add_ylg
├── SimHei.ttf
├── snownlp  snownlp模块
│   ├── classification
│   ├── __init__.py
│   ├── normal
│   ├── __pycache__
│   ├── seg
│   ├── sentiment
│   ├── sim
│   ├── summary
│   ├── tag
│   └── utils
├── stopwords.txt 停用词


```


#### 使用

填写并编写如下，目前仍在开发，暂时不提供成品部署
```
├── data  //数据
│   └── run.yaml  //任务器设置！
├── Runtask.py  //任务器
├── Diana.py    //分析器
```



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

[![s](https://img.shields.io/badge/Sponsor-Alipay-ff69b4)](https://azz.net/ly233)


[![](https://s3.bmp.ovh/imgs/2022/02/f30ca9d9152ba7aa.png)](https://gitlab.com/45iron/holdtag)

------------------------------



