import sys
import time
import pandas as pd
from PyQt5.QtWidgets import *
from .kiwoom import *

def get_daily_data(code, start='20000101', end='20161218', req_count=None):
    # login
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
    kiwoom.ohlcv_count = 0
    kiwoom.ohlcv_start = datetime.strptime(start, "%Y%m%d")
    kiwoom.ohlcv_req_count = req_count

    kiwoom._set_input_value("종목코드", code)
    kiwoom._set_input_value("기준일자", end)
    kiwoom._set_input_value("수정주가구분", 1)
    kiwoom._comm_rq_data("opt10081_req", "opt10081", 0, "0101")

    while kiwoom.remained_data == True:
        time.sleep(TR_REQ_TIME_INTERVAL)

        kiwoom._set_input_value("종목코드", code)
        kiwoom._set_input_value("기준일자", end)
        kiwoom._set_input_value("수정주가구분", 1)
        kiwoom._comm_rq_data("opt10081_req", "opt10081", 2, "0101")

    df = pd.DataFrame(kiwoom.ohlcv, columns=['open', 'high', 'low', 'close', 'volume'], index=kiwoom.ohlcv['date'])
    return df

app = QApplication(sys.argv)

