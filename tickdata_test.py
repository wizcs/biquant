import datetime
from huobi.client.market import *
import threading
import time


class ter(threading.Thread):
 #   def __init__(self):
 #       self.CEee = CEee
    b = 0
    a = 0

    def prrt(self, see):
        print(see)

    def callback(self, candlestick):
        timest = candlestick.ts
        lo = datetime.datetime.fromtimestamp(timest/1000)
        time_r = lo.strftime('%Y%m%d%H%M%S')
        ter.a = time_r
        ter.b = candlestick.tick.close
        print(ter.a, 'is', ter.b)
       # _thread.start_new_thread(prrt,('sdss',))

    def error(self, e: 'HuobiApiException'):
        print('这是api系统错误', e.error_code + e.error_message)


# class sta(threading.Thread):

# def run(self):
market_client = MarketClient()
iny = ter()
market_client.sub_candlestick(
    "ethusdt", CandlestickInterval.MIN1, iny.callback, iny.error)
temp = 0
while 1:
    if (temp != iny.b):
      #  print(iny.b)
        time.sleep(0.1)
    temp = iny.b

'''
thread1 = sta()
thread1.setName('testxc')
thread1.start()
'''
