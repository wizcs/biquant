
from huobi.client.trade import *  # 交易相关
from huobi.client.account import *  # 账户相关
from quantlib.account_add_func import *


class TradeByPosition():

    def __init__(self, cur, used_usdt):
        'used_usdt为该次开仓所使用总usdt，应包含当前已用仓位大致'
        import configparser
        config = configparser.ConfigParser()
        filename = 'quantlib/conf.ini'
        config.read(filename, encoding='utf-8')
        self.g_api_key = config['PRIVATE_CONFIG']['g_api_key']
        self.g_secret_key = config['PRIVATE_CONFIG']['g_secret_key']
        self.url = config['PRIVATE_CONFIG']['url']

        self.trade_c = TradeClient(api_key=self.g_api_key,
                                   secret_key=self.g_secret_key, url=self.url)
        self.account_c = AccountClient(
            api_key=self.g_api_key, secret_key=self.g_secret_key, url=self.url)
        # 多空命名
        self.cur = cur
        self.cur_s = cur + '1s'
        self.long_cur = cur + 'usdt'
        self.short_cur = cur + '1susdt'
        self.used_usdt = used_usdt
        self.check_account()

    def check_account(self):
        '获取最初账户信息，包括当前查询币种'
        account_balance = self.account_c.get_balance('10811886')
        AAFunc = AccountAddFunc(account_balance)
        self.ab_usdt = AAFunc.get_currency_balance('usdt')
        self.ab_cur_l = AAFunc.get_currency_balance(self.cur)
        self.ab_cur_s = AAFunc.get_currency_balance(self.cur_s)
        del AAFunc
        del account_balance
        print('已获取当前信息：ab_cur_l=', self.ab_cur_l, 'ab_cur_s=',
              self.ab_cur_s, 'usdt = ', self.ab_usdt)

    def cal_now_postion(self):
        now_postion = 0
        if(self.ab_cur_l > 0.002):
            now_postion = 1-(self.ab_usdt/self.used_usdt)
            print('当前仓位是', now_postion)
        if(self.ab_cur_s > 0.002):
            now_postion = (self.ab_usdt/self.used_usdt)-1
            print('当前仓位是', now_postion)
        return now_postion

    def change_position_to(self, postion_flag):
        now_postion = self.cal_now_postion()
        if(postion_flag == 0):
            self.close_position()

        elif(postion_flag > 0):  # 开多仓
            if(now_postion < 0):  # 如果当前空仓，那就先平了再买
                self.close_position()
                p_amount = self.used_usdt*postion_flag
                p_amount = int(p_amount * 10000) / 10000
                try:
                    order_id = self.trade_c.create_order(symbol=self.long_cur, account_id='10811886',
                                                         order_type=OrderType.BUY_MARKET, source=OrderSource.API, amount=p_amount, price=None)
                    print('订单成交', order_id)
                except:
                    print('此仓建立失败')

            elif((now_postion >= 0) and (now_postion < postion_flag)):  # 如果需要加仓
                p_amount = self.used_usdt*(postion_flag-now_postion)  # 需加仓位
                p_amount = int(p_amount * 10000) / 10000
                try:
                    order_id = self.trade_c.create_order(symbol=self.long_cur, account_id='10811886',
                                                         order_type=OrderType.BUY_MARKET, source=OrderSource.API, amount=p_amount, price=None)
                    print('订单成交', order_id)
                except:
                    print('此仓建立失败')

            elif(now_postion > postion_flag):  # 需减仓位
                p_amount = self.ab_cur_l*(now_postion-postion_flag)
                p_amount = int(p_amount * 10000) / 10000
                try:
                    order_id = self.trade_c.create_order(symbol=self.long_cur, account_id='10811886',
                                                         order_type=OrderType.SELL_MARKET, source=OrderSource.API, amount=p_amount, price=None)
                    print('订单成交', order_id)
                except:
                    print('此仓建立失败')

        else:  # 开空仓
            if(now_postion > 0):  # 如果当前多仓，那就先平了再开空
                self.close_position()
                p_amount = -self.used_usdt*postion_flag
                p_amount = int(p_amount * 10000) / 10000
                try:
                    order_id = self.trade_c.create_order(symbol=self.short_cur, account_id='10811886',
                                                         order_type=OrderType.BUY_MARKET, source=OrderSource.API, amount=p_amount, price=None)
                    print('订单成交', order_id)
                except:
                    print('此仓建立失败')

            elif((now_postion <= 0) and (now_postion > postion_flag)):  # 如果需要加仓
                p_amount = self.used_usdt*(now_postion-postion_flag)  # 需加仓位
                p_amount = int(p_amount * 10000) / 10000
                try:
                    order_id = self.trade_c.create_order(symbol=self.short_cur, account_id='10811886',
                                                         order_type=OrderType.BUY_MARKET, source=OrderSource.API, amount=p_amount, price=None)
                    print('订单成交', order_id)
                except:
                    print('此仓建立失败')

            elif(now_postion < postion_flag):  # 需减仓位
                p_amount = self.ab_cur_l*(postion_flag-now_postion)
                p_amount = int(p_amount * 10000) / 10000
                try:
                    order_id = self.trade_c.create_order(symbol=self.short_cur, account_id='10811886',
                                                         order_type=OrderType.SELL_MARKET, source=OrderSource.API, amount=p_amount, price=None)
                    print('订单成交', order_id)
                except:
                    print('此仓建立失败')

        self.check_account()

    def close_position(self):
        # '将全部仓位调为0或以进行反向开仓'
        if(self.ab_cur_l > 0.001):
            ab_cur_l_amount = int(self.ab_cur_l * 10000) / 10000
            order_id = self.trade_c.create_order(symbol=self.long_cur, account_id='10811886',
                                                 order_type=OrderType.SELL_MARKET, source=OrderSource.API, amount=ab_cur_l_amount, price=None)
            print('多仓已平')
        if(self.ab_cur_s > 0.001):
            ab_cur_s_amount = int(self.ab_cur_s * 10000) / 10000
            order_id = self.trade_c.create_order(symbol=self.short_cur, account_id='10811886',
                                                 order_type=OrderType.SELL_MARKET, source=OrderSource.API, amount=ab_cur_s_amount, price=None)
            print('空仓已平')
        self.check_account()

'''
这个当前仓位计算方法傻逼了废弃！！！！！！
def cal_now_postion(self, now_price):
        now_postion = 0
        if(self.ab_cur_l > 0.001):
            cur_usdt = self.ab_cur_l * now_price
            now_postion = cur_usdt/(cur_usdt+ab_usdt)
            print('当前多仓位', now_postion)
        elif(self.ab_cur_s > 0.001):
            cur_usdt = self.ab_cur_l * now_price
            now_postion = -cur_usdt/(cur_usdt+ab_usdt)
            print('当前空仓位', -now_postion)
        return now_postion
'''
