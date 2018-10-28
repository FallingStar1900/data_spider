import urllib.request
import json
from url_manager import DefReqUrl

class GetAllCitys:
    def __init__(self, url):
        #获取外部传进来的获取所有城市的url
        self.url = url
    def get_all_city_json(self):
        res = urllib.request.Request(self.url)
        response = urllib.request.urlopen(res)
        print(response.info)
        # 得到的结果从info中可以看到没有压缩，需要解析返回结果，由于最终结果是json，所以必须用json的形式打印
        raw_data = response.read()
        # print("返回数据", raw_data)
        raw_json = json.loads(raw_data)
        print(raw_json)
#to do
#class ParseAllCitys:
    #def __init__(self, res_json):
        #解析传进来的json，获取全国各个城市名称

if __name__ == "__main__":
    def_req_url = DefReqUrl()
    citys_url = def_req_url.get_ctrip_url_citys()
    all_city = GetAllCitys(citys_url)
    all_city.get_all_city_json()