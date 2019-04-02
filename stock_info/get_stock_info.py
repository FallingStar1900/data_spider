import os
import sys
import urllib.request
import re
import datetime
import pymysql

class GetAllStockInfo:

    def __init__(self, is_get_stock, mindays, *argv):
        self.is_get_stock = is_get_stock
        self.mindays = mindays
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
        final_date = []
        final_number = []
        days = int(self.mindays)
        now_year = datetime.datetime.now().year
        now_month = datetime.datetime.new().month
        if now_month > 0 and now_month < 4:
            season = 1
        elif now_month >3 and now_month < 7:
            season = 2
        elif now_month >6 and now_month < 10:
            season = 3
        elif now_month >9 and now_month <13:
            season = 4
        while True:
            url = "http://quotes.money.163.com/trade/lsjysj_" + code + ".html?year=" + now_year + "&season=" + season
            print(code)
            response = urllib.request.urlopen(url)
            raw_data = response.read().decode("utf-8")
            s_date = r"<tr class='[a-zA-Z]*'><td>(\d{4}-\d{1,2}-\d{1,2})</td>"
            s_number = r"<td[\s]*[a-z=]*\'*[a-zA-Z]*\'*>(\d*,*\d*,*\d*,*-*\d*\.*\d*)</td>"
            pat_date = re.compile(s_date)
            pat_number = re.compile(s_number)
            tmp_info_date = pat_date.findall(raw_data)
            tmp_info_number = pat_number.findall(raw_data)
            while '' in tmp_info_number:
                tmp_info_number.remove('')
            final_date = tmp_info_date[:days] + final_date
            nums = len(tmp_info_date[:days]) * 10
            final_number = tmp_info_number[:nums] + final_number
            if len(final_date) == days:
                break
            elif len(final_date) < days:
                left_days = days - len(final_date)
                season = season - 1
                days = left_days
                if season <= 0:
                    now_year = now_year - 1
                    season = 4
                    continue
                continue
        print(final_date)
        print(final_number)
        print(len(final_date))
        print(len(final_number))
        result = self.data_operate(final_date, final_number)
        return 1

    def select_mysql(self, code):
        sql = "select code from stock_id where code=" + "\"" + code + "\"" + ";"
        return sql

    def data_operate(self, list_date, list_number):
        stock_info = {}
        length = len(list_date)
        if length * 10 != len(list_number):
            print("获取的数据中日期和数据的数量不匹配!")
            return -1
        i = 0
        while i<len(list_number):
            stock_info["stock_date"] = list_date[i]
            start_price = list_number[i]
            max_price = list_number[i+1]
            min_price = list_number[i+2]
            end_price = list_number[i+3]
            float_price = list_number[i+4]
            float_percent = list_number[i+5]
            volume_hand = list_number[i+6]
            gmv_price = list_number[i+7]
            swing_percent = list_number[i+8]
            turnover_percent = list_number[i+9]
            i = i + 10
            #将数据写入dict中，后期可以转成json处理

        return

    def mysql_operate(self, data_dict):