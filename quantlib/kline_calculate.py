import threading
from huobi.client.market import *

class KlineCalculate():
    def __init__(self, past_kline_data, period):
        self.period = period
        self.pkd_obj = past_kline_data
        self.kline = []
        self.pkd_obj_data()  # 将初始化对象数据列表化以方便计算
        self.last_time = self.kline[-2]       #倒是

    def get_candle(self, one_candle):
        '将一个蜡烛的信息写入列表'
        kline_one_candle = []
        kline_one_candle.append(one_candle.id)
        kline_one_candle.append(one_candle.open)
        kline_one_candle.append(one_candle.close)
        kline_one_candle.append(one_candle.low)
        kline_one_candle.append(one_candle.high)
        kline_one_candle.append(one_candle.amount)  # 成交量
        kline_one_candle.append(one_candle.vol)  # 成交额（usdt）
        kline_one_candle.append(one_candle.count)  # 笔数
        return(kline_one_candle)

    def pkd_obj_data(self):
        'past kline data 已经读取过的kline数据'
        len_pkd = len(self.pkd_obj)
        for i in range(len_pkd):
            f_k = len_pkd - i - 1
            kline_new_candle = self.get_candle(self.pkd_obj[f_k])
            self.kline.append(kline_new_candle)
        print(self.period, '历史k线已经首次写入')

    def kline_update(self, new_candle):
        'new_candle为两个两个一组的更新'
        kline_new_candle = get_candle(self, new_candle)
        now_id = kline_new_candle[0]
        if(self.last_time != now_id):
