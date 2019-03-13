import os
import sys
import re
import urllib.request

class GetStockId:
    def __init__(self, url):
        self.url = url

    def get_stock_id(self):
        allCodeList = []
        response = urllib.request.urlopen(self.url)
        raw_data = response.read().decode('gbk')
        s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
        pat = re.compile(s)
        code = pat.findall(raw_data)
        for item in code:
            if item[0] == "6" or item[0] == "3" or item[0] == "0":
                allCodeList.append(item)
        return allCodeList



if __name__ == "__main__":
    url = "http://quote.eastmoney.com/stocklist.html"
    StockId = GetStockId(url)
    CodeList = StockId.get_stock_id()
    print(CodeList[:10])