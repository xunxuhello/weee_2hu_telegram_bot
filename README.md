# Weee\_2hu\_telegram\_bot

## Introduction

### 二虎是什么？
二虎是我们家的猫。他超级可爱！

### 为什么会有二虎 bot？
很久很久以前，二虎他妈发现了 [Weee](https://www.sayweee.com/) 上有 [Letao](https://www.letao.jp/) 。但是 Weee 很不经常上这个稀有的商品，所以二虎他爸只好一直在人肉刷 Weee。二虎他爸决定写一个二虎 bot，用来自动刷一刷Weee有没有上新的想要的商品。

### 二虎 bot 是怎么工作的？
二虎 bot 每隔一段时间（如一个小时）抓取 Weee 的商品列表，然后告诉二虎他爸本次抓取的列表与上一次的抓取的列表有什么新货。二虎他爸可以设定一些关键词，用来让二虎 bot 只汇报想要的商品的上新情况。

### 二虎 bot 支持多用户吗？
二虎 bot 可以同时为二虎他爸，二虎他妈以及二虎的小伙伴们刷 Weee！这样二虎他妈就可以给二虎他爸刷牛蹄筋了！二虎的小伙伴们可以设定自己的 zipcode，二虎会根据 zipcode 对指定地区刷 Weee。

二虎可真是个能干的宝宝。

# Installation

## Dependencies

* [Redis](https://redis.io/): 二虎 bot 使用 Redis 来当小本本
* [Redis-py](https://github.com/andymccurdy/redis-py): 二虎 bot 使用 Redis-py 来向 Redis 数据库刻下今天 Weee 有什么货物
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot): 二虎 bot 用 python-telegram-bot 来向 telegram 发送喵喵喵
* [Requests](https://requests.readthedocs.io/zh_CN/latest/): “Requests 是唯一的一个非转基因的 Python HTTP 库。Requests 允许你发送纯天然，植物饲养的 HTTP/1.1 请求，无需手工劳动。” 
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/): 二虎喜欢喝美丽汤。二虎用美丽汤漂亮的解析 HTML。

## Dependencies Installation

* For Redis: [https://redis.io/download#installation](https://redis.io/download#installation)
* For Python: `$ pip install redis python-telegram-bot requests beautifulsoup4`

如果你没有安装 pip （啧啧），这个 [Python installation guide](https://docs.python-guide.org/starting/installation/) 可以带你完成这一流程。

## Configuration

把 `conf_demo.json` 改名为 `conf.json` ，在里面添加你的 telegram-userid 和 bot 的 TOKEN。Bot TOKEN 可以在 telegram 里向 @BotFather 申请获得。

# Usage

TODO


