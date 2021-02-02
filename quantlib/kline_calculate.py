import threading
from huobi.client.market import *

class KlineCalculate():
    def __init__(self, past_kline_data):
        self.pkd_obj = past_kline_data
        self.kline = []
        self.pkd_obj_data()  # 将初始化对象数据列表化以方便计算
        self.last_time = self.kline.pop()[0]       #弹出倒数第一个kline为上一个已经确认的k线
        self.market_c_kc = MarketClient(url = "https://api.huobi.de.com")
        
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
        print('历史k线已经首次写入')

    def kline_update_15m(self,now_time,symbol):
        '15分钟k线向self.kline更新一组数据'
        if(now_time != self.last_time):
            if((now_time - self.last_time) == 900):
                list_obj = self.market_c_kc.get_candlestick(symbol, CandlestickInterval.MIN15, 2)
                self.kline.append(self.get_candle(list_obj[1]))  #如果新的更新时间大于上一次15分钟，则更新一个15分钟k线
                self.last_time = list_obj[0].id
                print('15分钟k线已经更新！当前时间戳为',self.last_time)
            else:
                print('果然还是有需要的时候')

    def kline_update_5m(self,now_time,symbol):
        '15分钟k线向self.kline更新一组数据'
        if(now_time != self.last_time):
            if((now_time - self.last_time) == 300):
                list_obj = self.market_c_kc.get_candlestick(symbol, CandlestickInterval.MIN5, 2)
                self.kline.append(self.get_candle(list_obj[1]))  #如果新的更新时间大于上一次5分钟，则更新一个15分钟k线
                self.last_time = list_obj[0].id
                print('5分钟k线已经更新！当前时间戳为',self.last_time)
            else:
                print('果然还是有需要的时候')