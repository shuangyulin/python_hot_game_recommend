# # -*- coding: utf-8 -*-

# 数据爬取文件

import scrapy
import pymysql
import pymssql
from ..items import GameinfoItem
import time
from datetime import datetime,timedelta
import datetime as formattime
import re
import random
import platform
import json
import os
import urllib
from urllib.parse import urlparse
import requests
import emoji
import numpy as np
from DrissionPage import Chromium
import pandas as pd
from sqlalchemy import create_engine
from selenium.webdriver import ChromeOptions, ActionChains
from scrapy.http import TextResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
from sqlalchemy import create_engine
from selenium.webdriver import ChromeOptions, ActionChains
from scrapy.http import TextResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
# 游戏信息
class GameinfoSpider(scrapy.Spider):
    name = 'gameinfoSpider'
    custom_settings = {
        'HTTPERROR_ALLOWED_CODES': [400,403],
        'RETRY_HTTP_CODES': [500, 503]
    }
    spiderUrl = 'https://shouyou.gamersky.com/ku/0-0-0-00_{}.html'
    start_urls = spiderUrl.split(";")
    protocol = ''
    hostname = ''
    realtime = False


    def __init__(self,realtime=False,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.realtime = realtime=='true'

    def start_requests(self):

        plat = platform.system().lower()
        if not self.realtime and (plat == 'linux' or plat == 'windows'):
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, 'l1o106t4_gameinfo') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return
        pageNum = 1 + 1

        for url in self.start_urls:
            if '{}' in url:
                for page in range(1, pageNum):

                    next_link = url.format(page)
                    yield scrapy.Request(
                        url=next_link,
                        callback=self.parse
                    )
            else:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse
                )

    # 列表解析
    def parse(self, response):
        _url = urlparse(self.spiderUrl)
        self.protocol = _url.scheme
        self.hostname = _url.netloc
        plat = platform.system().lower()
        if not self.realtime and (plat == 'linux' or plat == 'windows'):
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, 'l1o106t4_gameinfo') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return
        list = response.css('ul.pictxt li')
        for item in list:
            fields = GameinfoItem()

            if '(.*?)' in '''a::attr(title)''':
                try:
                    fields["gamename"] = str( re.findall(r'''a::attr(title)''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["gamename"] = str( self.remove_html(item.css('''a::attr(title)''').extract_first()))

                except:
                    pass
            if '(.*?)' in '''img::attr(src)''':
                try:
                    fields["imgurl"] = str( re.findall(r'''img::attr(src)''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["imgurl"] = str( self.remove_html(item.css('''img::attr(src)''').extract_first()))

                except:
                    pass
            if '(.*?)' in '''a::attr(href)''':
                try:
                    fields["detailurl"] = str( re.findall(r'''a::attr(href)''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["detailurl"] = str( self.remove_html(item.css('''a::attr(href)''').extract_first()))

                except:
                    pass
            detailUrlRule = item.css('a::attr(href)').extract_first()
            if self.protocol in detailUrlRule or detailUrlRule.startswith('http'):
                pass
            elif detailUrlRule.startswith('//'):
                detailUrlRule = self.protocol + ':' + detailUrlRule
            elif detailUrlRule.startswith('/'):
                detailUrlRule = self.protocol + '://' + self.hostname + detailUrlRule
            else:
                detailUrlRule = self.protocol + '://' + self.hostname + '/' + detailUrlRule
            yield scrapy.Request(url=detailUrlRule, meta={'fields': fields},  callback=self.detail_parse, dont_filter=True)

    # 详情解析
    def detail_parse(self, response):
        fields = response.meta['fields']
        try:
            if '(.*?)' in '''div.box_game div.box_txt::text''':
                fields["kaifa"] = str( re.findall(r'''div.box_game div.box_txt::text''', response.text, re.S)[0].strip().split(' | ')[0].replace('开发：', ''))

            else:
                if 'kaifa' != 'xiangqing' and 'kaifa' != 'detail' and 'kaifa' != 'pinglun' and 'kaifa' != 'zuofa':
                    fields["kaifa"] = str( self.remove_html(response.css('''div.box_game div.box_txt::text''').extract_first()).split(' | ')[0].replace('开发：', ''))

                else:
                    try:
                        fields["kaifa"] = str( emoji.demojize(response.css('''div.box_game div.box_txt::text''').extract_first()).split(' | ')[0].replace('开发：', ''))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div.box_game div.box_txt::text''':
                fields["wangluo"] = str( re.findall(r'''div.box_game div.box_txt::text''', response.text, re.S)[0].strip().split(' | ')[1].replace('网络：', ''))

            else:
                if 'wangluo' != 'xiangqing' and 'wangluo' != 'detail' and 'wangluo' != 'pinglun' and 'wangluo' != 'zuofa':
                    fields["wangluo"] = str( self.remove_html(response.css('''div.box_game div.box_txt::text''').extract_first()).split(' | ')[1].replace('网络：', ''))

                else:
                    try:
                        fields["wangluo"] = str( emoji.demojize(response.css('''div.box_game div.box_txt::text''').extract_first()).split(' | ')[1].replace('网络：', ''))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div.box_game div.box_txt::text''':
                fields["leixing"] = str( re.findall(r'''div.box_game div.box_txt::text''', response.text, re.S)[0].strip().split(' | ')[2].replace('类型：', ''))

            else:
                if 'leixing' != 'xiangqing' and 'leixing' != 'detail' and 'leixing' != 'pinglun' and 'leixing' != 'zuofa':
                    fields["leixing"] = str( self.remove_html(response.css('''div.box_game div.box_txt::text''').extract_first()).split(' | ')[2].replace('类型：', ''))

                else:
                    try:
                        fields["leixing"] = str( emoji.demojize(response.css('''div.box_game div.box_txt::text''').extract_first()).split(' | ')[2].replace('类型：', ''))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div.box_game div.box_tag a::text''':
                fields["tagname"] = str( re.findall(r'''div.box_game div.box_tag a::text''', response.text, re.S)[0].strip())

            else:
                if 'tagname' != 'xiangqing' and 'tagname' != 'detail' and 'tagname' != 'pinglun' and 'tagname' != 'zuofa':
                    fields["tagname"] = str( self.remove_html(response.css('''div.box_game div.box_tag a::text''').extract_first()))

                else:
                    try:
                        fields["tagname"] = str( emoji.demojize(response.css('''div.box_game div.box_tag a::text''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''c.gshit::text''':
                fields["redu"] = int( re.findall(r'''c.gshit::text''', response.text, re.S)[0].strip())
            else:
                if 'redu' != 'xiangqing' and 'redu' != 'detail' and 'redu' != 'pinglun' and 'redu' != 'zuofa':
                    fields["redu"] = int( self.remove_html(response.css('''c.gshit::text''').extract_first()))
                else:
                    try:
                        fields["redu"] = int( emoji.demojize(response.css('''c.gshit::text''').extract_first()))
                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div#Sorce::text''':
                fields["ymzs"] = int( re.findall(r'''div#Sorce::text''', response.text, re.S)[0].strip())
            else:
                if 'ymzs' != 'xiangqing' and 'ymzs' != 'detail' and 'ymzs' != 'pinglun' and 'ymzs' != 'zuofa':
                    fields["ymzs"] = int( self.remove_html(response.css('''div#Sorce::text''').extract_first()))
                else:
                    try:
                        fields["ymzs"] = int( emoji.demojize(response.css('''div#Sorce::text''').extract_first()))
                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div#scoreAvg::text''':
                fields["wjpf"] = float( re.findall(r'''div#scoreAvg::text''', response.text, re.S)[0].strip())
            else:
                if 'wjpf' != 'xiangqing' and 'wjpf' != 'detail' and 'wjpf' != 'pinglun' and 'wjpf' != 'zuofa':
                    fields["wjpf"] = float( self.remove_html(response.css('''div#scoreAvg::text''').extract_first()))
                else:
                    try:
                        fields["wjpf"] = float( emoji.demojize(response.css('''div#scoreAvg::text''').extract_first()))
                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''span#scoreTimes::text''':
                fields["scoretimes"] = int( re.findall(r'''span#scoreTimes::text''', response.text, re.S)[0].strip())
            else:
                if 'scoretimes' != 'xiangqing' and 'scoretimes' != 'detail' and 'scoretimes' != 'pinglun' and 'scoretimes' != 'zuofa':
                    fields["scoretimes"] = int( self.remove_html(response.css('''span#scoreTimes::text''').extract_first()))
                else:
                    try:
                        fields["scoretimes"] = int( emoji.demojize(response.css('''span#scoreTimes::text''').extract_first()))
                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div#Intro''':
                fields["gameintro"] = str( re.findall(r'''div#Intro''', response.text, re.S)[0].strip())

            else:
                if 'gameintro' != 'xiangqing' and 'gameintro' != 'detail' and 'gameintro' != 'pinglun' and 'gameintro' != 'zuofa':
                    fields["gameintro"] = str( self.remove_html(response.css('''div#Intro''').extract_first()))

                else:
                    try:
                        fields["gameintro"] = str( emoji.demojize(response.css('''div#Intro''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''span[class="content first_level"]::text''':
                fields["plcontent"] = str( re.findall(r'''span[class="content first_level"]::text''', response.text, re.S)[0].strip())

            else:
                if 'plcontent' != 'xiangqing' and 'plcontent' != 'detail' and 'plcontent' != 'pinglun' and 'plcontent' != 'zuofa':
                    fields["plcontent"] = str( self.remove_html(response.css('''span[class="content first_level"]::text''').extract_first()))

                else:
                    try:
                        fields["plcontent"] = str( emoji.demojize(response.css('''span[class="content first_level"]::text''').extract_first()))

                    except:
                        pass
        except:
            pass
        return fields

    # 数据清洗
    def pandas_filter(self):
        engine = create_engine('mysql+pymysql://root:123456@localhost/spiderl1o106t4?charset=UTF8MB4')
        df = pd.read_sql('select * from gameinfo limit 50', con = engine)

        # 重复数据过滤
        df.duplicated()
        df.drop_duplicates()

        #空数据过滤
        df.isnull()
        df.dropna()

        # 填充空数据
        df.fillna(value = '暂无')

        # 异常值过滤

        # 滤出 大于800 和 小于 100 的
        a = np.random.randint(0, 1000, size = 200)
        cond = (a<=800) & (a>=100)
        a[cond]

        # 过滤正态分布的异常值
        b = np.random.randn(100000)
        # 3σ过滤异常值，σ即是标准差
        cond = np.abs(b) > 3 * 1
        b[cond]

        # 正态分布数据
        df2 = pd.DataFrame(data = np.random.randn(10000,3))
        # 3σ过滤异常值，σ即是标准差
        cond = (df2 > 3*df2.std()).any(axis = 1)
        # 不满⾜条件的⾏索引
        index = df2[cond].index
        # 根据⾏索引，进⾏数据删除
        df2.drop(labels=index,axis = 0)

    # 去除多余html标签
    def remove_html(self, html):
        if html == None:
            return ''
        pattern = re.compile(r'<[^>]+>', re.S)
        return pattern.sub('', html).strip()

    # 数据库连接
    def db_connect(self):
        type = self.settings.get('TYPE', 'mysql')
        host = self.settings.get('HOST', 'localhost')
        port = int(self.settings.get('PORT', 3306))
        user = self.settings.get('USER', 'root')
        password = self.settings.get('PASSWORD', '123456')

        try:
            database = self.databaseName
        except:
            database = self.settings.get('DATABASE', '')

        if type == 'mysql':
            connect = pymysql.connect(host=host, port=port, db=database, user=user, passwd=password, charset='utf8mb4')
        else:
            connect = pymssql.connect(host=host, user=user, password=password, database=database)
        return connect

    # 断表是否存在
    def table_exists(self, cursor, table_name):
        cursor.execute("show tables;")
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]

        if table_name in table_list:
            return 1
        else:
            return 0

    # 数据缓存源
    def temp_data(self):

        connect = self.db_connect()
        cursor = connect.cursor()
        sql = '''
            insert into `gameinfo`(
                id
                ,gamename
                ,imgurl
                ,kaifa
                ,wangluo
                ,leixing
                ,tagname
                ,redu
                ,ymzs
                ,wjpf
                ,scoretimes
                ,gameintro
                ,plcontent
                ,detailurl
            )
            select
                id
                ,gamename
                ,imgurl
                ,kaifa
                ,wangluo
                ,leixing
                ,tagname
                ,redu
                ,ymzs
                ,wjpf
                ,scoretimes
                ,gameintro
                ,plcontent
                ,detailurl
            from `l1o106t4_gameinfo`
            where(not exists (select
                id
                ,gamename
                ,imgurl
                ,kaifa
                ,wangluo
                ,leixing
                ,tagname
                ,redu
                ,ymzs
                ,wjpf
                ,scoretimes
                ,gameintro
                ,plcontent
                ,detailurl
            from `gameinfo` where
                `gameinfo`.id=`l1o106t4_gameinfo`.id
            ))
            order by rand()
            limit 50;
        '''

        cursor.execute(sql)
        connect.commit()
        connect.close()
