# -*- coding:utf-8 -*-
import os
import time
import re
import urllib.request
import pymysql
import shutil
import json
import heapq
import math
import matplotlib.pyplot as plt
import threadpool
#python 3.0自带的未来趋势的模块
from concurrent.futures import ThreadPoolExecutor

class ModelStockNetShare:

    def __init__(self, *argv):
        if len(argv) == 1:
            self.cal_list = argv[0]
        elif len(argv) == 3:
            self.max_days = argv[1]
            self.codes_list = argv[0]
            self.isGetNewSource = argv[2]


    def GetHistoryData(self):
        threads = 10
        pool = threadpool.ThreadPool(threads)
        if self.isGetNewSource == "true":
            requests = threadpool.makeRequests(self.GetHistoryMoneyNewSource, self.codes_list)
            for req in requests:
                pool.putRequest(req)
            pool.wait()
        else:
            requests = threadpool.makeRequests(self.GetHistoryMoney, self.codes_list)
            for req in requests:
                pool.putRequest(req)
            pool.wait()

    def GetHistoryMoneyNewSource(self, coder):
        print("=====开始获取股票%s历史资金数据=====" % coder)
        f_path = ""
        fail_code_list = []
        div_number = int(coder) % divs
        print(div_number)
        s_json = {}

        if coder[0] == "6":
            f_path = foutpath_sh + '/' + str(div_number)
            types = 1
        elif coder[0] == "0":
            f_path = foutpath_sz + '/' + str(div_number)
            types = 2
        elif coder[0] == "3":
            f_path = foutpath_cyb + '/' + str(div_number)
            types = 2
        if os.path.exists(f_path + '/' + 'new_' + coder + '_' + str(div_number) + '_' + 'moneyHistory'):
            os.remove(f_path + '/' + 'new_' + coder + '_' + str(div_number) + '_' + 'moneyHistory')
        t = time.time()
        times = int(round(t * 1000))
        url1 = "http://ff.eastmoney.com//EM_CapitalFlowInterface/api/js?type=hff&rtntype=2&"
        url2 = "js=({data:[(x)]})&cb=var%20aff_data=&check=TMLBMSPROCR&"
        token = "acces_token=1942f5da9b46b069953c873404aad4b5&"
        ids = "id=" + coder + str(types) + "&_=" + str(times)
        url = url1 + url2 + token + ids
        try:
            response = urllib.request.urlopen(url)
        except Exception:
            response = urllib.request.urlopen(url)
        raw_data = response.read().decode('utf-8')
        info = raw_data.split('=')[1].strip('({data:})')
        print(info)
        s_info = r'\d{4}[-/]?\d{2}[-/]?\d{2}'
        pat_info = re.compile(s_info)
        dates = pat_info.findall(info)
        print(dates)
        nums = len(dates)
        info_1 = info.split(',')
        print(info_1)
        if nums * 13 != len(info_1) and nums == 0:
            fail_code_list.append(coder)
            return
        i = 0
        j = 0
        while i < len(info_1):
            info_date = info_1[i].strip('[[\"')
            # 主力净流入（万元）= 超大单净流入+大单净流入
            info_zhuli_jlr = info_1[i+1]
            # 主力净流入占比（净流入/成交额）
            info_zhuli_jlr_percent = info_1[i+2]
            # 超大单净流入（万元）
            info_super_jlr = info_1[i+3]
            info_super_jlr_percent = info_1[i+4]
            if info_super_jlr_percent == '-':
                info_super_jlr_percent = "0%"
            # 大单净流入（万元）
            info_big_jlr = info_1[i+5]
            info_big_jlr_percent = info_1[i+6]
            if info_big_jlr_percent == '-':
                info_big_jlr_percent = "0%"
            # 中单净流入（万元）
            info_middle_jlr = info_1[i+7]
            info_middle_jlr_percent = info_1[i+8]
            if info_middle_jlr_percent == '-':
                info_middle_jlr_percent = "0%"
            # 小单净流入（万元）
            info_small_jlr = info_1[i+9]
            info_small_jlr_percent = info_1[i+10]
            if info_small_jlr_percent == '-':
                info_small_jlr_percent = "0%"
            # 收盘价
            info_end_price = info_1[i+11]
            # 涨跌幅
            info_change_percent = info_1[i+12].strip('\"]]')

            s_json[dates[j]] = {}
            s_json[dates[j]]["end_price"] = info_end_price
            s_json[dates[j]]["change_percent"] = info_change_percent
            s_json[dates[j]]["zhuli_jlr"] = info_zhuli_jlr
            s_json[dates[j]]["zhuli_jlr_percent"] = info_zhuli_jlr_percent
            s_json[dates[j]]["super_jlr"] = info_super_jlr
            s_json[dates[j]]["super_jlr_percent"] = info_super_jlr_percent
            s_json[dates[j]]["big_jlr"] = info_big_jlr
            s_json[dates[j]]['big_jlr_percent'] = info_big_jlr_percent
            s_json[dates[j]]['middle_jlr'] = info_middle_jlr
            s_json[dates[j]]['middle_jlr_percent'] = info_middle_jlr_percent
            s_json[dates[j]]['small_jlr'] = info_small_jlr
            s_json[dates[j]]['small_jlr_percent'] = info_small_jlr_percent

            i = i + 13
            j = j + 1
        print(s_json)
        self.WriteNewSourceToJson(f_path, coder, s_json)

    def WriteNewSourceToJson(self, path, coder, dicts):
        div_no = int(coder) % divs
        fout = path + '/' + "new_" + str(coder) + '_' + str(div_no) + '_moneyHistory'
        f2 = open(fout, 'w+')
        f_json = json.dumps(dicts, indent=4)
        f2.write(f_json)
        f2.close()

    def GetMaxPage(self, url_1, coder):
        response = urllib.request.urlopen(url_1)
        raw_data = response.read().decode('utf-8')
        s_code = r'<a href="/trade/lszjlx_' + coder + '[,0-9]*\.html">([0-9]+)</a>'
        pat = re.compile(s_code)
        info = pat.findall(raw_data)
        maxs = info[-1]
        return maxs

    def GetHistoryMoney(self, coder):
        print("=====开始获取股票%s历史资金数据=====" % coder)
        i = 0
        fail_page_list = []
        f_path = ""
        div_number = int(coder) % divs
        print(div_number)
        if self.max_days == "all":
            tmp_max_days = "all"
        else:
            tmp_max_days = int(self.max_days)
        #print("该股票历史数据总共页数为: %s, 设定的需要获取数据的天数为: %s" % (self.pages, self.max_days))
        s_json = {}

        if coder[0] == "6":
            f_path = foutpath_sh + '/' + str(div_number)
        elif coder[0] == "0":
            f_path = foutpath_sz + '/' + str(div_number)
        elif coder[0] == "3":
            f_path = foutpath_cyb + '/' + str(div_number)
        if os.path.exists(f_path + '/' + coder + '_' + str(div_number) + '_' + 'moneyHistory'):
            os.remove(f_path + '/' + coder + '_' + str(div_number) + '_' + 'moneyHistory')
        #获取每个股票历史数据的最大页数
        tmp_url = "http://quotes.money.163.com/trade/lszjlx_" + coder + ".html#01b08"
        pages = self.GetMaxPage(tmp_url, coder)

        while i < int(pages):
            #print("开始获取第 %s 页的数据..." % (i + 1))
            url = "http://quotes.money.163.com/trade/lszjlx_" + coder + "," + str(i) + ".html"
            response = urllib.request.urlopen(url)
            raw_data = response.read().decode('utf-8')
            #print(raw_data)
            s_date = r'<td class="[a-z\_]*">(\d{4}-\d{1,2}-\d{1,2})</td>'
            s_price = r'<td><span class="[a-zA-Z]*">(\d*\.+\d*)</span>'
            s_zdf = r'<td><span class="[a-zA-Z]*">(-*\d*.*\d*\%+)</span>'
            s_net_share = r'<td><span class="[a-zA-Z]*">*(-*\d*,*\d*,*-*\d*)</span>*</td>'
            s_inout = r'<td>(\d*,*\d*,*\d*)</td>'
            pat_date = re.compile(s_date)
            pat_price = re.compile(s_price)
            pat_zdf = re.compile(s_zdf)
            pat_net_share = re.compile(s_net_share)
            pat_inout = re.compile(s_inout)

            info_date = pat_date.findall(raw_data)
            info_price = pat_price.findall(raw_data)
            info_zdf = pat_zdf.findall(raw_data)
            info_net_share = pat_net_share.findall(raw_data)
            info_inout = pat_inout.findall(raw_data)

            # 删除info_inout中的空元素
            del info_inout[0]
            if len(info_date) != len(info_price) and 2*len(info_date) != len(info_net_share) and 4*len(info_date) != len(info_inout) and len(info_date) != len(info_zdf):
                print("股票%s获取第: %s 页历史资金流动数据失败!!" % (self.code, i))
                fail_page_list.append(i)
                continue

            cur_nums = len(info_date)
            if tmp_max_days == "all":
                self.WriteJsonData(coder, s_json, f_path, cur_nums, info_date, info_price, info_zdf, info_inout, info_net_share)
            else:
                left_num = tmp_max_days - cur_nums
                if left_num <= 0:
                    nums = int(tmp_max_days)
                    self.WriteJsonData(coder, s_json, f_path, nums, info_date, info_price, info_zdf, info_inout, info_net_share)
                    break
                else:
                    nums = cur_nums
                    self.WriteJsonData(coder, s_json, f_path, nums, info_date, info_price, info_zdf, info_inout, info_net_share)
                    tmp_max_days = left_num
            i = i + 1
        print("股票%s获取历史资金流动数据成功" % coder)
        #print(info_date)
        #print(info_net_share)
        #print(info_inout)
        #print(len(info_date))
        #print(len(info_net_share))
        #print(len(info_inout))

    def WriteJsonData(self, coder, s_json, fpath, nums, i_date, i_price, i_zdf, i_inout, i_net_share):
        div_number = int(coder) % divs
        j = 0
        while j < nums:
            s_json[i_date[j]] = {}
            s_json[i_date[j]]["end_price"] = i_price[j]
            s_json[i_date[j]]["change_percent"] = float(i_zdf[j].strip('%'))
            s_json[i_date[j]]["money_inout"] = i_inout[4*j:4*j+4]
            s_json[i_date[j]]["money_net_share"] = i_net_share[2*j:2*j+2]
            j = j + 1
        #f_json = json.dumps(s_json, indent=4)
        #print(len(s_json.keys()))
        fout = fpath + '/' + str(coder) + '_' + str(div_number) + '_moneyHistory'
        if os.path.exists(fout):
            f1 = open(fout, 'r')
            tmp_dict = json.load(f1)
            s_json = dict(s_json, **tmp_dict)
            f_json = json.dumps(s_json, indent=4)
            f2 = open(fout, 'w+')
            f2.write(f_json)
            f2.close()
        else:
            f2 = open(fout, 'w+')
            f_json = json.dumps(s_json, indent=4)
            f2.write(f_json)
            f2.close()

    def GetCurStockValue(self, place, code):
        url = "https://gupiao.baidu.com/stock/" + place + code + ".html"
        response = urllib.request.urlopen(url)
        raw_data = response.read().decode('utf-8')
        s_value = r'<dt>流通市值</dt><dd>(\d*.*\d*亿)</dd>'
        pat_stock = re.compile(s_value)
        info_stock_value = pat_stock.findall(raw_data)
        print(info_stock_value)
        if len(info_stock_value) == 0:
            return 0
        return info_stock_value[0]

    def FilterData(self, dics):
        threshold = 8.0
        dicts = dics.copy()
        #print(len(dicts))
        for date_item in dics.keys():
            change = float(dics[date_item]["change_percent"])
            if math.fabs(change) >= threshold:
                del dicts[date_item]
        #print(len(dicts))
        return dicts

    # 计算股票的净增股本，净增值应该有正有负，维持一个稳定值，可能是0，可能是与发行股本之间的差值趋近于0
    def CaculateNetShare(self, coder):
        div_number = int(coder) % divs
        place = ""
        f_path = ""
        if coder[0] == "6":
            f_path = foutpath_sh + '/' + str(div_number)
            place = "sh"
        elif coder[0] == "0":
            f_path = foutpath_sz + '/' + str(div_number)
            place = "sz"
        elif coder[0] == "3":
            f_path = foutpath_cyb + '/' + str(div_number)
            place = "sz"
        try:
            f = open(f_path + '/' + str(coder) + '_' + str(div_number) + '_moneyHistory', 'r')
        except Exception:
            return
        try:
            f_new = open(f_path + '/' + 'new_' + str(coder) + '_' + str(div_number) + '_moneyHistory', 'r')
        except Exception:
            return

        dicts = json.load(f)
        dicts_new = json.load(f_new)

        # 排除历史数据中因政策导致的股票涨幅过大的数据，判断依据：跌停排除
        # dicts = self.FilterData(dicts)

        # 获取当天的流动市值
        cur_value = self.GetCurStockValue(place, coder)
        if cur_value == 0:
            return
        cur_value = float(cur_value.strip('亿'))
        # 对获取的老数据的处理
        market_value_temp = []
        money_net_share_list_temp = []
        change_percent_temp = []
        end_price_list_temp = []
        market_value_temp.append(cur_value)
        for key_date in dicts.keys():
            # 除10000表示单位亿
            net_share_1 = float(dicts[key_date]["money_net_share"][0].replace(',', ''))
            change_per_1 = dicts[key_date]["change_percent"]
            # 算出来的有数据的最早一天的流通市值
            cur_value = cur_value - float(net_share_1)/10000
            # 每天的流通市值，根据每日净流入算出
            market_value_temp.append(cur_value)
            # 获取每日净流入的资金值
            money_net_share_list_temp.append(net_share_1)
            change_percent_temp.append(change_per_1)
            end_price_list_temp.append(dicts[key_date]["end_price"])
        '''
        #=======求所有能获得数据的净流入资金的方差=======
        self.GetJlrFangCha(money_net_share_list_temp)
        #print(money_net_share_list_temp)

        #=======求所有能获得的数据的资金净流入与价格涨跌幅度的比值的标准差=======
        self.GetJlr_Zdf_Fangcha(money_net_share_list_temp, change_percent_temp)
        '''
        market_value_temp.pop()
        #print(market_value_temp)
        #print(len(market_value_temp))

        # ========用于获取有效的每天所有流动股数的环比差值样本数========
        # 方法1：获取分析的样本数（与发行价格最接近的那天开始作为分析样本的起始点）
        #indexs = self.GetDivValueMin(end_price_list_temp)
        # 方法2：获取分析的样本数（当天的流通股数差值为-0.33，则前n天的流通股数差值之和最接近+0.33的那一天作为起始点）
        #       分析策略：找到起始点当天的前一天与当天的涨跌趋势对比，前一天的流通股数净值和需要预测的未来一天的净值之和接近0
        # 获取每一天的流通股数差值list
        ssum, net_stock_list = self.GetAvg_hbc(market_value_temp, end_price_list_temp, "false")
        indexs, sums = self.GetDivValueSumClose(net_stock_list)

        if isGetSomeSample == "true":
            # 多获取一天的数据，用于预测未来一天的股本差值
            iindex = indexs + 2
        else:
            iindex = len(change_percent_temp)
        market_value = market_value_temp[0:iindex]
        end_price_list = end_price_list_temp[0:iindex]
        money_net_share_list = money_net_share_list_temp[0:iindex]
        change_percent_list = change_percent_temp[0:iindex]
        print("股票代码: %s, 有效的流通市值数量样本:%s,价格数量样本:%s,流通股数差值的数量样本:%s" % (coder, len(market_value), len(end_price_list), indexs))
        #print(dicts)
        #print(len(dicts.keys()))

        # =====参考指标1========每天所有流动股数的环比差值,同时求平均========
        # 因为前面多获取了一个数据，因此这里需要去除最后一个数据用于计算股数差值之和，这个值会更趋近于0
        result = self.Predict_1(sums, market_value, end_price_list)

        # =====参考指标2========历史的大单资金流入状况分析
        zhuli_jlr_percent_list = []
        for keys_new_date in dicts_new.keys():
            zhuli_jlr_per = dicts_new[keys_new_date]["zhuli_jlr_percent"].strip('%')
            if zhuli_jlr_per == "-":
                zhuli_jlr_per = 0.0
            zhuli_jlr_percent_list.append(zhuli_jlr_per)
        bzc = self.CalBzc(zhuli_jlr_percent_list)
        avgs = self.GetJlrFangCha(zhuli_jlr_percent_list)
        result_new = self.Predict_2(zhuli_jlr_percent_list, bzc, avgs)

        #各指标取交集
        f_res = open(f_result, 'a+')
        if result == "price_up" and result_new == "price_up":
            f_res.write(coder + '\n')

        #net_stock_bzc = self.CalBzc(net_stock_lists)
        #print("参考指标1（流通股数差值的标准方差是）: %s" % str(net_stock_bzc))

        # ========求有限数据中的方差=======
        #self.GetJlrFangCha(money_net_share_list)
        #self.GetJlr_Zdf_Fangcha(money_net_share_list, change_percent_list)

    # 对大单的资金流入情况做预估（机构活跃度和机构研究度）
    def Predict_2(self, lists, bzc, avgs):
        fuzhi_sum = 0
        if avgs <= 0 and float(lists[0]) < bzc:
            for i in lists:
                if float(i) <= 0.0:
                    fuzhi_sum = fuzhi_sum + 1
            if float(fuzhi_sum / len(lists)) > 0.5:
                return "price_up"
        else:
            return "price_down"


    def Predict_1(self, sums, market_value, end_price_list):
        pre_net_stock_sum = sums
        tmpsum, tmp_net_stock_lists = self.GetAvg_hbc(market_value, end_price_list, "false")
        # 用于预测的最后一天的流通股数净值
        old_old_net_stock = tmp_net_stock_lists[-1]
        old_old_price = end_price_list[-2]
        old_price = end_price_list[-3]
        tt1 = float(old_old_price) - float(old_price)
        if tt1 >= 0:
            if float(old_old_net_stock) + float(pre_net_stock_sum) >= 0:
                #print("预测结果：未来的一天该股票收盘价相对于前一天收盘价会下跌,但准确率可能只有百分之五十，跌幅在：%s" % (math.fabs(tt1)))
                return "price_down_possible"
            else:
                #print("预测结果：未来的一天该股票收盘价相对于前一天收盘价会下跌，跌幅在：%s " % (math.fabs(tt1)))
                return "price_down"
        else:
            if float(old_old_net_stock) + float(pre_net_stock_sum) < 0:
                #print("预测结果：未来的一天该股票收盘价相对于前一天收盘价会上涨,但准确率可能只有百分之五十，涨幅在: %s" % (math.fabs(tt1)))
                return "price_up_possible"
            else:
                print("预测结果：未来的一天该股票收盘价相对于前一天收盘价会上涨，涨幅在：%s " % (math.fabs(tt1)))
                return "price_up"
        pass

    # 获取净流入资金的方差，表示流动资金的变动程度
    def GetJlrFangCha(self, net_share_list):
        # 获取净流入的平均值
        sum1 = 0
        for ii in net_share_list:
            sum1 = sum1 + float(ii)
        jlr_avg = sum1 / len(net_share_list)
        # 获取标准差
        sum2 = 0
        for aa in net_share_list:
            tmp = float(aa) - float(jlr_avg)
            sum2 = sum2 + tmp**2
        jlr_std_fcha = math.sqrt(float(sum2) / (len(net_share_list)-1))
        #print("资金净流入前n天的平均值为: %s" % jlr_avg)
        #print("资金净流入前n天标准差: %s" % jlr_std_fcha)

        # 求第n天和前n-1天的标准差的比值，设为系数k1，求k1的标准差
        k_lists = []
        nn = 0
        while nn < len(net_share_list)-1:
            jlr_1 = net_share_list[nn]
            tmp_lists = net_share_list[(nn+1):len(net_share_list)]
            kk = float(jlr_1) / float(self.CalBzc(tmp_lists))
            k_lists.append(kk)
            nn = nn + 1
        print("资金净流入的第n天和前n-1天的标准差的比值分别为: %s" % str(k_lists))
        # print(len(k_lists))
        # 求k_lists的方差
        k_bzfc = self.CalBzc(k_lists)
        print("资金净流入的第n天和前n-1天的标准差的比值k的标准差为: %s" % k_bzfc)
        return jlr_avg

    # 获取资金净流入与价格涨跌幅度的比值的标准差
    def GetJlr_Zdf_Fangcha(self, jlr_list, zdf_list):
        k_jlr_zdf = []
        z = 0
        if len(jlr_list) != len(zdf_list):
            print("获取的净流入资金数据的样本数与获取的涨跌幅数据的样本数不相等!!!")
            exit(-1)
        while z < len(jlr_list):
            jlr_price = jlr_list[z]
            zdf_change = zdf_list[z]
            if zdf_change == 0:
                zdf_change == 0.0001
            k_temp = float(jlr_price) / float(zdf_change)
            k_jlr_zdf.append(k_temp)
            z = z + 1
        jlr_zdf_fangcha = self.CalBzc(k_jlr_zdf)
        print("资金净流入与涨跌幅比值前n天的标准差为: %s" % str(jlr_zdf_fangcha))

    # 计算标准差
    def CalBzc(self, lists):
        sum1 = 0
        for ii in lists:
            sum1 = float(sum1) + float(ii)
        avg = float(sum1) / float(len(lists))
        sum2 = 0
        for aa in lists:
            tmp = float(aa) - float(avg)
            sum2 = sum2 + tmp**2
        length = len(lists)
        if len(lists) == 1:
            length = 2
        # 最后两个样本，最后一个值的方差为0
        if sum2 == 0:
            return 1
        return math.sqrt(float(sum2) / (length-1))

    # 每天所有流动股数的环比差值,同时求平均
    def GetAvg_hbc(self, market_value, end_price_list, is_print):
        net_stock_nums = []
        t = 0
        while t < (len(market_value) - 1):
            c = float(market_value[t]) / float(end_price_list[t]) - float(market_value[t + 1]) / float(
                end_price_list[t + 1])
            net_stock_nums.append(c)
            t = t + 1
        every_net_stock_sum = 0
        q = 0
        while q < len(net_stock_nums):
            every_net_stock_sum = every_net_stock_sum + net_stock_nums[q]
            q = q + 1
        if is_print == "true":
            # print("当天比昨天的流通股数差值: %s" % str(net_stock_nums))
            # print("当天比昨天的流通股数差值样本数: %s" % str(len(net_stock_nums)))
            print("当天比昨天的流通股数差值的总样本数之和: %s" % str(every_net_stock_sum))
            print("参考指标1（流通股数差值的平均净值是）: %s" % str(every_net_stock_sum/len(net_stock_nums)))
            return [every_net_stock_sum, net_stock_nums]
        return [every_net_stock_sum, net_stock_nums]

    # 找到离发行价最接近的索引，从那个索引之后的数据作为数据样本，因为之前的数据从网上获取不全，因此去除
    def GetDivValueMin(self, end_price):
        sale_price = 8.89
        div_value = []
        for tmp in end_price:
            val = abs(sale_price - float(tmp))
            div_value.append(val)
        # 从div_value中找到最小值
        min_index_temp = map(div_value.index, heapq.nsmallest(1, div_value))
        min_index = list(min_index_temp)[0]
        # print("min_index: %s" % min_index)
        return min_index

    # 找更接近于0的
    def GetDivValueSumClose(self, tmp_list):
        kk = float(tmp_list[0]) + float(tmp_list[1])
        abs_kk = math.fabs(kk)
        close_index = 1
        sum1 = kk
        t = 2
        close_sum = 0
        while t < len(tmp_list):
            sum1 = sum1 + float(tmp_list[t])
            abs_sum1 = math.fabs(sum1)
            if abs_sum1 <= abs_kk:
                close_index = t
                abs_kk = abs_sum1
                close_sum = sum1
            t = t + 1
        # 这里需要加1，因为是差值样本，最后一个数据没有差值，但也要再获取数据的时候加上，因此加1
        return [close_index+1, close_sum]

    #根据数据绘制图标
    def PlotPic(self, list1, list2):
        pass

    def CalculateHistoryData(self):
        threads = 10
        pool = threadpool.ThreadPool(threads)
        requests = threadpool.makeRequests(self.CaculateNetShare, self.cal_list)
        for req in requests:
            pool.putRequest(req)
        pool.wait()


if __name__ == "__main__":
    db = pymysql.connect(host="localhost", user="", passwd="", db="stock_info", port=3306)
    cur = db.cursor()
    foutpath = "/Users/liliangliang6/Desktop/study-code/dev/stock_info"
    foutpath_sh = foutpath + "/sh"
    foutpath_sz = foutpath + "/sz"
    foutpath_cyb = foutpath + "/cyb"
    #isGetAllHistoryMoneyAgain = input("请问是否重新获取各股票的历史资金流动数据(true/false):")
    #analysis_days = input("请输入要获取并进行分析的数据的数量(天数):")
    #analysis_days = 90
    analysis_days = "all"
    isGetAllHistoryMoneyAgain = "false"
    isGetSomeSample = "true"
    isGetHistoryMoneyFromNewSource = "false"
    #isCaculateHistoryNetShare = input("请问是否对股票%s的流通股的增减净值进行分析(true/false):" % codes[0])
    isCaculateHistoryNetShare = "true"

    sql_code = "select code from stock_id"
    #sql_code = "select code from sh_stock_info where end_price <10.0 and end_price >5.0 and date_format(valid_date, '%Y-%m-%d')='2019-04-19'"
    cur.execute(sql_code)
    db.commit()
    # 把每个交易市场的股票分成多少份，分别创建一个目录
    divs = 5
    codes = cur.fetchall()
    code_list = []
    cal_code_list = []
    #存放预测出来的股票代码
    f_result = foutpath + '/stock_increase'
    '''
    if os.path.exists(f_result):
        os.remove(f_result)
    os.system('touch ' + f_result)
    '''
    print(codes)
    print(len(codes))
    #codes = ['002031']
    if isGetAllHistoryMoneyAgain == "true":
        if not os.path.exists(foutpath):
            #shutil.rmtree(foutpath)
            os.mkdir(foutpath)
            os.makedirs(foutpath_sh)
            os.makedirs(foutpath_sz)
            os.makedirs(foutpath_cyb)
        else:
            #os.mkdir(foutpath)
            if not os.path.exists(foutpath_sh) or not os.path.exists(foutpath_sz) or not os.path.exists(foutpath_cyb):
                os.makedirs(foutpath_sh)
                os.makedirs(foutpath_sz)
                os.makedirs(foutpath_cyb)
        # 分别创建divs个目录
        k = 0
        while k < divs:
            if not os.path.exists(foutpath_sh + '/' + str(k)):
                os.mkdir(foutpath_sh + '/' + str(k))
            if not os.path.exists(foutpath_sz + '/' + str(k)):
                os.mkdir(foutpath_sz + '/' + str(k))
            if not os.path.exists(foutpath_cyb + '/' + str(k)):
                os.mkdir(foutpath_cyb + '/' + str(k))
            k = k + 1

        for item in codes:
            if not item:
                print("从sql中获取股票id失败，请检查mysql的环境!!")
                exit(-1)
            code = item[0]
            #code = item
            #print(code)
            code_list.append(code)
        print(code_list)
        objs1 = ModelStockNetShare(code_list, analysis_days, isGetHistoryMoneyFromNewSource)
        objs1.GetHistoryData()

    if isCaculateHistoryNetShare == "true":
        for item in codes:
            code = item[0]
            #code = item
            cal_code_list.append(code)
        #objs2 = ModelStockNetShare(cal_code_list)
        #objs2.CalculateHistoryData()
        f_final = open(f_result, 'r')
        ff = f_final.readlines()
        #datas = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        datas = "2019-05-10"
        tmp = []
        for i in ff:
            i = i.strip('\n')
            if i[0] == "6":
                databases = "sh_stock_info"
            elif i[0] == "3":
                databases = "sz_stock_info"
            elif i[0] == "0":
                databases = "cyb_stock_info"
            sqls = "select end_price from " + databases + " where code=" + str(i) + " and date_format(valid_date, '%Y-%m-%d')=" + "\'" + datas + "\'" + ";"
            #print(sqls)
            cur.execute(sqls)
            db.commit()
            select_price = cur.fetchall()
            if len(select_price) != 0:
                s_price = select_price[0]
                if float(s_price[0]) < 5.0:
                    print("最后一天价格为:%s, 小于10元，且第二天可能上涨的股票代码: %s" % (s_price, i))





'''
def Find_min_2(a):
      
    if len(a) ==1:
        return a[0]
    else:
        return (min(a[len(a)-1], Find_min_2(a[0:len(a)-1])))
 
a=[4,1,3,5]
print(Find_min_2(a))
'''
