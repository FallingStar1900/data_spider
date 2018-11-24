import datetime
import random
class DefReqHeader:
    def __init__(self, src, src_id, src_name, des, des_id, des_name, url_type):
        self.src_city = src
        self.src_city_id = src_id
        self.src_city_name = src_name
        self.des_city = des
        self.des_city_id = des_id
        self.des_city_name = des_name
        self.req_url_type = url_type
        self.today_data = datetime.date.today()
    def get_req_header(self):
        header = {}
        header['Accept'] = '*/*'
        header['Accept-Encoding'] = 'gzip, deflate, br'
        header['Accept-Language'] = 'zh-CN,zh;q=0.9'
        header['Connection'] = 'keep-alive'
        if self.req_url_type == "low_price":
            content_length = 50
        elif self.req_url_type == "ctrip_single_airlines":
            content_length = 274
        else:
            content_length = 50
        header['Content-Length'] = content_length
        header['Content-Type'] = 'application/json'
        header['path'] = '/itinerary/api/12808/products'
        header['Host'] = 'flights.ctrip.com'
        header['Origin'] = 'https://flights.ctrip.com'
        print(str(self.today_data))
        header['Referer'] = 'https://flights.ctrip.com/itinerary/oneway/bjs-ckg?date=' + '2018-11-26' + '&portingToken=d04549c711694b459c3beec152cda919'
        #User-Agent得随机，否则需要验证码
        UserAgent = [
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
            "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 () Chrome/69.0.3497.100 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        ]
        header['User-Agent'] = random.choice(UserAgent)
        header['X-Requested'] = 'XMLHttpRequest'
        header['cookie'] = ''
        return header
    def req_form_data(self):
        if self.req_url_type == "low_price":
            formdata = {
            'flightWay': 'Oneway',
            'dcity': self.src_city,
            'acity': self.des_city
            }
        elif self.req_url_type == "ctrip_single_airlines":
            formdata = {
                'classType': "ALL",
                'flightWay': "Oneway",
                'hasBaby': "false",
                'hasChild': "false",
                'portingToken': "d04549c711694b459c3beec152cda919",
                'searchIndex': 1,
                'airportParams': [{
                    'acity': self.des_city,
                    'acityid': self.des_city_id,
                    'acityname': self.des_city_name,
                    'date': "2018-11-26",
                    'dcity': self.src_city,
                    'dcityid': self.src_city_id,
                    'dcityname': self.src_city_name
                }
                ]
            }
        else:
            formdata = { }
        return formdata
