import pandas as pd
import operator
operator_dict = {
    'gt': operator.gt,
    'gte': operator.ge,
    'eq': operator.eq,
    'lt': operator.lt,
    'eq': operator.eq,
}

df = pd.DataFrame({'stock_id':['1','2','3','4','5']})
df2 = pd.DataFrame({'stock_id':['5','2','3','4','1']})
df2 = df2.set_index('stock_id')
df = df.set_index('stock_id')
df['apple'] = [1,2,3,4,5]
# df2['banana'] = operator_dict['gt'](*(df,5))
df2['banana'] = [False,False,True,False,False]
df2['cat'] = [True, False,True,True,True]
df2['final'] = df2.eq(True, axis=0).all(1)
print(df2)
print(operator_dict['eq'](*(df2['cat'], df2['banana'])))