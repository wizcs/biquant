
from huobi.client.market import *
import pandas as pd
import datetime
from talib import abstract


def get_fff(qu):
    if(qu > 0.9):
        return('C')  # 下行
    elif(qu < 0.1):
        return('A')  # 上行
    else:
        return('B')  # 穿越


def kflag_cal(kl, ma):
    te_kflag = (kl['high']-ma) / \
        (kl['high']-kl['low'])
    return(te_kflag.apply(get_fff))


class KlineCalculate():
    def __init__(self, symbol, period, update_mode=0):
        'symbol,period为标的和时间粒度选择,更新模式-0为外部手动更新kline，1为对象自动更新kline'
        self.symbol = symbol
        self.period = period
        self.sjccy = self.timestamp_up()  # 该时间下的时间戳差异
        self.market_c_kc = MarketClient(url="https://api.huobi.be")
        past_list_obj = self.market_c_kc.get_candlestick(symbol, period, 2000)
        print('k线数据已下载')
        self.kline_time = self.pkd_obj_data(past_list_obj)  # 将初始化对象数据列表化以方便计算
        self.last_time = self.kline_time.pop()[0]  # 弹出倒数第一个kline的id为上一个未经确认的k线
        self.kline_list = self.split_data_to_talib()  # 基础数据转为talib的DataFrame
        self.tai_cal()

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

    def pkd_obj_data(self, list_obj):
        'past kline data 已经读取过的kline数据从对象转到列表'
        len_pkd = len(list_obj)
        kline_time = []
        for i in range(len_pkd):
            f_k = len_pkd - i - 1
            kline_new_candle = self.get_candle(list_obj[f_k])
            kline_time.append(kline_new_candle)
        return(kline_time)

    def timestamp_up(self):
        if(self.period == "1min"):
            return 60
        elif(self.period == "5min"):
            return 300
        elif(self.period == "15min"):
            return 900
        elif(self.period == "60min"):
            return 3600

    def tai_cal(self):

        self.macd_cal = abstract.MACD
        self.ma5_cal = abstract.MA
        self.ma5_cal.parameters = {'timeperiod': 5}

        self.macd_data = self.macd_cal(self.kline_list['close'])
        self.ma5_data = self.ma5_cal(self.kline_list['close'])

        self.kflag_data = kflag_cal(
            self.kline_list, self.ma5_data)  

    def split_data_to_talib(self) -> dict:
        '将单日排序的数据结构转为talib需要的时序dict'
        open = []
        close = []
        low = []
        high = []
        volume = []

        for i in range(len(self.kline_time)):
            open.append(self.kline_time[i][1])
            close.append(self.kline_time[i][2])
            low.append(self.kline_time[i][3])
            high.append(self.kline_time[i][4])
            volume.append(self.kline_time[i][5])

        kline_data = pd.DataFrame([])
        kline_data['open'] = open
        kline_data['close'] = close
        kline_data['low'] = low
        kline_data['high'] = high
        kline_data['volume'] = volume

        return kline_data
