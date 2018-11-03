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
            content_length = 274
        else:
            content_length = 50
        header['Content-Length'] = content_length
        header['Content-Type'] = 'application/json'
        header['path'] = '/itinerary/api/12808/products'
        header['Host'] = 'flights.ctrip.com'
        header['Origin'] = 'https://flights.ctrip.com'
        #https://flights.ctrip.com/itinerary/oneway/bjs-ckg?date=2018-10-30&portingToken=829ab5159dd8479aa879f545c990da94
        print(str(self.today_data))
        header[
            'Referer'] = 'https://flights.ctrip.com/itinerary/oneway/bjs-ckg?date=' + str(self.today_data) + '&portingToken=2a7ffe86f3a84c0189b3f6ab0d3ebe03'
        header[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 () Chrome/69.0.3497.100 Safari/537.36'

        #Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 () Chrome/69.0.3497.100 Safari/537.36
        header['X-Requested'] = 'XMLHttpRequest'
        header['cookie'] = '_abtest_userid=382812a1-3548-436e-bd3c-642b31b36348; _RSG=_GKlSVgZ9H2Hv_GV5fLYoA; _RDG=284b093b7228782e1a3cdeb62646a43076; _RGUID=24498ea7-dcbd-443f-aca2-56915f43fe51; _ga=GA1.2.1981757315.1537684211; traceExt=campaign=CHNbaidu81&adid=index; MKT_Pagesource=PC; Session=SmartLinkCode=U1911&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; DomesticUserHostCity=CAN|%b9%e3%d6%dd; _gid=GA1.2.285589722.1541171520; FD_SearchHistorty={"type":"S","data":"S%24%u5317%u4EAC%28BJS%29%24BJS%242018-11-22%24%u53A6%u95E8%28XMN%29%24XMN"}; _RF1=221.223.89.210; Union=OUID=000401app-&AllianceID=1630&SID=1911&SourceID=&Expires=1541860771299; __zpspc=9.5.1541255971.1541255971.1%231%7C%7C%7C%7C%7C%23; appFloatCnt=2; _bfa=1.1537684207843.zey2x.1.1541171517007.1541255968440.5.15; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1541005707845%7D%2C%7B%22aid%22%3A%221630%22%2C%22timestamp%22%3A1541256016963%7D%5D; _jzqco=%7C%7C%7C%7C1541171520119%7C1.658098453.1537684210757.1541256009702.1541256016974.1541256009702.1541256016974.undefined.0.0.14.14; _bfi=p1%3D10320673302%26p2%3D10320673302%26v1%3D15%26v2%3D14'
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
                'portingToken': "2a7ffe86f3a84c0189b3f6ab0d3ebe03",
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
