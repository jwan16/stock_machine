from .base import *
import pandas as pd
from stock.models import Historical_Price, Company
from model.models import Model, Model_param, Indicator, Report
import datetime
import operator
from django.core.mail import send_mail
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

stock_list = [add_zero(i.stock_id) for i in Company.objects.all()]
function_list = {
    'Moving Average': get_moving_avg,
    'Stochastic(k_fast)': get_stochastic_k_fast,
    'Stochastic(k_slow)': get_stochastic_k_slow,
    'Stochastic(d_fast)': get_stochastic_k_slow,
    'Stochastic(d_slow)': get_stochastic_d_slow,
    'MACD': get_macd,
    'MACD(EMA9)': get_macd_ema9,
}

def run(*script_args):
    result_df = pd.DataFrame({'stock_id': stock_list})
    result_df = result_df.set_index('stock_id')
    model_id = script_args[0]
    end_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    model = Model.objects.get(model_id = model_id)
    now = datetime.datetime.now()
    Report.objects.create(model = model, status='running', rundate=now)
    report = Report.objects.get(model=model, rundate=now)
    model_param = Model_param.objects.filter(model=model)
    param_list = []
    for param in model_param:
        param_list.append(param.indicator.name)
        print('Starting param ' + str(param.param_id))
        df = pd.DataFrame({'stock_id': stock_list})
        df = df.set_index('stock_id')
        argsdict = {
            'start_date': '2017-10-20',
            'end_date': end_date,
            'frequency': 'weekly',
        }
        argsdict[param.indicator.param1] = int(param.i_param1)
        try: argsdict[param.indicator.param2] = int(param.i_param2)
        except: None

            # argsdict[param.indicator.param2] = int(param.i_param2)


        for stock_id in stock_list:
            print('Analyzing param: ' + str(param.param_id) + ' stock_id: ' + str(stock_id))
            argsdict['stock_id'] = stock_id

            try:
                df.ix[stock_id,'col1'] = float(function_list[param.indicator.name](**argsdict).sort_index(ascending=False).iloc[1])
            except: None


        if param.param_type == 'value':
            result_df[str(param.param_id)] = operator_dict[param.operator](*(df['col1'],param.value))

        elif param.param_type == 'indicator':
            print('Analyzing compare_param: ')
            argsdict2 = {}
            argsdict2[param.compare_indicator.param1] = int(param.ci_param1)

            try: argsdict2[param.compare_indicator.param2] = int(param.ci_param2)
            except: None
            argsdict2['start_date'] = '2017-10-20'
            argsdict2['end_date'] = end_date
            argsdict2['frequency'] = 'weekly'


            for stock_id in stock_list:
                argsdict2['stock_id'] = stock_id
                print(argsdict2)
                try:
                    df.ix[stock_id, 'col2'] = float(function_list[param.compare_indicator.name](**argsdict2).sort_index(ascending=False).iloc[0])
                except:
                    None
            print('complete compare_param')
            df = df.dropna()
            print(df)
            if param.operator is '=':
                diff = abs((df['col2'] - df['col1']) / df['col1'])
                compare_diff = float(param.eq_diff)/100
                print(compare_diff)
                print(diff)
                result_df[str(param.param_id)] = operator.lt(*(diff, compare_diff))
            else:
                result_df[str(param.param_id)] = operator_dict[param.operator](*(df['col1'], df['col2']))

    print(result_df)
    result_df['final'] = result_df.eq(True, axis=0).all(1)
    print(result_df.index[result_df['final']].tolist())

    report.status = 'done'
    report.model_param = ','.join(param_list)
    report.result_count = len(result_df.index[result_df['final']].tolist())
    report.result_stock_id = ','.join(result_df.index[result_df['final']].tolist())
    report.save()

    # for stock_id in stock_list:
    #     print(stock_id)
    #     try:
    #         df.ix[stock_id, 'ma10'] = float(get_moving_avg(stock_id, '2017-10-20', '2017-10-30', 'daily', 10).sort_index(ascending=False).head(1))
    #     except: continue
    # return df
