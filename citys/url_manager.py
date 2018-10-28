class DefReqUrl:
    def get_ctrip_url_citys(self):
        self.citys_url = "https://flights.ctrip.com/itinerary/api/poi/get"
        return self.citys_url

    def get_ctrip_url_lowest_price(self):
        self.lowest_price_url = "http://flights.ctrip.com/itinerary/api/12808/lowestPrice"
        return self.lowest_price_url

    def get_ctrip_oneway_airlines_products(self):
        self.single_airlines_product_url = "https://flights.ctrip.com/itinerary/api/12808/products"
        return self.single_airlines_product_url