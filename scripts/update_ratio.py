import bs4 as bs
import urllib.request
from stock.models import Ratio, Company
import re
from socket import error as SocketError
import errno


stock_list = [int(i.stock_id) for i in Company.objects.distinct()]
year_list = ['2012-12-01','2013-12-01', '2014-12-01', '2015-12-01', '2016-12-01']

#

# Financial Ratio
ratio_url = 'http://www.aastocks.com/en/stocks/analysis/company-fundamental/financial-ratios?symbol='
ratio_dict = {'Current Ratio (X)': 'current_ratio', 'Dividend Payout (%)': 'div_payout', 'Fiscal Year High': 'fiscal_year_high', 'Fiscal Year Low': 'fiscal_year_low', 'Fiscal Year PER Range High (X)': 'fiscal_year_per_high', 'Fiscal Year PER Range Low (X)': 'fiscal_year_per_low', 'Fiscal Year Yield Range High (%)': 'fiscal_year_yield_high', 'Fiscal Year Yield Range Low (%)': 'fiscal_year_yield_low', 'Inventory Turnover (X)': 'inventory_turnover', 'Long Term Debt/Equity (%)': 'longterm_de', 'Net Profit Margin (%)': 'npm', 'Operating Profit Margin (%)': 'opm', 'Pre-tax Profit Margin (%)': 'pretax_pm', 'Quick Ratio (X)': 'quick_ratio', 'Return on Capital Employ (%)': 'roce', 'Return on Equity (%)': 'roe', 'Return on Total Assets (%)': 'rota', 'Total Debt/Capital Employed (%)': 'total_de_employed', 'Total Debt/Equity (%)': 'total_de'}
#
failed_list = []
for i in stock_list:
    code = str(i)
    print(code)
    # financial-ratio
    try:
        ratio_html = urllib.request.urlopen('http://www.aastocks.com/en/stocks/analysis/company-fundamental/financial-ratios?symbol='+str(code)).read()
        ratio_soup = bs.BeautifulSoup(ratio_html,'html5lib')
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        failed_list.append(code)
        pass  # Handle error here

    if len(re.findall('No related information.', ratio_html.decode('utf-8'))) > 0:
        continue

    table_row = ratio_soup.find_all('tr')
    for tr in table_row:
        td = tr.find_all('td')
        row = [a.text.strip() for a in td]
        print(row)
        if row[0] in ratio_dict.keys():
            print(row[0])

            for a in range(1,6):
                year = year_list[a-1]
                Ratio.objects.get_or_create(stock_id = Company.objects.get(stock_id = code), date = year)
                ratio = Ratio.objects.get(stock_id = Company.objects.get(stock_id = code), date = year)

                try:
                    print(float(row[a]))
                    field = {ratio_dict[row[0]]: row[a]}
                    ratio.__dict__.update(field)
                except:
                    print('faileddddddcddddddfdfdsffdfdffdfdfdsffsffdsff')
                    pass
                ratio.save()
print(failed_list)
