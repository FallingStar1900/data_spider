import os
import sys
import urllib.request
import re
import pymysql

class GetAllStockInfo:

    def __init__(self, is_get_stock, *argv):
        self.is_get_stock = is_get_stock
        self.ids_len = len(argv)
        #如果ids_len不为0表示抓取some或single
        if self.ids_len != 0:
            self.stock_ids = argv[0]
        self.db = pymysql.connect(host="localhost", user="", passwd="", db="stock_info", port=3306)
        self.cur = self.db.cursor()

    def get_stock_info(self):
        if self.ids_len == 0:
            print(self.ids_len)
            pass
        else:
            ids = self.stock_ids.split(",")
            for item in ids:
                sql = self.select_mysql(str(item))
                print(sql)
                try:
                    self.cur.execute(sql)
                    self.db.commit()
                    #获取查询的结果，默认list，如果要dict 设置cursorclass = pymysql.cursors.DictCursor
                    flag = self.cur.fetchall()
                    if flag:
                        print("stock code is exists")
                        #如果存在则爬取该id对应的信息，返回结果为json格式
                        result = self.spider_stock_info(str(item))
                        print(result)
                    else:
                        print("stock code:%s is not exists..." % str(item))

                    return 0
                except Exception as e:
                    self.db.rollback()
                    print(e)
                    print(item)
                    return -1
            #print(ids)
            self.db.close()
            pass

    def spider_stock_info(self, code):
        #抓取历史基本数据
        url = "http://quotes.money.163.com/trade/lsjysj_" + code + ".html?year=2019&season=1"

        print(code)
        response = urllib.request.urlopen(url)
        raw_data = response.read().decode("utf-8")
        s_data = r"<tr class='[a-zA-Z]*'><td>(\d{4}-\d{1,2}-\d{1,2})</td>"
        s_number = r"<td[\s]*[a-z=]*\'*[a-zA-Z]*\'*>(\d*,*\d*,*\d*,*-*\d*\.*\d*)</td>"
        pat_data = re.compile(s_data)
        pat_number = re.compile(s_number)
        info_data = pat_data.findall(raw_data)
        info_number = pat_number.findall(raw_data)
        while '' in info_number:
            info_number.remove('')
        print(info_data)
        print(info_number)
        print(len(info_data))
        print(len(info_number))
        return 1


    def select_mysql(self, code):
        sql = "select code from stock_id where code=" + "\"" + code + "\"" + ";"
        return sql

    #日期,股票代码,名称,收盘价,最高价,最低价,开盘价,前收盘,涨跌额,涨跌幅,换手率,成交量,成交金额,总市值,流通市值,成交笔数