# -*- coding: utf-8 -*-

import os; os.chdir("S:/siat")
from siat import *
#==============================================================================

g=dupont_decompose_china(ticker='601398.SS',fsdate='2022-12-31')
g=dupont_decompose_china(ticker='601398.SS',fsdate='2022-12-31')


g=dupont_decompose_china(ticker='601628.SS',fsdate='2022-12-31')
#==============================================================================
import akshare as ak
df = ak.stock_financial_abstract("000002")
df = ak.stock_financial_abstract("601398")
"""
['归母净利润',
 '营业总收入',
 '营业成本',
 '净利润',
 '扣非净利润',
 '股东权益合计(净资产)',
 '商誉',
 '经营现金流量净额',
 '基本每股收益',
 '每股净资产',
 '每股现金流',
 '净资产收益率(ROE)',
 '总资产报酬率(ROA)',
 '毛利率',
 '销售净利率',
 '期间费用率',
 '资产负债率',
 '基本每股收益',
 '稀释每股收益',
 '摊薄每股净资产_期末股数',
 '调整每股净资产_期末股数',
 '每股净资产_最新股数',
 '每股经营现金流',
 '每股现金流量净额',
 '每股企业自由现金流量',
 '每股股东自由现金流量',
 '每股未分配利润',
 '每股资本公积金',
 '每股盈余公积金',
 '每股留存收益',
 '每股营业收入',
 '每股营业总收入',
 '每股息税前利润',
 '净资产收益率(ROE)',
 '摊薄净资产收益率',
 '净资产收益率_平均',
 '净资产收益率_平均_扣除非经常损益',
 '摊薄净资产收益率_扣除非经常损益',
 '息税前利润率',
 '总资产报酬率',
 '总资本回报率',
 '投入资本回报率',
 '息前税后总资产报酬率_平均',
 '毛利率',
 '销售净利率',
 '成本费用利润率',
 '营业利润率',
 '总资产净利率_平均',
 '总资产净利率_平均(含少数股东损益)',
 '归母净利润',
 '营业总收入',
 '净利润',
 '扣非净利润',
 '营业总收入增长率',
 '归属母公司净利润增长率',
 '经营活动净现金/销售收入',
 '经营性现金净流量/营业总收入',
 '成本费用率',
 '期间费用率',
 '销售成本率',
 '经营活动净现金/归属母公司的净利润',
 '所得税/利润总额',
 '流动比率',
 '速动比率',
 '保守速动比率',
 '资产负债率',
 '权益乘数',
 '权益乘数(含少数股权的净资产)',
 '产权比率',
 '现金比率',
 '应收账款周转率',
 '应收账款周转天数',
 '存货周转率',
 '存货周转天数',
 '总资产周转率',
 '总资产周转天数',
 '流动资产周转率',
 '流动资产周转天数',
 '应付账款周转率']

"""

df2 = ak.stock_financial_analysis_indicator("000002")
df2 = ak.stock_financial_analysis_indicator("601398")
"""
['日期',
 '摊薄每股收益(元)',
 '加权每股收益(元)',
 '每股收益_调整后(元)',
 '扣除非经常性损益后的每股收益(元)',
 '每股净资产_调整前(元)',
 '每股净资产_调整后(元)',
 '每股经营性现金流(元)',
 '每股资本公积金(元)',
 '每股未分配利润(元)',
 '调整后的每股净资产(元)',
 '总资产利润率(%)',
 '主营业务利润率(%)',
 '总资产净利润率(%)',
 '成本费用利润率(%)',
 '营业利润率(%)',
 '主营业务成本率(%)',
 '销售净利率(%)',
 '股本报酬率(%)',
 '净资产报酬率(%)',
 '资产报酬率(%)',
 '销售毛利率(%)',
 '三项费用比重',
 '非主营比重',
 '主营利润比重',
 '股息发放率(%)',
 '投资收益率(%)',
 '主营业务利润(元)',
 '净资产收益率(%)',
 '加权净资产收益率(%)',
 '扣除非经常性损益后的净利润(元)',
 '主营业务收入增长率(%)',
 '净利润增长率(%)',
 '净资产增长率(%)',
 '总资产增长率(%)',
 '应收账款周转率(次)',
 '应收账款周转天数(天)',
 '存货周转天数(天)',
 '存货周转率(次)',
 '固定资产周转率(次)',
 '总资产周转率(次)',
 '总资产周转天数(天)',
 '流动资产周转率(次)',
 '流动资产周转天数(天)',
 '股东权益周转率(次)',
 '流动比率',
 '速动比率',
 '现金比率(%)',
 '利息支付倍数',
 '长期债务与营运资金比率(%)',
 '股东权益比率(%)',
 '长期负债比率(%)',
 '股东权益与固定资产比率(%)',
 '负债与所有者权益比率(%)',
 '长期资产与长期资金比率(%)',
 '资本化比率(%)',
 '固定资产净值率(%)',
 '资本固定化比率(%)',
 '产权比率(%)',
 '清算价值比率(%)',
 '固定资产比重(%)',
 '资产负债率(%)',
 '总资产(元)',
 '经营现金净流量对销售收入比率(%)',
 '资产的经营现金流量回报率(%)',
 '经营现金净流量与净利润的比率(%)',
 '经营现金净流量对负债比率(%)',
 '现金流量比率(%)',
 '短期股票投资(元)',
 '短期债券投资(元)',
 '短期其它经营性投资(元)',
 '长期股票投资(元)',
 '长期债券投资(元)',
 '长期其它经营性投资(元)',
 '1年以内应收帐款(元)',
 '1-2年以内应收帐款(元)',
 '2-3年以内应收帐款(元)',
 '3年以内应收帐款(元)',
 '1年以内预付货款(元)',
 '1-2年以内预付货款(元)',
 '2-3年以内预付货款(元)',
 '3年以内预付货款(元)',
 '1年以内其它应收款(元)',
 '1-2年以内其它应收款(元)',
 '2-3年以内其它应收款(元)',
 '3年以内其它应收款(元)']

"""
fbs = ak.stock_financial_report_sina(stock="000002", symbol="资产负债表")
fis = ak.stock_financial_report_sina(stock="000002", symbol="利润表")
fcf = ak.stock_financial_report_sina(stock="000002", symbol="现金流量表")

#==============================================================================


#==============================================================================