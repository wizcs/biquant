'''
from huobi.client.account import AccountClient
from huobi.constant import *

g_api_key="5407877e-mjlpdje3ld-fb1ca142-09617"
g_secret_key="2a96b9fc-f4c625bd-07f1f440-d5a68"
g_account_id='10811886'

# get accounts
from huobi.utils import *

account_client = AccountClient(api_key=g_api_key,
                              secret_key=g_secret_key)
list_obj = account_client.get_balance(account_id=g_account_id)

'''



'''

from huobi.client.market import *
def callback(candlestick_event):
    candlestick_event.print_object()
    print("\n")

def error(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)

mark_c = MarketClient()
mark_c.sub_trade_detail("btcusdt", callback)

'''


import pyecharts.options as opts
from pyecharts.charts import Bar, Line

bar = (
    Bar(init_opts = opts.InitOpts(width="500px", height="300px"))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    .add_yaxis("商家B", [15, 6, 45, 20, 35, 66])
 #   .set_global_opts(Init_opts = opts.InitOpts(width="500px", height="300px"))
    
)

bar.render()
