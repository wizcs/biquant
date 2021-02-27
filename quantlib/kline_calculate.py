
from huobi.client.market import *
import pandas as pd
import datetime
import quantlib.bqlog as bq

# 卧槽我吐了断断续续写点这种垃圾代码，每次自己都不记得写了啥然后重新研究日日日日日日日日日
# 大年初三决定重新写这个函数了，太扯淡了之前的，整个体系都乱了
# 大年初五都过了的凌晨我还在写，日了我怎么拖延症啊！！！
# 此kline_calculate类为k线计算与更新和存储类，在构造方法中传入此k线的信息：标的，时间区间,之后此对象将包含一个不断更新的kline数据，（手动或自动）
# kline_time为以每一个蜡烛信息为一组的列表，kline_list是以o、c、l、h等为一组的列表用以提供给talib计算指标。


class KlineCalculate():
    def __init__(self, symbol, period, update_mode=0):
        'symbol,period为标的和时间粒度选择,更新模式-0为外部手动更新kline，1为对象自动更新kline'
        self.symbol = symbol
        self.period = period
        self.sjccy = self.timestamp_up()  # 该时间下的时间戳差异
        self.market_c_kc = MarketClient(url="https://api.huobi.be")
        past_list_obj = self.market_c_kc.get_candlestick(symbol, period, 1000)
        self.kline_time = self.pkd_obj_data(past_list_obj)  # 将初始化对象数据列表化以方便计算
        self.last_time = self.kline_time.pop()[0]  # 弹出倒数第一个kline的id为上一个未经确认的k线
        self.kline_list = self.split_data_to_talib()  # 基础数据转为talib的DataFrame
        print(period, '历史k线已经首次写入')
        self.tai_cal()

    def readconf(self):
        import configparser
        config = configparser.ConfigParser()
        filename = 'quantlib/conf.ini'
        config.read(filename, encoding='utf-8')
       # self.g_api_key = config['PRIVATE_CONFIG']['n_api_key']
       # self.g_secret_key = config['PRIVATE_CONFIG']['n_secret_key']
        self.url = config['PRIVATE_CONFIG']['url']

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

    def update_kline_time(self):
        '更新此k线的全部数据'
        list_obj = self.market_c_kc.get_candlestick(
            self.symbol, self.period, 2)

        if((list_obj[0].id - self.last_time) == self.sjccy):
            self.last_time = list_obj[0].id
            self.kline_time.append(self.get_candle(
                list_obj[1]))  # klinetime型数据更新
            self.kline_list = self.kline_list.append(  # klinelist型数据更新
                [{'open': list_obj[1].open, 'close':list_obj[1].close, 'low':list_obj[1].low, 'high':list_obj[1].high, 'volume':list_obj[1].vol}])
            print(self.period, 'k线已在', self.last_time, '更新')
            self.tai_update()
        else:
            print('时间更新出错啦！！时间应该是', self.sjccy, '但现在是',
                  (list_obj[0].id - self.last_time))

    def tai_cal(self):
        return()
        '这是全部可直接利用的该时间区间下全部数据DataFrame,包括不断更新的para,在构造方法中初始化此方法包括当前k线的各类判决条件'

    def tai_update(self):
        '技术指标数据更新'
        return()

    def split_data_to_echarts(self) -> dict:
        'ecahrt柱状图需要的非更新数据'
        datas = []
        times = []
        vols = []

        for i in range(len(self.kline_time)):
            datas.append(self.kline_time[i][1:5])
            ca = datetime.datetime.fromtimestamp(self.kline_time[i][0])
            times.append(ca.strftime('%m-%d %H:%M'))
            vols.append(self.kline_time[i][5])

        return {
            "datas": datas,
            "times": times,
            "vols": vols
        }

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

    def change_all(self):
        '纠错程序'


'''
    #def kline_update_15m(self, now_time, symbol):
    #   '15分钟k线向self.kline_time更新一组数据,暂时废弃用于外部比对时间即可'
    #     if(now_time != self.last_time):
    #         if((now_time - self.last_time) == 900):
    #             list_obj = self.market_c_kc.get_candlestick(
    #                 symbol, CandlestickInterval.MIN15, 2)
    #             # 如果新的更新时间大于上一次15分钟，则更新一个15分钟k线
    #             self.kline_time.append(self.get_candle(list_obj[1]))
    #             self.last_time = list_obj[0].id
    #             print('15分钟k线已经更新！当前时间戳为', self.last_time)
    #         else:
    #             print('果然还是有需要的时候')
'''
