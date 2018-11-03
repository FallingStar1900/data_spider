# -*- coding:utf-8 -*-

from citys.all_city import GetAllCitys
from citys.url_manager import DefReqUrl

class ParseDict:
    def __init__(self, dict_data):
        self.dict_data = dict_data

    def parse_dict2str(self):
        for k,v in self.dict_data.items():
            print(k,v)
        list_item = []
        for item in self.dict_data['data']:
            print(item)
            list_item.append(item)
        print(list_item)
        item_len = len(self.dict_data['data'])
        num=1
        while num < item_len:
            for i in self.dict_data['data'][list_item[num]]:
                for j in self.dict_data['data'][list_item[num]][i]:
                    city_name = j['display']
                    data = j['data']
                    info_item = data.split('|')
                    city_number = info_item[2]
                    city_code = str(info_item[3])
                    print(city_name, city_number, city_code)
                    #print(city_number)
                    #print(city_code)
            num = num + 1

if __name__ == "__main__":
    def_req_url = DefReqUrl()
    citys_url = def_req_url.get_ctrip_url_citys()
    all_city = GetAllCitys(citys_url)
    dict_city_data = all_city.get_all_city_json()
    parsedict = ParseDict(dict_city_data)
    parsedict.parse_dict2str()