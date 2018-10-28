import datetime
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
            content_length = 273
        else:
            content_length = 50
        header['Content-Length'] = content_length
        header['Content-Type'] = 'application/json'
        header['Host'] = 'flights.ctrip.com'
        header['Origin'] = 'https://flights.ctrip.com'
        #https://flights.ctrip.com/itinerary/oneway/bjs-ckg?date=2018-10-30&portingToken=829ab5159dd8479aa879f545c990da94
        header[
            'Referer'] = 'https://flights.ctrip.com/itinerary/oneway/bjs-ckg?date=' + str(self.today_data) + '&portingToken=829ab5159dd8479aa879f545c990da94'
        header[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 () Chrome/69.0.3497.100 Safari/537.36'
        header['X-Requested'] = 'XMLHttpRequest'
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
                'portingToken': "cf4821e212f34c13901327c6b95ce865",
                'searchIndex': 1,
                'airportParams': [{
                    'acity': self.src_city,
                    'acityid': self.src_city_id,
                    'acityname': self.src_city_name,
                    'date': str(self.today_data),
                    'dcity': self.des_city,
                    'dcityid': self.des_city_id,
                    'dcityname': self.des_city_name
                }
                ]
            }
        else:
            formdata = { }
        return formdata
