import threading
class KlineCalculate():

    def __init__(self,past_kline_data):
        self.pkd_obj = past_kline_data
        self.kline = []
    
    def pkd_obj_data(self):
        len_pkd = len(self.pkd_obj)
        for i in range(len_pkd):
            kline_onetime = []
            f_k = len_pkd - i -1
            kline_onetime.append(self.pkd_obj[f_k].id)
            kline_onetime.append(self.pkd_obj[f_k].open)
            kline_onetime.append(self.pkd_obj[f_k].close)
            kline_onetime.append(self.pkd_obj[f_k].low)
            kline_onetime.append(self.pkd_obj[f_k].high)
            kline_onetime.append(self.pkd_obj[f_k].amount) #成交量
            kline_onetime.append(self.pkd_obj[f_k].vol) #成交额（usdt）
            kline_onetime.append(self.pkd_obj[f_k].vol) #笔数
            self.kline.append(kline_onetime)
        print('历史k线已经读取')