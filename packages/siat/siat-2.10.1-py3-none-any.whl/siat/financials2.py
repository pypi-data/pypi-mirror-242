# -*- coding: utf-8 -*-
"""
本模块功能：计算财务报表比例，应用层
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2023年11月23日
最新修订日期：2023年11月23日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""
#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')
#==============================================================================
#本模块的公共引用
from siat.common import *
from siat.translate import *
from siat.financial_statements import *
from siat.financials import *
from siat.grafix import *
#==============================================================================
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize']=(12.8,7.2)
plt.rcParams['figure.dpi']=300
plt.rcParams['font.size'] = 13
plt.rcParams['xtick.labelsize']=11 #横轴字体大小
plt.rcParams['ytick.labelsize']=11 #纵轴字体大小

title_txt_size=16
ylabel_txt_size=14
xlabel_txt_size=14
legend_txt_size=14

#设置绘图风格：网格虚线
plt.rcParams['axes.grid']=True
#plt.rcParams['grid.color']='steelblue'
#plt.rcParams['grid.linestyle']='dashed'
#plt.rcParams['grid.linewidth']=0.5
#plt.rcParams['axes.facecolor']='whitesmoke'

#处理绘图汉字乱码问题
import sys; czxt=sys.platform
if czxt in ['win32','win64']:
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体
    mpfrc={'font.family': 'SimHei'}

if czxt in ['darwin']: #MacOSX
    plt.rcParams['font.family']= ['Heiti TC']
    mpfrc={'font.family': 'Heiti TC'}

if czxt in ['linux']: #website Jupyter
    plt.rcParams['font.family']= ['Heiti TC']
    mpfrc={'font.family':'Heiti TC'}

# 解决保存图像时'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False 
#==============================================================================
if __name__=='__main__':
    tickers=["JD","00700.HK",'BABA','09999.HK']
    fsdates='2022-12-31'
    
    analysis_type='Balance Sheet'
    analysis_type='Income Statement'
    analysis_type='Cash Flow Statement'
    
    fs_analysis(tickers,fsdates,analysis_type='balance sheet')
    fs_analysis(tickers,fsdates,analysis_type='income statement')
    fs_analysis(tickers,fsdates,analysis_type='cash flow statement')

    tickers=["000002.SZ","600266.SS",'600383.SS','600048.SS']    
    fsdates=['2021-12-31','2020-12-31','2019-12-31','2018-12-31']
    fs_analysis(tickers,fsdates,analysis_type='fs summary')
    fs_analysis(tickers,fsdates,analysis_type='financial indicator')
    
    tickers='00700.HK'
    analysis_type='profile'
    category='profile'
    fs_analysis(tickers,fsdates,analysis_type='profile')
    fs_analysis(tickers,fsdates,analysis_type='profile',category='shareholder')
    fs_analysis(tickers,fsdates,analysis_type='profile',category='dividend')
    fs_analysis(tickers,fsdates,analysis_type='profile',category='business')
    fs_analysis(tickers,fsdates,analysis_type='profile',category='business',business_period='annual')
    fs_analysis(tickers,fsdates,analysis_type='profile',category='valuation')
    fs_analysis(tickers,fsdates,analysis_type='profile',category='financial')

def fs_analysis(tickers,fsdates=[],analysis_type='balance sheet', \
                category='profile',business_period='annual', \
                printout=True,gview=False, \
                loc1='upper left',loc2='upper right', \
                ):
    """
    功能：tickers为股票列表，fsdates为财报日期，可为单个日期或日期列表
    注意1：仅从雅虎财经获取数据
    注意2：不同经济体上市公司报表币种可能不同，金额项目仅进行同公司对比，不进行公司间对比
    注意3：公司间仅对比财务比率
    注意4：不同经济体上市公司年报季报日期不同，需要列示报表日期和类型(年报或季报)
    
    business_period：取季报'quarterly'，年报'annual'，最近的6次报告'recent', 所有'all'    
    """
        
    # 统一转小写，便于判断
    analysis_type1=analysis_type.lower()
    
    import datetime as dt
    todaydt=dt.date.today().strftime('%Y-%m-%d')
    
    million=1000000
    billion=million * 1000
    
    import numpy as np
    
    if ('profile' in analysis_type1):
        # 股票需为单只股票，若为列表则仅取第一个        
        if not isinstance(tickers,str):
            if isinstance(tickers,list): tickers=tickers[0]
            else:
                print("  #Warning(fs_analysis_china): must be one ticker or first ticker in a list for",tickers)
                return        

        # 检查category
        category_list=['profile','officers','market_rates','dividend','stock_split','fin_rates','risk_general','risk_esg']
        if category not in category_list:
            print("  Unsupported category:",category,"\b. Supported categories as follows:")
            print_list(category_list,leading_blanks=2)
        
        if category == 'profile':
            info=get_stock_profile(ticker)
        elif category == 'dividend':
            info=stock_dividend(ticker,fromdate='1990-1-1',todate=todaydt)
        elif category == 'stock_split':    
            info=stock_split(ticker,fromdate='1990-1-1',todate=todaydt)
        else:
            info=get_stock_profile(ticker,info_type=category)
            
        return 
    
    elif ('balance' in analysis_type1) or ('sheet' in analysis_type1) \
         or ('asset' in analysis_type1) or ('liability' in analysis_type1):
        # 股票需为单只股票，若为列表则仅取第一个        
        if not isinstance(tickers,str):
            if isinstance(tickers,list): tickers=tickers[0]
            else:
                print("  #Warning(fs_analysis_china): must be one ticker or first ticker in a list for",tickers)
                return 
        
        # 分析资产负债表       
        fsdf=get_balance_sheet(symbol=tickers)
        
        fsdf['reportDate']=fsdf['asOfDate'].apply(lambda x: x.strftime('%y-%m-%d'))
        fsdf.set_index('reportDate',inplace=True)
        fsdf.fillna(0,inplace=True)     
        
        fsdf2=fsdf.copy()
        collist=list(fsdf2)
        for c in collist:
            try:
                fsdf2[c]=round(fsdf2[c] / billion,2)
            except:
                continue
        
        # 变换年报/季报
        fsdf2['periodType']=fsdf2['periodType'].apply(lambda x: 'Annual' if x=='12M' else 'Quarterly')
        
        # 删除不用的列
        currency=fsdf2['currencyCode'].values[0]
        droplist=['currencyCode','TA-TL-TE','asOfDate']
        fsdf2.drop(droplist,axis=1,inplace=True)

        # 打印前处理
        if printout:        
            # 降序排列
            fsdf3=fsdf2.sort_index(ascending=False)
            
            business_period=business_period.lower()
            if business_period == 'recent':
                fsdf4=fsdf3.head(6)
            elif business_period == 'quarterly':
                fsdf4=fsdf3[fsdf3['periodType']=='Quarterly']
            elif business_period == 'annual':
                fsdf4=fsdf3[fsdf3['periodType']=='Annual']   
            else:
                fsdf4=fsdf3[fsdf3['periodType']=='Annual']                
                
            # 转置
            fsdf4=fsdf4.T
            
            fsdf4.replace(0,'---',inplace=True)
            
            titletxt="\n***** "+codetranslate(tickers)+": BALANCE SHEET"+ \
                " (Based on IFRS, in unit of "+currency+' billion)'+' *****\n'
            print(titletxt)
            """
            tablefmt_list=["plain","simple","github","grid","simple_grid","rounded_grid", \
                           "heavy_grid","mixed_grid","double_grid","fancy_grid","outline", \
                           "simple_outline","rounded_outline","heavy_outline", \
                           "mixed_outline","double_outline","fancy_outline","pipe", \
                           "orgtbl","asciidoc","jira","presto","pretty","psql", \
                           "rst","mediawiki","moinmoin","youtrack","html","unsafehtml", \
                           "latex","latex_raw","latex_booktabs","latex_longtable", \
                           "textile","tsv"]
            for t in tablefmt_list:
                print("\n\n  ========== tablefmt: "+t+" ============\n")
                alignlist=['left']+['right']*(len(list(fsdf3))-1)
                print(fsdf3.to_markdown(tablefmt=t,index=True,colalign=alignlist))
            """
            #print(fsdf3)
            """
            collist=list(fsdf3)
            fsdf3['Item']=fsdf3.index
            fsdf4=fsdf3[['Item']+collist]
            pandas2prettytable(fsdf4,titletxt,firstColSpecial=False,leftColAlign='l',otherColAlign='r')
            """
            collist=list(fsdf4)
            fsdf4['Item']=fsdf4.index
            fsdf5=fsdf4[['Item']+collist]   
            
            alignlist=['left']+['right']*(len(list(fsdf5))-1)
            print(fsdf5.to_markdown(tablefmt='plain',index=False,colalign=alignlist))                
                
            footnote="\n*** Data source: Yahoo Finance, "+todaydt
            print(footnote)    
        
        return
    
    elif ('income' in analysis_type1) or ('cost' in analysis_type1) \
         or ('expense' in analysis_type1) or ('earning' in analysis_type1):
        # 股票需为单只股票，若为列表则仅取第一个        
        if not isinstance(tickers,str):
            if isinstance(tickers,list): tickers=tickers[0]
            else:
                print("  #Warning(fs_analysis_china): must be one ticker or first ticker in a list for",tickers)
                return    
        
        # 分析利润表
        fsdf=get_income_statements(symbol=tickers)
        
        fsdf['reportDate']=fsdf['asOfDate'].apply(lambda x: x.strftime('%y-%m-%d'))
        fsdf.set_index('reportDate',inplace=True)
        fsdf.fillna(0,inplace=True)     
        
        fsdf2=fsdf.copy()
        collist=list(fsdf2)
        for c in collist:
            try:
                fsdf2[c]=round(fsdf2[c] / billion,2)
            except:
                continue
        
        # 变换年报/季报
        fsdf2['periodType']=fsdf2['periodType'].apply(lambda x: 'Annual' if x=='12M' else 'Quarterly')
        
        # 删除不用的列
        currency=fsdf2['currencyCode'].values[0]
        droplist=['currencyCode','asOfDate']
        fsdf2.drop(droplist,axis=1,inplace=True)

        # 打印前处理
        if printout:        
            # 降序排列
            fsdf3=fsdf2.sort_index(ascending=False)
            
            business_period=business_period.lower()
            if business_period == 'recent':
                fsdf4=fsdf3.head(6)
            elif business_period == 'quarterly':
                fsdf4=fsdf3[fsdf3['periodType']=='Quarterly']
            elif business_period == 'annual':
                fsdf4=fsdf3[fsdf3['periodType']=='Annual']  
            else:
                fsdf4=fsdf3[fsdf3['periodType']=='Annual']                
                
            # 转置
            fsdf4=fsdf4.T
            
            fsdf4.replace(0,'---',inplace=True)
            
            titletxt="\n***** "+codetranslate(tickers)+": INCOME STATEMENTS"+ \
                " (Based on IFRS, in unit of "+currency+' billion)'+' *****\n'
            print(titletxt)
            
            collist=list(fsdf4)
            fsdf4['Item']=fsdf4.index
            fsdf5=fsdf4[['Item']+collist]   
            
            alignlist=['left']+['right']*(len(list(fsdf5))-1)
            print(fsdf5.to_markdown(tablefmt='plain',index=False,colalign=alignlist))                
                
            footnote="\n*** Data source: Yahoo Finance, "+todaydt
            print(footnote)    
        
        return
    
    elif ('cash' in analysis_type1) or ('flow' in analysis_type1):
        # 股票需为单只股票，若为列表则仅取第一个        
        if not isinstance(tickers,str):
            if isinstance(tickers,list): tickers=tickers[0]
            else:
                print("  #Warning(fs_analysis_china): must be one ticker or first ticker in a list for",tickers)
                return      
        
        # 分析现金流量表
        fsdf=get_cashflow_statements(symbol=tickers)
        
        fsdf['reportDate']=fsdf['asOfDate'].apply(lambda x: x.strftime('%y-%m-%d'))
        fsdf.set_index('reportDate',inplace=True)
        fsdf.fillna(0,inplace=True)     
        
        fsdf2=fsdf.copy()
        collist=list(fsdf2)
        for c in collist:
            try:
                fsdf2[c]=round(fsdf2[c] / billion,2)
            except:
                continue
        
        # 变换年报/季报
        fsdf2['periodType']=fsdf2['periodType'].apply(lambda x: 'Annual' if x=='12M' else 'Quarterly')
        
        # 删除不用的列
        currency=fsdf2['currencyCode'].values[0]
        droplist=['currencyCode','asOfDate']
        fsdf2.drop(droplist,axis=1,inplace=True)

        # 打印前处理
        if printout:        
            # 降序排列
            fsdf3=fsdf2.sort_index(ascending=False)
            
            business_period=business_period.lower()
            if business_period == 'recent':
                fsdf4=fsdf3.head(6)
            elif business_period == 'quarterly':
                fsdf4=fsdf3[fsdf3['periodType']=='Quarterly']
            elif business_period == 'annual':
                fsdf4=fsdf3[fsdf3['periodType']=='Annual'] 
            else:
                fsdf4=fsdf3[fsdf3['periodType']=='Annual']
                    
            # 转置
            fsdf4=fsdf4.T
            
            fsdf4.replace(0,'---',inplace=True)
            
            titletxt="\n***** "+codetranslate(tickers)+": CASHFLOW STATEMENTS"+ \
                " (Based on IFRS, in unit of "+currency+' billion)'+' *****\n'
            print(titletxt)
            
            collist=list(fsdf4)
            fsdf4['Item']=fsdf4.index
            fsdf5=fsdf4[['Item']+collist]   
            
            alignlist=['left']+['right']*(len(list(fsdf5))-1)
            print(fsdf5.to_markdown(tablefmt='plain',index=False,colalign=alignlist))                
                
            footnote="\n*** Data source: Yahoo Finance, "+todaydt
            print(footnote)    
            
        return
    
    elif ('summary' in analysis_type1):
        
        itemlist1=[
            #资产负债表
            'CashAndCashEquivalents','AccountsReceivable','Inventory', \
            'CurrentAssets','NetPPE','Goodwill','TotalAssets', \
            'CurrentLiabilities','LongTermDebt','TotalLiabilities','TotalEquities', \
            #利润表
            'TotalRevenue','GrossProfit','OperatingRevenue','OperatingIncome', \
            'GeneralAndAdministrativeExpense','EBITDA','PretaxIncome', \
            'NetIncome', \
            'NetIncomeCommonStockholders','NetIncomeContinuousOperations', \
            #现金表
            'OperatingCashFlow', \
            'FreeCashFlow', \
            ]
            
        itemlist2=[            
            #财务指标
            'BasicEPS','DilutedEPS', \
            'Gross Margin','Operating Margin','Profit Margin', \
            'Return on Equity','Return on Asset','Debt to Asset', \
            ]  
        itemlist=itemlist1+itemlist2
        
        # 股票可为单只股票(单只股票深度分析)       
        if isinstance(tickers,str):
            fsdf=get_financial_rates(tickers)
        
            fsdf['reportDate']=fsdf['asOfDate'].apply(lambda x: x.strftime('%y-%m-%d'))
            fsdf.set_index('reportDate',inplace=True)
            
            fsdf.replace([np.inf, -np.inf], np.nan, inplace=True)
            fsdf.fillna(0,inplace=True) 
            
            currency=fsdf['currencyCode'].values[0]
            
            # 变换年报/季报
            fsdf['periodType']=fsdf['periodType'].apply(lambda x: 'Annual' if x=='12M' else 'Quarterly')

            # 删除不用的列
            fsdf2=fsdf.copy()
            collist=list(fsdf2)
            keeplist=[]
            for c in itemlist:
                if c in collist:
                    keeplist=keeplist+[c]
                    if c in itemlist1:
                        try:
                            fsdf2[c]=fsdf2[c].apply(lambda x: round(x / billion,2))
                        except: pass
                    else:
                        fsdf2[c]=fsdf2[c].apply(lambda x: round(x,4))
                else: pass
                    
            keeplist=['periodType']+keeplist       
            fsdf2=fsdf2[keeplist]
    
            # 打印处理
            if printout:        
                # 降序排列
                fsdf3=fsdf2.sort_index(ascending=False)
                
                business_period=business_period.lower()
                if business_period == 'recent':
                    fsdf4=fsdf3.head(6)
                elif business_period == 'quarterly':
                    fsdf4=fsdf3[fsdf3['periodType']=='Quarterly']
                elif business_period == 'annual':
                    fsdf4=fsdf3[fsdf3['periodType']=='Annual']
                elif business_period == 'all':
                    fsdf4=fsdf3                    
                else:
                    fsdf4=fsdf3[fsdf3['periodType']=='Annual']
                    
                # 转置
                fsdf4=fsdf4.T
                
                fsdf4.replace(0,'---',inplace=True)
                
                titletxt="\n***** "+codetranslate(tickers)+": FINANCIAL STATEMENT SUMMARY"+ \
                    " (Based on IFRS, in unit of "+currency+' billion for amount items)'+' *****\n'
                print(titletxt)
                
                collist=list(fsdf4)
                fsdf4['Item']=fsdf4.index
                fsdf5=fsdf4[['Item']+collist]   
                
                alignlist=['left']+['right']*(len(list(fsdf5))-1)
                print(fsdf5.to_markdown(tablefmt='plain',index=False,colalign=alignlist))                
                    
                footnote="\n*** Data source: Yahoo Finance, "+todaydt
                print(footnote)    

            return
                
        # 股票可为股票列表(多只股票对比)        
        if isinstance(tickers,list):
            
            business_period=business_period.lower()
            fsdf=pd.DataFrame()
            for t in tickers:
                dftmp=get_financial_rates(t)
                
                if business_period=='recent':
                    dftmp2=dftmp.tail(1)
                elif business_period=='annual':
                    dftmp2=dftmp[dftmp['periodType']=='12M'].tail(1)
                elif business_period=='quarterly':
                    dftmp2=dftmp[dftmp['periodType']=='3M'].tail(1)
                else:
                    dftmp2=dftmp.tail(1)
                
                dftmp2=pd.DataFrame(dftmp2)
                fsdf=pd.concat([fsdf,dftmp2])
            
            # 变换年报/季报
            fsdf['periodType']=fsdf['periodType'].apply(lambda x: 'Annual' if x=='12M' else 'Quarterly')
            fsdf['reportDate']=fsdf['asOfDate'].apply(lambda x: x.strftime('%y-%m-%d'))
            fsdf['Name']=fsdf['ticker'].apply(lambda x: codetranslate(x))
            fsdf.set_index('Name',inplace=True)
            
            fsdf.replace([np.inf, -np.inf], np.nan, inplace=True)
            fsdf.fillna(0,inplace=True) 

            # 删除不用的列
            fsdf2=fsdf.copy()
            collist=list(fsdf2)
            keeplist=[]
            for c in itemlist:
                if c in collist:
                    keeplist=keeplist+[c]
                    if c in itemlist1:
                        try:
                            fsdf2[c]=fsdf2[c].apply(lambda x: round(x / billion,2))
                        except: pass
                    else:
                        fsdf2[c]=fsdf2[c].apply(lambda x: round(x,4))
                else: pass
                    
            keeplist=['periodType','reportDate','currencyCode']+keeplist       
            fsdf2=fsdf2[keeplist]            
    
            # 打印处理
            if printout:        
                # 降序排列
                #fsdf3=fsdf2.sort_index(ascending=False)
                fsdf4=fsdf2    
                # 转置
                fsdf4=fsdf4.T
                
                fsdf4.replace(0,'---',inplace=True)
                
                titletxt="\n***** COMPARISON OF FINANCIAL STATEMENT SUMMARY *****"+ \
                         "\n (Based on IFRS, in unit of billion for amount items)\n"
                print(titletxt)
                
                collist=list(fsdf4)
                fsdf4['Item']=fsdf4.index
                fsdf5=fsdf4[['Item']+collist]   
                
                alignlist=['left']+['right']*(len(list(fsdf5))-1)
                print(fsdf5.to_markdown(tablefmt='plain',index=False,colalign=alignlist))                
                    
                footnote="\n*** Data source: Yahoo Finance, "+todaydt
                print(footnote)  

        return        
    
    elif ('indicator' in analysis_type1):
        
        itemlist=[
            #短期偿债能力
            'Current Ratio','Quick Ratio','Cash Ratio','Cash Flow Ratio', \
            'Times Interest Earned', \
            #长期偿债能力
            'Debt to Asset','Equity to Asset','Equity Multiplier','Debt to Equity', \
            'Debt Service Coverage', \
            #营运能力
            'Inventory Turnover','Receivable Turnover','Current Asset Turnover', \
            'Fixed Asset Turnover','Total Asset Turnover', \
            #盈利能力
            'Gross Margin','Operating Margin','Profit Margin', \
            'Net Profit on Costs','ROA','ROE','ROIC', \
            #股东持股
            #'Payout Ratio', \
            'Cashflow per Share', \
            #'Dividend per Share', \
            'Net Asset per Share','BasicEPS','DilutedEPS', \
            #发展潜力
            #'Revenue Growth', \
            #'Capital Accumulation', \
            #'Total Asset Growth' \
            ]        
        
        # 股票可为单只股票(单只股票深度分析)       
        if isinstance(tickers,str):
            fsdf=get_financial_rates(tickers)
        
            fsdf['reportDate']=fsdf['asOfDate'].apply(lambda x: x.strftime('%y-%m-%d'))
            fsdf.set_index('reportDate',inplace=True)
            
            fsdf.replace([np.inf, -np.inf], np.nan, inplace=True)
            fsdf.fillna(0,inplace=True) 
            
            currency=fsdf['currencyCode'].values[0]
            
            # 变换年报/季报
            fsdf['periodType']=fsdf['periodType'].apply(lambda x: 'Annual' if x=='12M' else 'Quarterly')

            # 删除不用的列
            fsdf2=fsdf.copy()
            collist=list(fsdf2)
            keeplist=[]
            for c in itemlist:
                if c in collist:
                    keeplist=keeplist+[c]
                    try:
                        fsdf2[c]=fsdf2[c].apply(lambda x: round(x,4))
                    except: pass
                else: pass
                    
            keeplist=['periodType']+keeplist       
            fsdf2=fsdf2[keeplist]
    
            # 打印处理
            if printout:        
                # 降序排列
                fsdf3=fsdf2.sort_index(ascending=False)
                
                business_period=business_period.lower()
                if business_period == 'recent':
                    fsdf4=fsdf3.head(6)
                elif business_period == 'quarterly':
                    fsdf4=fsdf3[fsdf3['periodType']=='Quarterly']
                elif business_period == 'annual':
                    fsdf4=fsdf3[fsdf3['periodType']=='Annual']
                elif business_period == 'all':
                    fsdf4=fsdf3                    
                else:
                    fsdf4=fsdf3[fsdf3['periodType']=='Annual']
                    
                # 转置
                fsdf4=fsdf4.T
                
                fsdf4.replace(0,'---',inplace=True)
                
                titletxt="\n***** "+codetranslate(tickers)+": FINANCIAL INDICATORS"+ \
                    " (Based on IFRS)"+' *****\n'
                print(titletxt)
                
                collist=list(fsdf4)
                fsdf4['Item']=fsdf4.index
                fsdf5=fsdf4[['Item']+collist]   
                
                alignlist=['left']+['right']*(len(list(fsdf5))-1)
                print(fsdf5.to_markdown(tablefmt='plain',index=False,colalign=alignlist))                
                    
                footnote="\n*** Data source: Yahoo Finance, "+todaydt
                print(footnote)    

            return
                
        # 股票可为股票列表(多只股票对比)        
        if isinstance(tickers,list):
            
            business_period=business_period.lower()
            fsdf=pd.DataFrame()
            for t in tickers:
                dftmp=get_financial_rates(t)
                
                if business_period=='recent':
                    dftmp2=dftmp.tail(1)
                elif business_period=='annual':
                    dftmp2=dftmp[dftmp['periodType']=='12M'].tail(1)
                elif business_period=='quarterly':
                    dftmp2=dftmp[dftmp['periodType']=='3M'].tail(1)
                else:
                    dftmp2=dftmp.tail(1)
                
                dftmp2=pd.DataFrame(dftmp2)
                fsdf=pd.concat([fsdf,dftmp2])
            
            # 变换年报/季报
            fsdf['periodType']=fsdf['periodType'].apply(lambda x: 'Annual' if x=='12M' else 'Quarterly')
            fsdf['reportDate']=fsdf['asOfDate'].apply(lambda x: x.strftime('%y-%m-%d'))
            fsdf['Name']=fsdf['ticker'].apply(lambda x: codetranslate(x))
            fsdf.set_index('Name',inplace=True)
            
            fsdf.replace([np.inf, -np.inf], np.nan, inplace=True)
            fsdf.fillna(0,inplace=True) 

            # 删除不用的列
            fsdf2=fsdf.copy()
            collist=list(fsdf2)
            keeplist=[]
            for c in itemlist:
                if c in collist:
                    keeplist=keeplist+[c]
                    try:
                        fsdf2[c]=fsdf2[c].apply(lambda x: round(x,4))
                    except: pass
                else: pass
                    
            keeplist=['periodType','reportDate','currencyCode']+keeplist       
            fsdf2=fsdf2[keeplist]            
    
            # 打印处理
            if printout:        
                # 降序排列
                #fsdf3=fsdf2.sort_index(ascending=False)
                fsdf4=fsdf2    
                # 转置
                fsdf4=fsdf4.T
                
                fsdf4.replace(0,'---',inplace=True)
                
                titletxt="\n***** COMPARISON OF FINANCIAL INDICATORS *****"+ \
                         "\n                (Based on IFRS)\n"
                print(titletxt)
                
                collist=list(fsdf4)
                fsdf4['Item']=fsdf4.index
                fsdf5=fsdf4[['Item']+collist]   
                
                alignlist=['left']+['right']*(len(list(fsdf5))-1)
                print(fsdf5.to_markdown(tablefmt='plain',index=False,colalign=alignlist))                
                    
                footnote="\n*** Data source: Yahoo Finance, "+todaydt
                print(footnote)  

        return        
       
    
    elif ('dupont' in analysis_type1) and (('identity' in analysis_type1) or ('analysis' in analysis_type1)):
        # 股票需为股票列表        
        if not isinstance(tickers,list):
            print("  #Warning(fs_analysis_china): must be ticker list for",tickers)
            return        
        # 日期需为一个日期        
        if not isinstance(fsdates,str):
            fsdates=fsdates[0]
            """
            print("  #Warning(fs_analysis_china): must one date for",fsdates)
            return
            """        

        # 多只股票的杜邦分析对比      
        from siat.financials_china import compare_dupont_china           
        df_db=compare_dupont_china(tickers,fsdate=fsdates,printout=printout)
        return        
    
    
    else:
        print("  #Warning(fs_analysis_china): sorry, no idea on what to do for",analysis_type)
    return


#==============================================================================
#==============================================================================
#==============================================================================