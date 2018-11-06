# -*- coding:utf-8 -*-

from ctrip.low_price import GetSingleLowPrice
from citys.url_manager import DefReqUrl
import pymysql

class ParseSingleLowPrice:
    def __init__(self, dict_data):
        self.dict_data = dict_data
        self.db = pymysql.connect(host="localhost", user="", passwd="", db="data_spider", port=)
        self.cur = self.db.cursor()

    def parse_single_low_price(self):
        list = []
        for i in self.dict_data['data']['oneWayPrice'][0]:
            low_price_date = i
            low_price = self.dict_data['data']['oneWayPrice'][0][i]
            date_price = str(low_price_date) + ":" + str(low_price)
            list.append(date_price)
        text = ",".join(list)
        print(text)
        sql = self.load_low_price2mysql("厦门", "1", "BJS", "广州", "25", "XMN", text)
        print(sql)
        try:
            self.cur.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
        #return low_price_date, low_price

    def load_low_price2mysql(self, src_city_name, src_city_num, src_city_id, des_city_name, des_city_num, des_city_id, text):
        src_des_city = src_city_name + "_" + des_city_name
        mysql = "insert into low_price values(" + "\"" + src_des_city + "\"" + "," +"\"" + src_city_name + "\"" + "," + src_city_num + "," + "\"" + \
                src_city_id + "\"" + "," + "\"" + des_city_name + "\"" + "," + des_city_num + "," + "\"" + des_city_id + \
                "\"" + "," + "\"" + text + "\"" + ")" + " ON DUPLICATE KEY UPDATE " + "src_city_name=" + "\"" + src_city_name \
                + "\"" + "," + "src_city_number=" + src_city_num + "," + "src_city_code=" + "\"" + src_city_id + "\"" + "," + \
                "des_city_name=" + "\"" + des_city_name + "\"" + "," + "des_city_number=" + des_city_num + "," + "des_city_code=" \
                + "\"" + des_city_id + "\"" + "," + "low_price_list=" + "\"" + text + "\"" + ";"
        return mysql



if __name__ == "__main__":
    #def_req_url = DefReqUrl()
    #lowest_price_url = def_req_url.get_ctrip_url_lowest_price()
    low_price = GetSingleLowPrice("BJS", 1, "北京", "XMN", 25, "厦门", "low_price")
    all_low_price = low_price.get_low_price()
    parsedict = ParseSingleLowPrice(all_low_price)
    parsedict.parse_single_low_price()