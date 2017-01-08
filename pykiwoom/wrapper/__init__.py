import sys
import time
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)

class KiwoomWrapper:
    def __init__(self, kiwoom):
        self.kiwoom = kiwoom

    def get_daily_data(self, code, start='20000101', end='20161218', req_count=None):
        self.kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
        self.kiwoom.ohlcv_count = 0
        self.kiwoom.ohlcv_start = datetime.strptime(start, "%Y%m%d")
        self.kiwoom.ohlcv_req_count = req_count

        self.kiwoom._set_input_value("종목코드", code)
        self.kiwoom._set_input_value("기준일자", end)
        self.kiwoom._set_input_value("수정주가구분", 1)
        self.kiwoom._comm_rq_data("opt10081_req", "opt10081", 0, "0101")

        while self.kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)

            self.kiwoom._set_input_value("종목코드", code)
            self.kiwoom._set_input_value("기준일자", end)
            self.kiwoom._set_input_value("수정주가구분", 1)
            self.kiwoom._comm_rq_data("opt10081_req", "opt10081", 2, "0101")

        df = pd.DataFrame(self.kiwoom.ohlcv, columns=['open', 'high', 'low', 'close', 'volume'], index=self.kiwoom.ohlcv['date'])
        return df

    def get_pbr(self, code):
        self.kiwoom._set_input_value("종목코드", code)
        self.kiwoom._comm_rq_data("opt10001_req", "opt10001", 0, "0101")
        return self.kiwoom.pbr

    def get_per(self, code):
        self.kiwoom._set_input_value("종목코드", code)
        self.kiwoom._comm_rq_data("opt10001_req", "opt10001", 0, "0101")
        return self.kiwoom.per



