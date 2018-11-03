# -*- coding:utf-8 -*-

from ctrip.ctrip_single_airlines import GetSingleLowPrice


class ParseMultiAirlines:
    def __init__(self, dict_data):
        self.dict_data = dict_data

    def parse_multi_airlines(self):
        for k,v in self.dict_data.items():
            print(k,v)


if __name__ == "__main__":
    singleAirlines = GetSingleLowPrice("BJS", 1, "北京", "XMN", 25, "厦门", "ctrip_single_airlines")
    airlines_ctrip = singleAirlines.get_ctrip_airlines()
    multi_airlines = ParseMultiAirlines(airlines_ctrip)
    multi_airlines.parse_multi_airlines()