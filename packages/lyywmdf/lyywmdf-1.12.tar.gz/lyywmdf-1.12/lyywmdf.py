import pandas as pd
import numpy as np
import MyTT
import os
import sys
import lyytools
from tqdm import tqdm
from datetime import datetime, timedelta
from pytdx.hq import TdxHq_API
import time

api_dict = {}

#项目地址：https://github.com/rainx/pytdx
#更多说明：https://rainx.gitbooks.io/pytdx/content/pytdx_hq.html
# 如果需要一些常用hosts
#from pytdx.config.hosts import hq_hosts


def 分钟线合成日K(df) -> pd.DataFrame:
    所有分钟线 = df.copy()
    所有分钟线['day'] = pd.to_datetime(所有分钟线['day'])
    完美日K线 = 所有分钟线.resample('D', on='day').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}).dropna()
    完美日K线 = 完美日K线.reset_index(drop=False)
    完美日K线['day'] = 完美日K线['day'].dt.date
    return (完美日K线)


def 多周期K线合并(完美日K线, 十点K线) -> pd.DataFrame:
    # print(十点K线['date'].tail(1).apply(type).value_counts())
    # 用每天早上情况生成新日线。其中，o,h,l,c都是9点半到10点K线。CC为当天收盘价。UP为high/ref(cc,1)
    mg1_test = 十点K线.loc[:, (
        'high',
        'day',
    )]
    mg1_test.rename(columns={'high': 'tenhigh'}, inplace=True)
    多周期合成K线 = pd.merge(完美日K线, mg1_test, on='day')

    多周期合成K线['up'] = list(map(lambda x, y: round((float(x) / float(y) - 1) * 100, 2), 多周期合成K线['high'], MyTT.REF(多周期合成K线['close'], 1)))
    多周期合成K线['chonggao'] = list(map(lambda x, y: round((float(x) / float(y) - 1) * 100, 2), 多周期合成K线['tenhigh'], MyTT.REF(多周期合成K线['close'], 1)))
    print("多周期合成K线=", 多周期合成K线['chonggao'])
    多周期合成K线['huitoubo'] = list(map(lambda x, y: round((1 - (float(x) / float(y))) * 100, 2), 多周期合成K线['close'], 多周期合成K线['high']))
    return (多周期合成K线)


def 合成完美K线(df) -> pd.DataFrame:
    df['shiftc'] = df['close'].shift(1)
    df['up'] = list(map(lambda x, y: x if x > y else y, df['close'], df['shiftc']))
    所有分钟线 = df.copy()
    所有分钟线['day'] = pd.to_datetime(所有分钟线['day'])
    新日K = 分钟线合成日K(所有分钟线)
    # print(新日K)
    新15分钟K = 分钟线5合15(所有分钟线)
    完美K线 = 多周期K线合并(新日K, 新15分钟K)
    # print(完美K线)
    return 完美K线


def 原始分钟df格式化(原始分钟df, debug=False):
    原始分钟df.drop(columns=['amount', 'year', 'month', 'day', 'hour', 'minute'], inplace=True)
    原始分钟df.columns = ['open', 'close', 'high', 'low', 'volume', 'day']

    原始分钟df['shiftc'] = 原始分钟df['close'].shift(1)
    原始分钟df['up'] = list(map(lambda x, y: x if x > y else y, 原始分钟df['close'], 原始分钟df['shiftc']))
    所有分钟线 = 原始分钟df.copy()
    所有分钟线['day'] = pd.to_datetime(所有分钟线['day'])

    新日K = 分钟线合成日K(所有分钟线)
    新15分钟K = 分钟线5合15(所有分钟线)
    print("打印15分钟K线")
    print(新15分钟K)
    完美df = 多周期K线合并(新日K, 新15分钟K)

    完美df['volume'] = 完美df['volume'].apply(lambda x: int(x / 10000))
    # 完美df['open'] = 完美df['open'].apply(lambda x: int(x * 100))
    # 完美df['close'] = 完美df['close'].apply(lambda x: int(x * 100))
    # 完美df['high'] = 完美df['high'].apply(lambda x: int(x * 100))
    # 完美df['low'] = 完美df['low'].apply(lambda x: int(x * 100))
    完美df['day'] = 完美df['day'].apply(lambda x: int(str(x)[:4] + str(x)[5:7] + str(x)[8:10]))
    # 完美df.dropna(inplace=True)

    return 完美df


def 分钟线5合15(所有分钟线) -> pd.DataFrame:
    多分钟K线 = 所有分钟线.resample('15min', on='day').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}).dropna()
    多分钟K线 = 多分钟K线.reset_index(drop=False)
    多分钟K线['time'] = 多分钟K线['day'].dt.strftime('%H%M')
    多分钟K线['day'] = 多分钟K线['day'].dt.date
    # 多分钟K线.drop(columns=['day'], inplace = True)
    十点K线 = pd.DataFrame(多分钟K线, columns=['time', 'day', 'high'])[多分钟K线['time'] == '1000']
    # 成功。从result中抽取时间和日期和最高价，生成当日的冲高数据
    return (十点K线)


def 分钟线15合15(多分钟K线):
    多分钟K线['time'] = 多分钟K线['day'].dt.strftime('%H%M')
    多分钟K线['day'] = 多分钟K线['day'].dt.date
    多分钟K线 = 多分钟K线.reset_index(drop=True)[多分钟K线['time'] <= '1000']
    df_grouped = 多分钟K线.groupby('day').max()
    #多分钟K线=多分钟K线[['day','high']]
    # 成功。从result中抽取时间和日期和最高价，生成当日的冲高数据
    df_grouped = (df_grouped.reset_index(drop=False))
    selected_columns = df_grouped[['day', 'high']]
    selected_columns.rename(columns={'high': 'chonggao'})
    print("多分钟K线\n", selected_columns)
    return (selected_columns)


def 原始15分钟df格式化(原始分钟df, debug=False):

    原始分钟df.drop(columns=['amount', 'year', 'month', 'day', 'hour', 'minute'], inplace=True)
    原始分钟df.columns = ['open', 'close', 'high', 'low', 'volume', 'day']

    原始分钟df['shiftc'] = 原始分钟df['close'].shift(1)
    原始分钟df['up'] = list(map(lambda x, y: x if x > y else y, 原始分钟df['close'], 原始分钟df['shiftc']))
    所有分钟线 = 原始分钟df.copy()
    所有分钟线['day'] = pd.to_datetime(所有分钟线['day'])
    新日K = 分钟线合成日K(所有分钟线)

    新15分钟K = 分钟线15合15(所有分钟线)
    print("原始15分钟df格式化打印15分钟K线")
    print(新15分钟K)
    完美df = 多周期K线合并(新日K, 新15分钟K)

    完美df['volume'] = 完美df['volume'].apply(lambda x: int(x / 10000))
    # 完美df['open'] = 完美df['open'].apply(lambda x: int(x * 100))
    # 完美df['close'] = 完美df['close'].apply(lambda x: int(x * 100))
    # 完美df['high'] = 完美df['high'].apply(lambda x: int(x * 100))
    # 完美df['low'] = 完美df['low'].apply(lambda x: int(x * 100))
    完美df['day'] = 完美df['day'].apply(lambda x: int(str(x)[:4] + str(x)[5:7] + str(x)[8:10]))
    # 完美df.dropna(inplace=True)

    return 完美df


def wmdf15(api, stk_code_num, to_down_kline, debug=False) -> pd.DataFrame:
    if debug:
        print("函数名：", sys._getframe().f_code.co_name, ": try to get wmdf")
    if debug:
        t0 = datetime.now()
    try:
        df = 通达信下载原始分钟K线(api, stk_code_num, to_down_kline, debug=debug)
        if df.empty:
            raise Exception("通达信下载原始分钟K线 error: DataFrame must not be empty")
    except Exception as e:
        print("Fuction: wmdf, try to run 通达信下载原始分钟线 error。stk_code_num:", stk_code_num, "to_down_kline:", to_down_kline, "api:", api, e)
        print("wmdf error:", e)
        return None
    if debug:
        lyytools.测速(t0, "通达信下载原始K线")
    t1 = datetime.now()

    try:
        wmdf = 原始15分钟df格式化(df)
    except Exception as e:
        print("error函数名：", sys._getframe().f_code.co_name, ": try to get wmdf")
        print("api=", api, " stk_code_num=", stk_code_num, " to_down_line=", to_down_kline, "try to run wmdf = 原始分钟df格式化(df) error:", e)
        return None
    if debug:
        lyytools.测速(t1, "df格式转换")
    return wmdf


def wmdf(api, stk_code_num, to_down_kline, debug=False) -> pd.DataFrame:
    if debug:
        print("函数名：", sys._getframe().f_code.co_name, ": try to get wmdf")
    if debug:
        t0 = datetime.now()
    try:
        df = 通达信下载原始分钟K线(api, stk_code_num, to_down_kline, debug=debug)
        if df.empty:
            raise Exception("通达信下载原始分钟K线 error: DataFrame must not be empty")
    except Exception as e:
        print("Fuction: wmdf, try to run 通达信下载原始分钟线 error。stk_code_num:", stk_code_num, "to_down_kline:", to_down_kline, "api:", api, e)
        print("wmdf error:", e)
        return None
    if debug:
        lyytools.测速(t0, "通达信下载原始K线")
    t1 = datetime.now()

    try:
        wmdf = 原始分钟df格式化(df)
    except Exception as e:
        print("error函数名：", sys._getframe().f_code.co_name, ": try to get wmdf")
        print("api=", api, " stk_code_num=", stk_code_num, " to_down_line=", to_down_kline, "try to run wmdf = 原始分钟df格式化(df) error:", e)
        return None
    if debug:
        lyytools.测速(t1, "df格式转换")
    return wmdf


def mk_api_list(svlist, debug=False) -> list:
    api_list = []
    if debug:
        print("函数名：", sys._getframe().f_code.co_name)

    for i in tqdm(range(len(svlist))):
        try:
            serverip, tdxport = svlist[i], 7709
            if debug:
                print("mk_api_list: try to con to ", serverip)
            exec("api" + str(i) + " = TdxHq_API(multithread=False,heartbeat=False,auto_retry=True)")
            exec("api" + str(i) + ".connect(serverip, tdxport)")
            api_list.append(eval("api" + str(i)))
        except Exception as e:

            print("mk_api_list error", e)
    print("mkapi: All done")
    return api_list


def 通达信下载原始分钟K线(api, 股票数字代码: str, 要下载的K线数量, debug=False) -> pd.DataFrame:
    """
    通达信下载原始分钟K线(tdxserverip:str, 股票数字代码:str, 开始日期:str, 结束日期, debug=False)
    """
    fun_name = sys._getframe().f_code.co_name
    t0 = datetime.now()

    if debug:
        print("函数名：", fun_name)
    市场代码 = int(股票数字代码[0].find('6')) + 1
    if debug:
        lyytools.测速(t0, "一、下载原始K线->1. tdx api connect")  # 0.05 of mainwork 0.7
    t1 = datetime.now()
    df_tdx = api.to_df(api.get_security_bars(1, 市场代码, 股票数字代码, 0, 要下载的K线数量))

    if debug:
        lyytools.测速(t1, "一、下载原始K线->2. tdx get result")  # 0.17 of mainwork 0.7
    if len(df_tdx) < 1:
        print(fun_name + " " + 股票数字代码 + ": 空数据，请检查@" + str(api) + ", to:" + str(要下载的K线数量))
    if debug: print(len(df_tdx), "条数据")
    if debug: print(df_tdx)
    return (df_tdx)


def 通达信下载原始分钟K线_simple(api, stkcode: str, 要下载的K线数量=800, debug=False) -> pd.DataFrame:
    """
    通达信下载原始分钟K线(tdxserverip:str, 股票数字代码:str, 开始日期:str, 结束日期, debug=False)
    """
    市场代码 = int(stkcode[0].find('6')) + 1
    print(f"market={市场代码}, code={stkcode}")
    tdxserverip = "120.79.210.76"
    #api.connect(tdxserverip,7709)

    df_tdx = api.to_df(api.get_security_bars(1, 市场代码, stkcode, 0, 要下载的K线数量))

    print(df_tdx)
    return (df_tdx)


def 通达信下载原始分钟K线by_ip(tdxserverip, stkcode, retry=True, debug=False):
    市场代码 = str(stkcode).zfill(6)[0].find('6') + 1
    print(f"market={市场代码}, code={stkcode}")

    api = TdxHq_API(heartbeat=True, multithread=False)
    api.connect(tdxserverip, 7709)
    df = api.to_df(api.get_security_bars(1, 市场代码, stkcode, 0, 800))
    return df
    # K线种类： 0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线 5 周K线 6 月K线 7 1分钟 81分钟K线 9 日K线 10 季K线 11 年K线


def test_servers_speed(ip, debug=False):
    """
    测试通达信服务器速度

    Args:
        ip (str): tdx服务器地址
        debug (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """

    api = TdxHq_API()
    api.connect(ip, 7709)
    start_time = time.time()

    api.get_security_count(0)
    end_time = time.time()
    api.disconnect()
    latency = end_time - start_time
    latency = round(latency, 2)
    latency_with_unit = f"{latency:.2f}秒"
    if debug:
        print("测速结果：", ip, latency_with_unit)
    return latency


def iplist_add_latency(iplist, debug=False):
    latency_dict = {}

    for i in tqdm(range(len(iplist)), desc="通达信服务器速度测试"):
        ip = iplist[i]  # 测速
        try:
            latency = test_servers_speed(ip, debug=debug)
            if latency is not None and latency < 0.1:
                latency_dict[ip] = latency
            else:
                if debug:
                    print(f"{ip}速度太慢，丢弃")
                continue
        except Exception as e:
            print("test_servers_speed error:", e)
    return latency_dict


def get_fast_tdx_server_ip_list(iplist, latency, debug=False) -> list:
    """
    获取速度快延时<latency的通达信服务器地址列表
    """
    debug = True
    latency_dict = iplist_add_latency(iplist, debug=debug)
    fast_server_ip_list = [key for key, value in latency_dict.items() if value < latency]

    return fast_server_ip_list


def df_table(df, index):
    import prettytable as pt
    #利用prettytable对输出结果进行美化,index为索引列名:df_table(df,'market')
    tb = pt.PrettyTable()
    # 如果为trade_time为index转换为日期类型，其它不用管。
    if index == "trade_time":
        df = df.set_index(index)
        df.index = pd.DatetimeIndex(df.index)
    # df.reset_index(level=None, drop=True, inplace=True, col_level=0, col_fill='')
    df = df.reset_index(drop=True)
    tb.add_column(index, df.index)  #按date排序
    for col in df.columns.values:  #df.columns.values的意思是获取列的名称
        # print('col',col)
        # print('df[col]',df[col])
        tb.add_column(col, df[col])
    #print(tb)
    return tb


def initialize_api(server_ip, debug=False):
    global api_dict  # 声明api_dict是全局变量

    if server_ip not in api_dict.keys():
        api = TdxHq_API(multithread=False, heartbeat=False, auto_retry=True)
        api.connect(server_ip, 7709)
        if len(api_dict) == 0:
            df_tdx = api.to_df(api.get_security_bars(1, 0, "000001", 0, 20))
            print(df_tdx)
        if debug: print("serverip=", server_ip, "api=", api)
        api_dict[server_ip] = api
        return api
    else:
        if debug: print(" api_dict[server_ip] is already in api_dict")
        return api_dict[server_ip]


def mk_api_list(svlist, debug=False):
    if sys.stdout.isatty():
        cy_funs = tqdm
    else:

        def cy_funs(x):
            return x

    api_list = []
    if debug:
        print("函数名：" + sys._getframe().f_code.co_name)
    for i in cy_funs(range(len(svlist))):
        try:
            serverip, tdxport = svlist[i], 7709
            if debug:
                print("mk_api_list: try to con to " + serverip)
            exec("api" + str(i) + " = TdxHq_API(multithread=False,heartbeat=False,auto_retry=True)")
            exec("api" + str(i) + ".connect(serverip, tdxport)")
            api_list.append(eval("api" + str(i)))
        except Exception as e:
            # sql = "UPDATE stock_tdx_servers SET error_times = error_times + 1 WHERE ip = '"+serverip+"'"
            # conn.execute(text(sql))
            global error_server_list
            error_server_list.append(serverip)
            print("mk_api_list error" + str(e))
    print("mkapi: All done")
    return api_list


def perfact_new_fast_server_list(cache_file=".", interval=1, nextfuntion=None, timeout=0.6, debug=False):
    """
    检查文件是否很新鲜，如果是，则不需要重新下载

    Returns:
        _type_: _description_
    """
    home_dir = os.path.dirname(os.path.abspath(__file__))
    cache_file = home_dir + "/faster_tdxserver_cache.ini"

    if os.path.isfile(cache_file):
        if debug: print("cache_file exists")
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=interval)
        mod_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        if mod_time >= one_hour_ago and mod_time <= now:
            if debug: print("cache_file is fresh, just read it")
            with open(cache_file, "r", encoding='utf-8') as f:
                fater_server_list = f.readlines()
                if debug: print("fater_server_list=", fater_server_list)
                fater_server_list = [item.strip() for item in fater_server_list]
                if debug: print("fater_server_list=", fater_server_list)
                return fater_server_list

    if debug: print("no file or not so fresh, download new")
    server_list = nextfuntion()
    if len(server_list) < 10:
        if debug: print("spare plane : server list is too short, try to get more")
        from pytdx.config.hosts import hq_hosts
        server_list = [host[1] for host in hq_hosts]
    fater_server_list = get_fast_tdx_server_ip_list(server_list, timeout)
    with open(cache_file, "w", encoding="utf-8") as f:
        f.writelines('%s\n' % item for item in fater_server_list)
    return fater_server_list


def get_cg_dict(api, stkcode: str, 要下载的K线数量=800, debug=False) -> pd.DataFrame:
    """
    通达信下载原始分钟K线(tdxserverip:str, 股票数字代码:str, 开始日期:str, 结束日期, debug=False)
    """
    市场代码 = int(stkcode[0].find('6')) + 1
    print(f"market={市场代码}, code={stkcode}")
    tdxserverip = "120.79.210.76"
    #api.connect(tdxserverip,7709)
    df = api.to_df(api.get_security_bars(1, 市场代码, stkcode, 0, 要下载的K线数量))
    tb = df_table(df, "datetime")
    #print(tb)
    # 将 "datetime" 列转换为日期时间类型
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['day'] = df['datetime'].dt.date
    # 提取小时和分钟
    df['time'] = df['datetime'].dt.time
    time_obj = datetime.strptime("10:00", "%H:%M").time()
    # 选取满足条件的记录
    selected_data = df[(df['time'] <= time_obj)]
    #print(selected_data)
    # 按日期分组，并计算每天最大高点值
    max_high_per_day = selected_data.groupby('day')['high'].max()
    #print(type(max_high_per_day))
    #max_high_per_day.rename(columns={'high': 'cg'}, inplace=True)
    # 将结果转换为字典形式
    result_dict = max_high_per_day.to_dict()
    # for key in result_dict.keys():
    #     print(f"Key: {key}, Type: {type(key)}")
    return max_high_per_day, result_dict


def newwmdf(api, code, daykline_n):
    cg_df, cg_dict = get_cg_dict(api, code, daykline_n * 16)
    market = int(code.startswith("6"))
    df = api.to_df(api.get_security_bars(9, market, code, 0, 50))
    df['day'] = pd.to_datetime(df['datetime']).dt.date
    result = df.merge(cg_df, on='day', how='left')
    result = result.rename(columns={'high_y': 'cg'})
    return result


def 测试15(api, stkcode: str, 要下载的K线数量=800, debug=False) -> pd.DataFrame:
    """
    通达信下载原始分钟K线(tdxserverip:str, 股票数字代码:str, 开始日期:str, 结束日期, debug=False)
    """
    市场代码 = int(stkcode[0].find('6')) + 1
    #print(f"market={市场代码}, code={stkcode}")
    tdxserverip = "120.79.210.76"
    #api.connect(tdxserverip,7709)
    df_tdx_15min = api.to_df(api.get_security_bars(1, 市场代码, stkcode, 0, 要下载的K线数量))
    tb = df_table(df_tdx_15min, "datetime")
    print(tb)
    wmdf = 原始15分钟df格式化(df_tdx_15min)
    return wmdf


def get_ltz(api, code,debug=False):
    result = api.get_company_info_category(0, code)
    if debug: print("result=", result)
    for item in result:
        if item.get('name') == '股本结构':
            if debug: print(item)
            file_name = item.get('filename')
            start = item.get('start')
            length = item.get('length')

            if debug: print("file_name=", file_name)

    import re

    def extract_number(t):
        number = re.findall(r'\d+\.?\d*', t)
        number = float(number[0])
        number_billion = number / 10000 if "万" in t else number
        return number_billion

    result = api.get_company_info_content(0, code, file_name, start, length)
    gb = result.split("\n")
    lt = gb[14]

    lt = [word.strip() for word in lt.split("｜") if len(word) > 1]
    #print("lt=", lt)#lt= ['流通A股', '6621.9087万', '6094.3979万', '-', '-', '-', '-']
    ltz = lt[1]
    ltz_number_billion = extract_number(ltz)
    if debug: print("ltz_number_billion=", ltz_number_billion)  #ltz= 0.66219087
    #print("result=", result[5].split('|')[2])
    return ltz_number_billion

if __name__ == "__main__":
    #错在昨天，cg应该大于5，价格为11.59，cg实际为2.74
    tdxserverip = "120.79.210.76"
    #df = 通达信下载原始分钟K线by_ip(tdxserverip, "300313")
    print("-" * 80)
    api = TdxHq_API()
    api.connect(tdxserverip, 7709)
    print(api.to_df(api.get_security_bars(9, 1, "880863", 0, 800)))
    exit()

    df2 = wmdf15(api, "880863", 60)
    print("df", df2)
    exit()
    df22 = df_table(df2, "datetime")
    print(df22)
    wmdf = 原始分钟df格式化(df2)
    print(wmdf)
    df3 = df_table(wmdf, "day")

    print(df3)
    exit()
    from pytdx.hq import TdxHq_API
    api = TdxHq_API()
    api.connect('221.237.182.7', 7709)

    data = api.get_k_data('000001', '19900101', '20211231')

    print(data)
    exit()
