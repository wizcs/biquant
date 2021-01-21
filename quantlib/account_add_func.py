
class AccountAddFunc:
    '为AccountClient下,get_account_balance()得到的account_balance_list添加更多筛查方法'

    def __init__(self, abl_list):
        self.list_obj = abl_list

    def get_currency_balance(self, cur_name):
        for abl_i in self.list_obj:
            currency_name = abl_i.currency
            if ((currency_name == cur_name) and (abl_i.type == 'trade')):
                return(float(abl_i.balance))
