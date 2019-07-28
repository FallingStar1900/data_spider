import os
import sys
import json
import pymysql

class GetResultInfo:

    def __init__(self, fin, datas, max_price, plate_info, divs, weight_thread):
        self.f_result = fin
        self.datas = datas
        self.max_price = max_price
        self.weight_thread = weight_thread
        self.plate_info = plate_info
        self.divs = divs
        self.db = pymysql.connect(host="localhost", user="", passwd="", db="stock_info", port=3306)
        self.cur = self.db.cursor()

    def get_result(self):
        f_final = open(self.f_result, 'r')
        ff = f_final.readlines()
        databases = "sh_stock_info"
        for k in ff:
            aa = k.strip('\n').split(',')
            i = aa[0]
            weight = aa[1]
            divnums = int(i) % int(self.divs)
            plate_path = ""
            if i[0] == "6":
                databases = "sh_stock_info"
                plate_path = "/Users/liliangliang6/Desktop/study-code/dev/stock_info/sh/" + str(divnums) + "/" + str(i) + "_" + str(divnums) + "_stockPlateInfo"
            elif i[0] == "0":
                databases = "sz_stock_info"
                plate_path = "/Users/liliangliang6/Desktop/study-code/dev/stock_info/sz/" + str(divnums) + "/" + str(i) + "_" + str(divnums) + "_stockPlateInfo"
            elif i[0] == "3":
                databases = "cyb_stock_info"
                plate_path = "/Users/liliangliang6/Desktop/study-code/dev/stock_info/cyb/" + str(divnums) + "/" + str(i) + "_" + str(divnums) + "_stockPlateInfo"
                continue
            sqls1 = "select end_price from " + databases + " where code=" + str(i) + " and date_format(valid_date, '%Y-%m-%d')=" + "\'" + str(self.datas) + "\'" + ";"
            self.cur.execute(sqls1)
            self.db.commit()
            select_price = self.cur.fetchall()
            if len(select_price) != 0:
                s_price = select_price[0]
                if float(s_price[0]) < float(self.max_price):
                    res = self.is_in_plate(plate_path)
                    if res == 1:
                        if float(weight) >= weight_thread:
                            print("最后一天价格为:%s, 小于%s元，且第二天可能上涨的股票代码: %s, 股票上涨权重: %s" % (s_price, self.max_price, i, weight))
                    #elif res == -1:
                        #print("最后一天价格为:%s, 小于%s元，且第二天可能上涨的股票代码: %s, 股票上涨权重: %s， 但该股没有在关注的板块内!" % (s_price, self.max_price, i, weight))
                    elif isinstance(res, list):
                        plate = ",".join(res)
                        if float(weight) >= float(self.weight_thread):
                            print("最后一天价格为:%s, 小于%s元，且第二天可能上涨的股票代码: %s, 股票上涨权重: %s, 股票所属的板块为: %s" % (s_price, self.max_price, i, weight, plate))

    def is_in_plate(self, fpath):
        f = open(fpath, 'r')
        f_json = json.load(f)
        temp_info = f_json[str(self.datas)]
        valid_plate = []
        flag = ""
        for plate_no in temp_info.keys():
            name = temp_info[plate_no]["plate_name"]
            plate_list = self.plate_info.split(",")
            if len(plate_list) == 0:
                flag = 1
                break
            for i in plate_list:
                if name.find(str(i)) != -1:
                    valid_plate.append(name)
                    flag = 0

        if flag == 1:
            return 1
        elif flag == 0:
            return valid_plate
        else:
            return -1


if __name__ == "__main__":
    foutpath = "/Users/liliangliang6/Desktop/study-code/dev/stock_info"
    f_result = foutpath + '/stock_increase'
    datas = "2019-06-11"
    max_price = 15.0
    plate_info = input("请输入要分析的板块(多个时逗号分隔):")
    plate_info = ""
    weight_thread = 0.86
    divs = 5
    objs = GetResultInfo(f_result, datas, max_price, plate_info, divs, weight_thread)
    objs.get_result()