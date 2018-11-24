# -*- coding:utf-8 -*-

from ctrip.ctrip_single_airlines import GetSingleLowPrice
import pymysql

class ParseMultiAirlines:
    def __init__(self, dict_data):
        self.dict_data = dict_data
        self.db = pymysql.connect(host="localhost", user="", passwd="", db="data_spider", port=3306)
        self.cur = self.db.cursor()

    def parse_multi_airlines(self):
        num = len(self.dict_data['data']['routeList'])
        print(num)
        i = 0
        while i < num:
            print(i)
            route_list = self.dict_data['data']['routeList'][i]
            if route_list['routeType'] == "Flight":
                src_name = route_list['legs'][0]['flight']['departureAirportInfo']['cityName']
                src_name_code = route_list['legs'][0]['flight']['departureAirportInfo']['cityTlc']
                src_airport_name = route_list['legs'][0]['flight']['departureAirportInfo']['airportName']
                src_airport_code = route_list['legs'][0]['flight']['departureAirportInfo']['airportTlc']
                src_airport_number = route_list['legs'][0]['flight']['departureAirportInfo']['terminal']['name']
                des_name = route_list['legs'][0]['flight']['arrivalAirportInfo']['cityName']
                des_name_code = route_list['legs'][0]['flight']['arrivalAirportInfo']['cityTlc']
                des_airport_name = route_list['legs'][0]['flight']['arrivalAirportInfo']['airportName']
                des_airport_code = route_list['legs'][0]['flight']['arrivalAirportInfo']['airportTlc']
                des_airport_number = route_list['legs'][0]['flight']['arrivalAirportInfo']['terminal']['name']
                departure_data = route_list['legs'][0]['flight']['departureDate']
                arrival_data = route_list['legs'][0]['flight']['arrivalDate']

                punctualityRate = route_list['legs'][0]['flight']['punctualityRate']
                #当json中的value为空时，这里用""来判断
                if punctualityRate == "":
                    punctualityRate = "aa"
                airlineName = route_list['legs'][0]['flight']['airlineName']
                flightNumber = route_list['legs'][0]['flight']['flightNumber']

                craftTypeName = route_list['legs'][0]['flight']['craftTypeName']
                #json中的value为null时，这里的值为None
                if craftTypeName is None:
                    craftTypeName = "Null"
                craftTypeKindDisplayName = route_list['legs'][0]['flight']['craftTypeKindDisplayName']
                if craftTypeKindDisplayName is None:
                    craftTypeKindDisplayName = "Null"
                lowest_price = route_list['legs'][0]['characteristic']['lowestPrice']
                if route_list['legs'][0]['characteristic']['standardPrices'] is None:
                    cabin_info = "null"
                else:
                    standprice_num = len(route_list['legs'][0]['characteristic']['standardPrices'])

                    t = 0
                    list = []
                    while t < standprice_num:
                        cabin_class = route_list['legs'][0]['characteristic']['standardPrices'][t]['cabinClass']
                        cabin_class_price = route_list['legs'][0]['characteristic']['standardPrices'][t]['price']
                        cabin_price = cabin_class + "_" + str(cabin_class_price)
                        list.append(cabin_price)
                        t = t + 1
                    cabin_info = ",".join(list)
                stop_times = route_list['legs'][0]['flight']['stopTimes']
                if stop_times != 0 :
                    stop_time = route_list['legs'][0]['flight']['stopInfo'][0]['dateRange']['endDate']
                    stop_city = route_list['legs'][0]['flight']['stopInfo'][0]['cityName']
                    stop_city_code = route_list['legs'][0]['flight']['stopInfo'][0]['cityCode']
                else:
                    stop_time = "Null"
                    stop_city = "Null"
                    stop_city_code = "Null"
                stop_info = stop_time + ":" + stop_city + ":" + str(stop_city_code)
                #print(src_name, des_name, airlineName, flightNumber, craftTypeName, craftTypeKindDisplayName, departure_data, arrival_data, stop_time,
                      #punctualityRate, cabin_info, stop_info)
            else:
                print("空铁特惠组合")
            i = i + 1
            src_des_airlineinfo = src_name + "_" + des_name + "_" + flightNumber
            sql = self.load_oneway_flight_info(src_des_airlineinfo, src_name, src_name_code, src_airport_name, src_airport_code, src_airport_number, \
                                               des_name, des_name_code, des_airport_name, des_airport_code, des_airport_number, \
                                               departure_data, arrival_data, punctualityRate, airlineName, flightNumber, \
                                               craftTypeName, craftTypeKindDisplayName, lowest_price, cabin_info, stop_info)
            try:
                self.cur.execute(sql)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
            #print(sql)


    def load_oneway_flight_info(self, src_des_airlineinfo, sn, sc, san, sac, sanum, dn, dc, dan, dac, danum, fdate, adate, rate, airlinename, \
                                flightnuber, craftname, craftkind, low_price, cabin_info, stop_info):

        mysql1 = "insert into flight_info values(" + "\"" + src_des_airlineinfo + "\"" + ","
        mysql2 = "\"" + sn + "\"" + "," + "\"" + sc + "\"" + "," + "\"" + san + "\"" + "," + "\"" + sac + "\"" + "," + "\"" + sanum + "\"" + ","
        mysql3 = "\"" + dn + "\"" + "," + "\"" + dc + "\"" + "," + "\"" + dan + "\"" + "," + "\"" + dac + "\"" + "," + "\"" + danum + "\"" + ","
        mysql4 = "\"" + fdate + "\"" + "," + "\"" + adate + "\"" + "," + "\"" + rate + "\"" + ","
        mysql5 = "\"" + airlinename + "\"" + "," + "\"" + flightnuber + "\"" + "," + "\"" + craftname + "\"" + "," + "\"" + craftkind + "\"" + ","
        mysql6 = str(low_price) + "," +"\"" + cabin_info + "\"" + "," + "\"" + stop_info + "\"" + ")"
        mysql7 = " ON DUPLICATE KEY UPDATE " + "src_des_airlineinfo=" + "\"" + src_des_airlineinfo + "\"" + "," +"src_name=" + "\"" + sn + "\"" + "," + "src_name_code=" + "\"" +sc + "\"" +"," + \
                 "src_airport_name=" + "\"" + san + "\"" + "," + "src_airport_code=" + "\"" + sac + "\"" + "," + "src_airport_number=" + "\"" + sanum + "\"" + ","
        mysql8 = "des_name=" + "\"" + dn + "\"" + "," + "des_name_code=" + "\"" +dc + "\"" + "," + \
                 "des_airport_name=" + "\"" + dan + "\"" + "," + "des_airport_code=" + "\"" + dac + "\"" + "," + "des_airport_number=" + "\"" + danum + "\"" + ","
        mysql9 = "departure_data=" + "\"" + fdate + "\"" + "," + "arrival_data=" + "\"" + adate + "\"" + "," + "punctualityRate=" + "\"" + rate + "\"" + ","
        mysql10 = "airlineName=" + "\"" + airlinename + "\"" + "," + "flightNumber=" + "\"" + flightnuber + "\"" + ","\
                  + "craftTypeName=" + "\"" + craftname+ "\"" + "," + "craftTypeKindDisplayName=" + "\"" + craftkind + "\"" + ","
        mysql11 = "lowest_price=" + "\"" + str(low_price) + "\"" + "," + "cabin_info=" + "\"" +cabin_info + "\"" + "," + "stop_info=" + "\"" +stop_info + "\"" + ";"
        mysql = mysql1 + mysql2 + mysql3 + mysql4 + mysql5 + mysql6 + mysql7 + mysql8 + mysql9 + mysql10 + mysql11
        return mysql

if __name__ == "__main__":
    singleAirlines = GetSingleLowPrice("BJS", 1, "北京", "XMN", 25, "厦门", "ctrip_single_airlines")
    airlines_ctrip = singleAirlines.get_ctrip_airlines()
    multi_airlines = ParseMultiAirlines(airlines_ctrip)
    multi_airlines.parse_multi_airlines()