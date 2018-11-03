# -*- coding:utf-8 -*-

from ctrip.low_price import GetSingleLowPrice
from citys.url_manager import DefReqUrl

class ParseSingleLowPrice:
    def __init__(self, dict_data):
        self.dict_data = dict_data

    def parse_single_low_price(self):
        #for k,v in self.dict_data.items():
            #print(k,v)
            #print("aaa")
        for i in self.dict_data['data']['oneWayPrice'][0]:
            low_price_date = i
            low_price = self.dict_data['data']['oneWayPrice'][0][i]
            print(low_price_date, low_price)
            #return low_price_date, low_price
        return low_price_date, low_price


if __name__ == "__main__":
    #def_req_url = DefReqUrl()
   # lowest_price_url = def_req_url.get_ctrip_url_lowest_price()
    low_price = GetSingleLowPrice("BJS", 1, "北京", "XMN", 25, "厦门", "low_price")
    all_low_price = low_price.get_low_price()
    parsedict = ParseSingleLowPrice(all_low_price)
    parsedict.parse_single_low_price()