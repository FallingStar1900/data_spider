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
            print("ids: %s" % self.stock_ids)
        self.db = pymysql.connect(host="localhost", user="xiangyu1987826", passwd="xiangyu1987826", db="stock_info", port=3306)
        self.cur = self.db.cursor()

    def get_stock_info(self):
        if self.ids_len == 0:
            print(self.ids_len)
            pass
        else:
            ids = self.stock_ids.split(",")
            for item in ids:
                sql = self.select_mysql(str(item))
                #print(sql)
                try:
                    self.cur.execute(sql)
                    self.db.commit()
                    #获取查询的结果，默认list，如果要dict 设置cursorclass = pymysql.cursors.DictCursor
                    flag = self.cur.fetchall()
                    if flag:
                        print("stock code:%s is exists" % str(item))
                        #如果存在则爬取该id对应的信息，返回结果为json格式
                        result = self.spider_stock_info(str(item))
                        if result == 0:
                            print("获取股票%s数据成功..." % str(item))
                            continue
                        else:
                            print("获取股票%s数据失败..." % str(item))
                            continue
                    else:
                        print("stock code:%s is not exists..." % str(item))
                except Exception as e:
                    self.db.rollback()
                    print(e)
                    print(item)
                    continue
            #print(ids)
            self.db.close()
            return 0

    def spider_stock_info(self, code):
        #抓取历史基本数据
        final_date = []
        final_number = []
        days = int(self.mindays)
        now_year = datetime.datetime.now().year
        now_month = datetime.datetime.now().month
        if now_month > 0 and now_month < 4:
            season = 1
        elif now_month >3 and now_month < 7:
            season = 2
        elif now_month >6 and now_month < 10:
            season = 3
        elif now_month >9 and now_month <13:
            season = 4
        #print(season)
        while True:
            url = "http://quotes.money.163.com/trade/lsjysj_" + code + ".html?year=" + str(now_year) + "&season=" + str(season)
            #print(code)
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
            #print("mindays %s" % days)
            #print("final_date %s" % len(final_date))
            if len(tmp_info_date[:days]) == days:
                break
            elif len(tmp_info_date[:days]) < days:
                left_days = int(self.mindays) - len(final_date)
                season = season - 1
                days = left_days
                #print("season is %s:" % season)
                if season <= 0:
                    now_year = now_year - 1
                    season = 4
                    continue
                continue
        #print(final_date)
        #print(final_number)
        #print(len(final_date))
        #print(len(final_number))
        result = self.data_operate(code, final_date, final_number)
        return result

    def select_mysql(self, code):
        sql = "select code from stock_id where code=" + "\"" + code + "\"" + ";"
        return sql

    def data_operate(self, code, list_date, list_number):
        stock_info = {}
        temp_dict = {}
        length = len(list_date)
        if length * 10 != len(list_number):
            print("获取的数据中日期和数据的数量不匹配!")
            return -1
        i = 0
        j = 0
        #{"stock_date":{"2019-03-31":{"start_price":3.71,"max_price":3.8,"min_price":3.6},"2019-04-01":{"start_price":3.71,"max_price":3.8,"min_price":3.6}}}
        while j < length:
            tmp = {}
            # 将数据写入dict中，后期可以转成json处理
            d = tmp.setdefault(list_date[j], {})
            d.setdefault("start_price", list_number[i])
            d.setdefault("max_price", list_number[i+1])
            d.setdefault("min_price", list_number[i+2])
            d.setdefault("end_price", list_number[i+3])
            d.setdefault("change_price", list_number[i+4])
            d.setdefault("change_percent", list_number[i+5])
            d.setdefault("volume_hand", list_number[i+6])
            d.setdefault("gmv_price", list_number[i+7])
            d.setdefault("swing_percent", list_number[i+8])
            d.setdefault("turnover_percent", list_number[i+9])
            temp_dict = dict(temp_dict, **tmp)
            j = j + 1
            i = i + 10
        stock_info["stock_date"] = temp_dict
        #print(stock_info)
        result = self.mysql_operate(code, stock_info)
        return result

    def mysql_operate(self, code, data_dict):
        code = code
        dateList = data_dict["stock_date"].keys()
        #print(dateList)
        for i in dateList:
            tempDict =  data_dict["stock_date"][i]
            vd = i
            sp = tempDict["start_price"]
            maxp = tempDict["max_price"]
            minp = tempDict["min_price"]
            ep = tempDict["end_price"]
            cpri = tempDict["change_price"]
            cper = tempDict["change_percent"]
            vh = tempDict["volume_hand"]
            gp = tempDict["gmv_price"]
            sper = tempDict["swing_percent"]
            tp = tempDict["turnover_percent"]
            dbs1 = "sh_stock_info"
            if code[0] == "6":
                dbs1 = "sh_stock_info"
            elif code[0] == "3":
                dbs1 = "cyb_stock_info"
            elif code[0] == "0":
                dbs1 = "sz_stock_info"
            sql = self.sql_generate(dbs1, vd, code, sp, maxp, minp, ep, cpri, cper, vh, gp, sper, tp)
            #print(sql)
            try:
                self.cur.execute(sql)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
                return -1
        return 0

    def sql_generate(self, dbs, vd, code, sp, maxp, minp, ep, cpri, cper, vh, gp, sper, tp):
        vh = str(vh).replace(',', '')
        gp = str(gp).replace(',', '')
        all_record = (dbs, vd, code, sp, maxp, minp, ep, cpri, cper, vh, gp, sper, tp)
        some1 = (sp, maxp, minp, ep)
        some2 = (cpri, cper, vh, gp)
        some3 = (sper, tp)

        sql = "insert into %s values (\"%s\", \"%s\", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % all_record + \
              "ON DUPLICATE KEY UPDATE start_price=%s,max_price=%s,min_price=%s,end_price=%s" % some1 + \
              ",change_price=%s,change_percent=%s,volume_hand=%s,gmv_price=%s" % some2 + \
              ",swing_percent=%s,turnover_percent=%s" % some3 + ";"
        return sql