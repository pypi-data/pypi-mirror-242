# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
import numpy as np
import pandas as pd
import xlwings

from WindPy import w
w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒
w.isconnected()  # 判断WindPy是否已经登录成功


class OverseasOverview:
    def __init__(self, start_date, end_date, data_path):
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_hyphen = datetime.strptime(self.start_date, '%Y%m%d').strftime('%Y-%m-%d')
        self.end_date_hyphen = datetime.strptime(self.end_date, '%Y%m%d').strftime('%Y-%m-%d')
        self.data_path = data_path
        self.index_list = ['881001.WI', 'HSI.HI', 'HSTECH.HI',
                           'SPX Index', 'INDU Index', 'CCMP Index',
                           'SXXP Index', 'SX5E Index', 'UKX Index', 'CAC Index', 'DAX Index',
                           'TPX Index', 'NKY Index', 'KOSPI Index', 'VN30 Index', 'SENSEX Index']
        self.index_name_dict = {'881001.WI': '万得全A指数', 'HSI.HI': '恒生指数', 'HSTECH.HI': '恒生科技指数',
                                'SPX Index': '标普500指数', 'INDU Index': '道琼斯工业平均指数', 'CCMP Index': '纳斯达克综合指数',
                                'SXXP Index': '欧洲斯托克600指数', 'SX5E Index': '欧洲斯托克50指数', 'UKX Index': '英国富时100指数', 'CAC Index': '法国CAC40指数', 'DAX Index': '德国DAX30指数',
                                'TPX Index': '日本东证指数', 'NKY Index': '日经225指数', 'KOSPI Index': '韩国综合指数', 'VN30 Index': '越南VN30指数', 'SENSEX Index': '印度孟买30指数'}
        # self.trade_df = w.wsd("SPX.GI", "close", self.start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
        # self.trade_df['index'] = self.trade_df['index'].apply(lambda x: x.strftime('%Y%m%d'))
        # self.trade_df = self.trade_df[['index']].rename(columns={'index': 'TRADE_DATE'})
        # self.trade_df.to_hdf('{0}trade_df.hdf'.format(self.data_path), key='table', mode='w')
        self.trade_df = pd.read_hdf('{0}trade_df.hdf'.format(self.data_path), key='table')
        self.load()

    def load(self):
        self.overseas_index_daily_k = HBDB().get_overseas_index_daily_k_given_indexs(self.index_list)
        self.overseas_index_daily_k.to_hdf('{0}overseas_index_daily_k.hdf'.format(self.data_path), key='table', mode='w')
        self.overseas_index_daily_k = pd.read_hdf('{0}overseas_index_daily_k.hdf'.format(self.data_path), key='table')


    def index(self):
        index_w = w.wsd(",".join(self.index_list[:3]), "close", self.start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
        index_w['index'] = index_w['index'].apply(lambda x: x.strftime('%Y%m%d'))
        index_w = index_w.set_index('index')
        index = self.overseas_index_daily_k[['bzzsdm', 'jyrq', 'px_last']]
        index['jyrq'] = index['jyrq'].astype(str)
        index = index.pivot(index='jyrq', columns='bzzsdm', values='px_last')
        index = pd.concat([index_w, index], axis=1)
        index = index[index.index.isin(self.trade_df['TRADE_DATE'].unique().tolist())].sort_index().fillna(method='ffill')
        index = index[(index.index >= self.start_date) & (index.index <= self.end_date)]
        index = index[self.index_list].rename(columns=self.index_name_dict)

        close = index.copy(deep=True)
        close = close.T.reset_index()
        close['TYPE'] = '收盘点位'
        close = close.set_index(['TYPE', 'index']).T

        close_nav = index.dropna()
        close_nav = close_nav / close_nav.iloc[0]
        close_nav = close_nav.T.reset_index()
        close_nav['TYPE'] = '收盘点位（最大同期归一化）'
        close_nav = close_nav.set_index(['TYPE', 'index']).T

        close_ytd = index[index.index >= '20221230']
        close_ytd = close_ytd / close_ytd.iloc[0]
        close_ytd = close_ytd.T.reset_index()
        close_ytd['TYPE'] = '收盘点位（今年以来归一化）'
        close_ytd = close_ytd.set_index(['TYPE', 'index']).T

        # close_relative = index.copy(deep=True)
        # close_relative['沪深300/中证1000'] = close_relative['沪深300'] / close_relative['中证1000']
        # close_relative = close_relative[['沪深300/中证1000']]
        # close_relative = close_relative.T.reset_index()
        # close_relative['TYPE'] = '比值'
        # close_relative = close_relative.set_index(['TYPE', 'INDEX_SYMBOL']).T
        #
        # ret_1w = index.pct_change(5)
        # ret_1w = ret_1w.T.reset_index()
        # ret_1w['TYPE'] = '近一周'
        # ret_1w = ret_1w.set_index(['TYPE', 'INDEX_SYMBOL']).T
        #
        # ret_1m = index.pct_change(20 * 1)
        # ret_1m = ret_1m.T.reset_index()
        # ret_1m['TYPE'] = '近一月'
        # ret_1m = ret_1m.set_index(['TYPE', 'INDEX_SYMBOL']).T
        #
        # ret_3m = index.pct_change(20 * 3)
        # ret_3m = ret_3m.T.reset_index()
        # ret_3m['TYPE'] = '近三月'
        # ret_3m = ret_3m.set_index(['TYPE', 'INDEX_SYMBOL']).T
        #
        # ret_6m = index.pct_change(20 * 6)
        # ret_6m = ret_6m.T.reset_index()
        # ret_6m['TYPE'] = '近六月'
        # ret_6m = ret_6m.set_index(['TYPE', 'INDEX_SYMBOL']).T
        #
        # ret_1y = index.pct_change(250)
        # ret_1y = ret_1y.T.reset_index()
        # ret_1y['TYPE'] = '近一年'
        # ret_1y = ret_1y.set_index(['TYPE', 'INDEX_SYMBOL']).T
        #
        # index_2023 = index[index.index >= self.date_2023]
        # ret_2023 = index_2023 / index_2023.iloc[0] - 1
        # ret_2023 = ret_2023.T.reset_index()
        # ret_2023['TYPE'] = '2023年以来'
        # ret_2023 = ret_2023.set_index(['TYPE', 'INDEX_SYMBOL']).T
        #
        # index_2022 = index[index.index >= self.date_2022]
        # ret_2022 = index_2022 / index_2022.iloc[0] - 1
        # ret_2022 = ret_2022.T.reset_index()
        # ret_2022['TYPE'] = '2022年以来'
        # ret_2022 = ret_2022.set_index(['TYPE', 'INDEX_SYMBOL']).T
        #
        # index_2021 = index[index.index >= self.date_2021]
        # ret_2021 = index_2021 / index_2021.iloc[0] - 1
        # ret_2021 = ret_2021.T.reset_index()
        # ret_2021['TYPE'] = '2021年以来'
        # ret_2021 = ret_2021.set_index(['TYPE', 'INDEX_SYMBOL']).T
        #
        # index_2015 = index[index.index >= self.date_2015]
        # ret_2015 = index_2015 / index_2015.iloc[0] - 1
        # ret_2015 = ret_2015.T.reset_index()
        # ret_2015['TYPE'] = '2015年以来'
        # ret_2015 = ret_2015.set_index(['TYPE', 'INDEX_SYMBOL']).T

        index = pd.concat([close, close_nav, close_ytd], axis=1)#, close_relative, ret_1w, ret_1m, ret_3m, ret_6m, ret_1y, ret_2023, ret_2022, ret_2021, ret_2015], axis=1)
        index.index = map(lambda x: datetime.strptime(x, '%Y%m%d').date(), index.index)
        return index

    def valuation(self):
        index_list = ['000300', '000905', '000852', '399303', '881001']
        index_name_dict = {'000300': '沪深300', '000905': '中证500', '000852': '中证1000', '399303': '国证2000', '881001': '万得全A'}
        valuation = HBDB().read_index_daily_k_given_date_and_indexs(self.start_date, index_list)
        valuation = valuation[['zqdm', 'jyrq', 'pe']]
        valuation = valuation.rename(columns={'zqdm': 'INDEX_SYMBOL', 'jyrq': 'TRADE_DATE', 'pe': 'PE（TTM）'})
        valuation['TRADE_DATE'] = valuation['TRADE_DATE'].astype(str)
        valuation = valuation[valuation['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        valuation = valuation[(valuation['TRADE_DATE'] >= self.start_date) & (valuation['TRADE_DATE'] <= self.end_date)]
        valuation = valuation.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='PE（TTM）').sort_index()
        valuation = valuation.replace(0.0, np.nan)
        valuation = valuation[index_list].rename(columns=index_name_dict)
        valuation['IDX'] = range(len(valuation))

        pettm = valuation.copy(deep=True).drop('IDX', axis=1)
        pettm = pettm.T.reset_index()
        pettm['TYPE'] = 'PE（TTM）'
        pettm = pettm.set_index(['TYPE', 'INDEX_SYMBOL']).T

        pettm_relative = valuation.copy(deep=True)
        pettm_relative['沪深300PE（TTM）/中证1000PE（TTM）'] = pettm_relative['沪深300'] / pettm_relative['中证1000']
        pettm_relative = pettm_relative[['沪深300PE（TTM）/中证1000PE（TTM）']]
        pettm_relative = pettm_relative.T.reset_index()
        pettm_relative['TYPE'] = '比值'
        pettm_relative = pettm_relative.set_index(['TYPE', 'INDEX_SYMBOL']).T

        pettm_q1y = valuation.copy(deep=True).drop('IDX', axis=1)
        for col in list(pettm_q1y.columns):
            pettm_q1y[col] = valuation['IDX'].rolling(250 * 1).apply(lambda x: quantile_definition(x, col, valuation))
        pettm_q1y = pettm_q1y.T.reset_index()
        pettm_q1y['TYPE'] = '近一年分位水平'
        pettm_q1y = pettm_q1y.set_index(['TYPE', 'INDEX_SYMBOL']).T

        pettm_q3y = valuation.copy(deep=True).drop('IDX', axis=1)
        for col in list(pettm_q3y.columns):
            pettm_q3y[col] = valuation['IDX'].rolling(250 * 3).apply(lambda x: quantile_definition(x, col, valuation))
        pettm_q3y = pettm_q3y.T.reset_index()
        pettm_q3y['TYPE'] = '近三年分位水平'
        pettm_q3y = pettm_q3y.set_index(['TYPE', 'INDEX_SYMBOL']).T

        pettm_q5y = valuation.copy(deep=True).drop('IDX', axis=1)
        for col in list(pettm_q5y.columns):
            pettm_q5y[col] = valuation['IDX'].rolling(250 * 5).apply(lambda x: quantile_definition(x, col, valuation))
        pettm_q5y = pettm_q5y.T.reset_index()
        pettm_q5y['TYPE'] = '近五年分位水平'
        pettm_q5y = pettm_q5y.set_index(['TYPE', 'INDEX_SYMBOL']).T

        valuation = pd.concat([pettm, pettm_relative, pettm_q1y, pettm_q3y, pettm_q5y], axis=1)
        valuation.index = map(lambda x: datetime.strptime(x, '%Y%m%d').date(), valuation.index)
        return valuation

    def get_all(self):
        index = self.index()
        # valuation = self.valuation()

        filename = '{0}overseas_overview.xlsx'.format(self.data_path)
        app = xlwings.App(visible=False)
        wookbook = app.books.open(filename)
        sheet_names = [wookbook.sheets[i].name for i in range(len(wookbook.sheets))]
        index_wooksheet = wookbook.sheets['指数']
        index_wooksheet.clear()
        index_wooksheet["A1"].options(pd.DataFrame, header=1, expand='table').value =index
        # valuation_wooksheet = wookbook.sheets['估值']
        # valuation_wooksheet.clear()
        # valuation_wooksheet["A1"].options(pd.DataFrame, header=1, expand='table').value = valuation
        wookbook.save(filename)
        wookbook.close()
        app.quit()
        return


if __name__ == '__main__':
    start_date = '20070101'
    end_date = '20231103'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/overseas_overview/'
    OverseasOverview(start_date, end_date, data_path).get_all()