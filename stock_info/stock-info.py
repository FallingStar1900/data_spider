import os
import sys
import re
import urllib.request
import pymysql
from stock_info.get_stock_info import GetAllStockInfo


class GetStockInfo:
    def __init__(self, url, page):
        self.url = url
        self.page = page
        self.db = pymysql.connect(host="localhost", user="", passwd="", db="stock_info", port=3306)
        self.cur = self.db.cursor()

    def get_stock_info(self):
        self.get_stock_id()
        return 0

    def get_stock_id(self):
        allCodeList = []
        response = urllib.request.urlopen(self.url)
        raw_data = response.read().decode('utf-8')
        s_code = r'<td><a class=content href="./\S\S/[0-9]{6}/">([0-9\(\)\u4e00-\u9fa5A-Z\*\�].*?)</a>'
        pat = re.compile(s_code)
        info = pat.findall(raw_data)
        print(info)
        length = len(info)
        is_ok = length % 3
        if is_ok != 0:
            print("第%s页数据没有抓取完整,请检查内容中是否有特殊字符..." % self.page)
            print(is_ok)
            exit(-1)
        code_items = int(length / 3)
        print(code_items)
        i = 0
        trade_place = "unknown"
        while i < length:
            code = info[i]
            if code[0] == "6":
                trade_place = "SHA"
                allCodeList.append(code)
            elif code[0] == "3":
                trade_place = "SZA"
                allCodeList.append(code)
            elif code[0] == "0":
                trade_place = "CYB"
                allCodeList.append(code)
            else:
                i = i + 3
                print(self.page)
                continue

            company = info[i+1]
            company_des = info[i+2]
            #抓取的页面中有不识别的字符，因此手动赋值
            if code == "002752":
                company = "昇兴股份"
                company_des = "昇兴集团股份有限公司"
            print(code)
            #todo 写入mysql
            mysql_flag = self.base_info_to_mysql(code, company, company_des, trade_place)
            if mysql_flag == 0:
                print("stock数据成功写入了mysql...")
            else:
                print("stock数据写入mysql失败，失败的stock股票是%s %s" % (code, company))
            i = i + 3
        #exit(0)
        return allCodeList

    def base_info_to_mysql(self, code, name, company, trade_place):
        sql = "insert into stock_id values(null," + "\"" + code + "\"" + "," + "\"" + name + "\"" + "," + \
              "\"" + company + "\"" + "," + "\"" + trade_place + "\"" + ")" + \
              " ON DUPLICATE KEY UPDATE " + \
              "code=" + "\"" + code + "\"" + "," + "name=" + "\"" + name + "\"" + "," + \
              "company=" + "\"" + company + "\"" + "," + "exchangeType=" + "\"" + trade_place + "\"" + ";"
        try:
            self.cur.execute(sql)
            self.db.commit()
            return 0
        except Exception as e:
            self.db.rollback()
            print(e)
            return -1


if __name__ == "__main__":
    #is_rewrite_stock_id = input("是否重新抓取所有的股票代码(true/false):")
    is_rewrite_stock_id = "false"
    is_get_stock = input("请输入要爬取的股票代码的数量(all/some/single)(当要分析某些股票数据的时候用到some或single，否则选all):")
    page = 1
    pageAll = 185
    if is_rewrite_stock_id == "true":
        while page <= pageAll:
            if page == 1:
                url = "http://www.yz21.org/stock/info/"
            else:
                url = "http://www.yz21.org/stock/info/stocklist_" + str(page) + ".html"
            print(url)
            StockInfo = GetStockInfo(url, page)
            status = StockInfo.get_stock_info()
            page = page + 1
            if status == 0:
                print("获取股票code成功")
            else:
                print("获取股票code失败")
    else:
        if is_get_stock == "all":
            mindays = input("请输出要获取信息的天数:")
            get_stock = GetAllStockInfo(is_get_stock, mindays)
            get_stock.get_stock_info()
        elif is_get_stock == "some":
            stock_code = input("请输入具体要获取信息的股票代码(请用逗号分隔):")
            mindays = input("请输出要获取信息的天数:")
            #mindays=60
            #stock_code = "002031"
            print(stock_code)
            get_stock = GetAllStockInfo(is_get_stock, mindays, stock_code)
            get_stock.get_stock_info()
        elif is_get_stock == "single":
            stock_code = input("请输入具体要获取信息的股票代码:")
            mindays = input("请输出要获取信息的天数:")
            get_stock = GetAllStockInfo(is_get_stock, mindays, stock_code)
            get_stock.get_stock_info()
        exit(0)