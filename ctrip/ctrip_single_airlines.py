import urllib.request
import json
import gzip
from citys.url_manager import DefReqUrl
from ctrip.req_header_ctrip import DefReqHeader

class GetSingleLowPrice:
    def __init__(self, src, src_id, src_name, des, des_id, des_name, req_type):
        self.src_city = src
        self.src_city_id = src_id
        self.src_city_name = src_name
        self.des_city = des
        self.des_city_id = des_id
        self.des_city_name = des_name
        self.req_type = req_type
    def get_ctrip_airlines(self):
        ctripHeader = DefReqHeader(self.src_city, self.src_city_id, self.src_city_name, self.des_city, self.des_city_id, self.des_city_name, self.req_type)
        header = ctripHeader.get_req_header()
        formdata = ctripHeader.req_form_data()
        url = DefReqUrl().get_ctrip_oneway_airlines_products()
        res = urllib.request.Request(url=url, headers=header)
        #请求参数要进行编码
        req_formdata = json.dumps(formdata).encode()
        response = urllib.request.urlopen(res, req_formdata)
        print(response.info())
        # 得到的结果从info中可以看到是gzip压缩，需要解析返回结果，由于最终结果是json，所以必须用json的形式打印
        print(response)
        raw_data = response.read()
        # print("返回数据", raw_data)
        res_json = json.loads(gzip.decompress(raw_data))
        print(res_json)

if __name__ == "__main__":
    singleAirlines = GetSingleLowPrice("BJS", 1, "北京", "XMN", 25, "厦门", "ctrip_single_airlines")
    singleAirlines.get_ctrip_airlines()
