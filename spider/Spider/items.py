# 数据容器文件

import scrapy

class SpiderItem(scrapy.Item):
    pass

class GameinfoItem(scrapy.Item):
    # 游戏名称
    gamename = scrapy.Field()
    # 图片
    imgurl = scrapy.Field()
    # 开发
    kaifa = scrapy.Field()
    # 网络
    wangluo = scrapy.Field()
    # 类型
    leixing = scrapy.Field()
    # 标签
    tagname = scrapy.Field()
    # 热度
    redu = scrapy.Field()
    # 游民指数
    ymzs = scrapy.Field()
    # 玩家评分
    wjpf = scrapy.Field()
    # 投票数
    scoretimes = scrapy.Field()
    # 游戏介绍
    gameintro = scrapy.Field()
    # 评论内容
    plcontent = scrapy.Field()
    # 详情地址
    detailurl = scrapy.Field()

