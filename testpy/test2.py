import datetime

from huobi.client.market import *
'''
def callback(CEee):
    timest = CEee.ts
    lo = datetime.datetime.fromtimestamp(timest/1000)
    time_r = lo.strftime('%Y%m%d%H%M%S')
    print(time_r)
    if(int(time_r) > 20210111214200 ):
        return;

def error(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)


market_client = MarketClient()
market_client.sub_candlestick("btcusdt", CandlestickInterval.MIN1, callback, error)
'''

import threading

class ter:
 #   def __init__(self):
 #       self.CEee = CEee

    a = 0
    def prrt(self,see):
        print(see)

    def callback(self,CEee):
        timest = CEee.ts
        lo = datetime.datetime.fromtimestamp(timest/1000)
        time_r = lo.strftime('%Y%m%d%H%M%S')
       # ter.a = time_r
      #  print(ter.a)
       # _thread.start_new_thread(prrt,('sdss',))

def error(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)

market_client = MarketClient()

iny = ter()
market_client.sub_candlestick("eth1susdt", CandlestickInterval.MIN1, iny.callback, error)
import time
time.sleep(10)
print(threading.currentThread().name)
print(threading.currentThread().ident)
#print(dir(market_client))

import time

#while 1:
 #   time.sleep(0.2)
 #   print(iny.a)
time.sleep(15)
del market_client
del iny
print('anlilaishuoyxh')
 #   break
