from .base import *
import pandas as pd
from stock.models import Historical_Price, Company
from model.models import Indicator
from backtest.models import Backtest, Backtest_param, Report
import datetime
import operator
import math


operator_dict = {
    '>': operator.gt,
    '>=': operator.ge,
    '=': operator.eq,
    '<': operator.lt,
    '<=': operator.le,
}



def col_name(name, param1, param2, param3):
    if param3 is not None:
        result = name + str(param1) + str(param2) + str(param3)
    elif param2 is not None:
        result = name + str(param1) + str(param2)
    elif param1 is not None:
        result = name + str(param1)
    else:
        result = name
    return result

def add_zero(stock_id):
    if len(stock_id) < 2:
        stock_id = '000' + str(stock_id)
    elif len(stock_id) < 3:
        stock_id = '00' + str(stock_id)
    elif len(stock_id) < 4:
        stock_id = '0' + str(stock_id)
    else:
        stock_id = str(stock_id)
    return stock_id

def record_param_name(param_name, param1, param2, param3):
    if param3 is not None:
        result = param_name + '(' + param1 + ',' + param2 + ',' + param3 +')'
    elif param2 is not None:
        result = param_name + '(' + param1 + ',' + param2 + ')'
    else:
        result = param_name + '(' + param1 + ')'
    return result
stock_list = [stock.stock_id for stock in Company.objects.all()]
# stock_list = ['0001', '0002', '0003', '0004', '0005', '0006', '0011', '0012', '0016', '0017', '0019', '0023', '0027', '0066', '0083', '0101', '0135', '0144', '0151', '0175', '0267', '0288', '0293', '0386', '0388', '0688', '0700', '0762', '0823', '0836', '0857', '0883', '0939', '0941', '0992', '1038', '1044', '1088', '1109', '1113', '1299', '1398', '1928', '2018', '2318', '2319', '2388', '2628', '3328', '3988']
function_list = {
    'Moving Average': get_moving_avg,
    'Stochastic(k_fast)': get_stochastic_k_fast,
    'Stochastic(k_slow)': get_stochastic_k_slow,
    'Stochastic(d_fast)': get_stochastic_k_slow,
    'Stochastic(d_slow)': get_stochastic_d_slow,

}

def run(*script_args):
    result_df = pd.DataFrame({'stock_id': stock_list})
    result_df = result_df.set_index('stock_id')

    backtest_id = script_args[0]
    backtest = Backtest.objects.get(backtest_id = backtest_id)
    now = datetime.datetime.now()
    Report.objects.create(backtest = backtest, status='running', rundate=now)
    report = Report.objects.get(backtest=backtest, rundate=now)
    backtest_param = Backtest_param.objects.filter(backtest=backtest)
    start_date = datetime.datetime.strftime(backtest.startdate, '%Y-%m-%d')
    end_date = datetime.datetime.strftime(backtest.enddate, '%Y-%m-%d')
    for stock_id in stock_list:
        print(str(stock_id))
        stock_df = pd.DataFrame()
        for param in backtest_param:
            print('Starting param ' + str(param.param_id))
            df = pd.DataFrame()
            argsdict = {
                'start_date': start_date,
                'end_date': end_date,
                'frequency': 'daily',
                'stock_id': stock_id
            }

            argsdict[param.indicator.param1] = int(param.i_param1)
            if param.indicator.param2:
                argsdict[param.indicator.param2] = int(param.i_param2)
            print(argsdict)

            df['col1'] = function_list[param.indicator.name](**argsdict)
            print(df)
            # Param Type = 'value'
            if param.param_type == 'value':
                stock_df[str(param.param_id)] = operator_dict[param.operator](*(df['col1'],param.value))

            # Param Type = 'indicator'
            elif param.param_type == 'indicator':
                print('Analyzing compare_param: ' + str(param.param_id))
                argsdict2 = {
                    'start_date': datetime.datetime.strftime(backtest.startdate, '%Y-%m-%d'),
                    'end_date': datetime.datetime.strftime(backtest.enddate, '%Y-%m-%d'),
                    'frequency': 'daily',
                    'stock_id': stock_id
                }
                argsdict2[param.compare_indicator.param1] = int(param.ci_param1)

                if param.compare_indicator.param2:
                    argsdict2[param.compare_indicator.param2] = int(param.ci_param2)

                df['col2'] = function_list[param.compare_indicator.name](**argsdict2)
                print('complete compare_param')
                print(df)
                df = df.dropna()
                stock_df[str(param.param_id)] = operator_dict[param.operator](*(df['col1'], df['col2']))
            if param.trigger:
                print('param triggered')
                print(stock_df[str(param.param_id)])
                stock_df.loc[(stock_df[str(param.param_id)] == True) & (stock_df[str(param.param_id)].shift(+1) == False), 'trigger'] = 'buy'
                stock_df.loc[(stock_df[str(param.param_id)] == False) & (stock_df[str(param.param_id)].shift(+1) == True), 'trigger'] = 'sell'

        buy_param_id = [str(i.param_id) for i in Backtest_param.objects.filter(backtest=backtest, position_type='buy', trigger=False)]
        sell_param_id = [str(i.param_id) for i in Backtest_param.objects.filter(backtest=backtest, position_type='sell', trigger=False)]

        stock_df['buy'] = stock_df[buy_param_id].eq(True, axis=0).all(1)
        stock_df['sell'] = stock_df[sell_param_id].eq(True, axis=0).all(1)

        stock_df['Close'] = get_historical_price(stock_id, start_date, end_date, 'daily')['Close']
        print(stock_df)
        capital = backtest.capital
        onstock = 0
        # print(Company.objects.get(stock_id=stock_id))
        # boardlot = Company.objects.get(stock_id=stock_id)['board_lot']
        position = 'capital'
        trigger_df = stock_df[['trigger', 'Close']].dropna()
        print(trigger_df)
        for i in range(0, trigger_df['trigger'].count()):
            if position == 'capital':
                if trigger_df['trigger'][i] == 'buy':
                    onstock = math.floor(capital / trigger_df['Close'][i])
                    capital = capital - onstock * trigger_df['Close'][i]
                    position = 'onstock'

            if position == 'onstock':
                if trigger_df['trigger'][i] == 'sell':
                    capital = capital + onstock * trigger_df['Close'][i]
                    onstock = 0
                    position = 'capital'

        if position == 'onstock':
            capital = capital + onstock * trigger_df.iloc[-1]['Close']
        print(capital)
        result_df.set_value(stock_id, 'result' , capital)
        # stock_df.loc[(stock_df['buy'] == True) & (stock_df['buy'].shift(+1) == False), 'signal'] = 'buy'
        # stock_df.loc[(stock_df['sell'] == True) & (stock_df['sell'].shift(-1) == False), 'signal'] = 'sell'
        # print(stock_df)
    print(result_df)

    # report.status = 'done'
    # report.model_param = ','.join(param_list)
    # report.result_count = len(result_df.index[result_df['final']].tolist())
    # report.result_stock_id = ','.join(result_df.index[result_df['final']].tolist())
    # report.save()

    # for stock_id in stock_list:
    #     print(stock_id)
    #     try:
    #         df.ix[stock_id, 'ma10'] = float(get_moving_avg(stock_id, '2017-10-20', '2017-10-30', 'daily', 10).sort_index(ascending=False).head(1))
    #     except: continue
    # return df
