# -*- coding:utf-8 -*-

from ctrip.ctrip_single_airlines import GetSingleLowPrice


class ParseMultiAirlines:
    def __init__(self, dict_data):
        self.dict_data = dict_data

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
                airlineName = route_list['legs'][0]['flight']['airlineName']
                flightNumber = route_list['legs'][0]['flight']['flightNumber']
                craftTypeName = route_list['legs'][0]['flight']['craftTypeName']
                craftTypeKindDisplayName = route_list['legs'][0]['flight']['craftTypeKindDisplayName']
                lowest_price = route_list['legs'][0]['characteristic']['lowestPrice']
                standardPrices_Y = route_list['legs'][0]['characteristic']['standardPrices'][0]['price']
                standardPrices_C = route_list['legs'][0]['characteristic']['standardPrices'][1]['price']
                standardPrices_F = route_list['legs'][0]['characteristic']['standardPrices'][2]['price']
                stop_times = route_list['legs'][0]['flight']['stopTimes']
                if stop_times != 0 :
                    stop_time = route_list['legs'][0]['flight']['stopInfo'][0]['dateRange']['endDate']
                    stop_city = route_list['legs'][0]['flight']['stopInfo'][0]['cityName']
                    stop_city_code = route_list['legs'][0]['flight']['stopInfo'][0]['cityCode']
                else:
                    stop_time = "Null"
                    stop_city = "Null"
                    stop_city_code = "Null"
                print(src_name, des_name, airlineName, flightNumber, departure_data, arrival_data, stop_time,
                      punctualityRate, lowest_price, standardPrices_C, standardPrices_F, standardPrices_Y)
            else:
                print("空铁特惠组合")
            i = i + 1


if __name__ == "__main__":
    singleAirlines = GetSingleLowPrice("BJS", 1, "北京", "XMN", 25, "厦门", "ctrip_single_airlines")
    airlines_ctrip = singleAirlines.get_ctrip_airlines()
    multi_airlines = ParseMultiAirlines(airlines_ctrip)
    multi_airlines.parse_multi_airlines()