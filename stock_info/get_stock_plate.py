import os
import re
import threadpool
import json
import urllib.request
import pymysql

class GetStockPlateInfo:

    def __init__(self, code_list, divs, new_dates, days):
        self.code_list = code_list
        self.divs = divs
        self.new_dates = new_dates
        self.maxdays = days

    #写入json的同时，写入mysql
    def GetInfo(self, code):
        db = pymysql.connect(host="localhost", user="", passwd="", db="stock_info", port=3306)
        cur = db.cursor()
        wh = code[3] + code[4] + code[5]
        url = "http://hq.stock.sohu.com/cn/" + str(wh) + "/cn_" + code + "-1.html?_=1558842299828"
        print(url)
        try:
            response = urllib.request.urlopen(url)
            raw_data = response.read().decode('gbk')
        except Exception:
            return -1
        s_info = r'\'sector\':(.*),\'price_B1'
        pat_info = re.compile(s_info)
        plate_temp = pat_info.findall(raw_data)
        tmp_list = plate_temp[0].split("],[")
        temp_info = {}
        print(self.new_dates)
        temp_info[str(self.new_dates)] = {}
        for item in tmp_list:
            plates = item.strip("[[").strip("]]")
            plate_info = plates.split(',')
            plate_num = plate_info[0]
            plate_name = plate_info[1]
            plate_change = plate_info[2]
            plate_all_addr = plate_info[3]
            temp_info[str(self.new_dates)][plate_num.strip("\'")] = {}
            temp_info[str(self.new_dates)][plate_num.strip("\'")]["plate_name"] = plate_name.strip("\'")
            temp_info[str(self.new_dates)][plate_num.strip("\'")]["plate_change"] = plate_change.strip("\'")
            temp_info[str(self.new_dates)][plate_num.strip("\'")]["plate_all_addr"] = plate_all_addr.strip("\'")
            sql = self.SqlGenerate(str(self.new_dates), plate_num, plate_name, plate_change, plate_all_addr)
            #print(sql)
            try:
                cur.execute(sql)
                db.commit()
                res = self.ClearMoreDatas(db, cur, plate_num.strip("\'"))
                if res != 0:
                    print("clear stock_plate_info is fail, the plate number is: %s" % plate_num.strip("\'"))

            except Exception as e:
                db.rollback()
                print(e)
                return -1
        self.WriteToJson(code, temp_info)
        #print(temp_info)

    def ClearMoreDicts(self):
        pass

    def ClearMoreDatas(self, db, cur, plate_num):
        sqls1 = "select count(*) from stock_plate_info where number=%s;" % plate_num
        sqls2 = "delete from stock_plate_info where number = \"%s\" and valid_date not in " % plate_num + \
                "(select a.valid_date from (select valid_date from stock_plate_info " + \
                "where number = %s order by valid_date desc limit %s) as a);" % (plate_num, int(self.maxdays))
        count = 0
        try:
            cur.execute(sqls1)
            db.commit()
            count_list = cur.fetchall()
        except Exception as e:
            db.rollback()
            print(e)
            return -1
        for i in count_list:
            count = i[0]
        if count <= int(self.maxdays):
            return 0
        else:
            try:
                cur.execute(sqls2)
                db.commit()
                return 0
            except Exception as e:
                db.rollback()
                print(e)
                return -1

    def SqlGenerate(self,valid_date, numbers, name, change, addr):
        all_record = (valid_date, numbers, name, change, addr)
        s1 = "insert into stock_plate_Info values(\"%s\", %s, %s, %s, %s)" % all_record + \
             " ON DUPLICATE KEY UPDATE valid_date=\"%s\", number=%s, name=%s, change_per=%s, addr=%s" % all_record + ";"
        return s1

    def WriteToJson(self, code, temp_info):
        foutpath = "/Users/liliangliang6/Desktop/study-code/dev/stock_info"
        foutpath_sh = foutpath + "/sh"
        foutpath_sz = foutpath + "/sz"
        foutpath_cyb = foutpath + "/cyb"
        divides = int(code) % self.divs
        tmp_path = ""
        if code[0] == "6":
            tmp_path = foutpath_sh + "/" + str(divides) + "/"
        elif code[0] == "0":
            tmp_path = foutpath_sz + "/" + str(divides) + "/"
        elif code[0] == "3":
            tmp_path = foutpath_cyb + "/" + str(divides) + "/"
        file_name = tmp_path + str(code) + "_" + str(divides) + "_stockPlateInfo"
        print(temp_info)
        if os.path.exists(file_name):
            if os.path.getsize(file_name) != 0:
                f_temp = open(file_name, 'r')
                temp_json = json.load(f_temp)
                temp_info = dict(temp_info, **temp_json)
                # 按照date排序
                date_plate_list = sorted(temp_info.items(), key=lambda k: k[0], reverse=True)

                if len(date_plate_list) > int(self.maxdays):
                    clear_tmp = len(date_plate_list) - int(self.maxdays)
                    clear_nums = 0 - int(clear_tmp)
                    clear_date = date_plate_list[clear_nums:]
                    for ii in clear_date:
                        if ii[0] in temp_info.keys():
                            del temp_info[ii[0]]
                f_w = open(file_name, 'w')
                f_w.write(json.dumps(temp_info, indent=4, ensure_ascii=False))
            else:
                f_w = open(file_name, 'w')
                f_w.write(json.dumps(temp_info, indent=4, ensure_ascii=False))
        else:
            f_w = open(file_name, 'w')
            f_w.write(json.dumps(temp_info, indent=4, ensure_ascii=False))

    def GetStockPlate(self):
        threads = 1
        pool = threadpool.ThreadPool(threads)
        print(self.code_list)
        requests = threadpool.makeRequests(self.GetInfo, self.code_list)
        for req in requests:
            pool.putRequest(req, timeout=10)
        pool.wait()


if __name__ == "__main__":
    lists = ["601988","002031"]
    new_dates = "2019-05-28"
    days = 2
    obj = GetStockPlateInfo(lists, 5, new_dates, days)
    obj.GetStockPlate()
