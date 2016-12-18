from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from datetime import datetime

TR_REQ_TIME_INTERVAL = 0.2

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        self.login_event_loop.exit()

    def get_code_list_by_market(self, market):
        func = 'GetCodeListByMarket("%s")' % market
        ret = self.dynamicCall(func)
        code_list = ret.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        func = 'GetMasterCodeName("%s")' % code
        code_name = self.dynamicCall(func)
        return code_name

    def _set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code, real_type, field_name, index, item_name)
        return ret.strip()

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        # check remained data
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        # get data according to tr
        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)

        # exit event loop for tr
        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            date    = self._comm_get_data(trcode, "", rqname, i, "일자")
            open    = self._comm_get_data(trcode, "", rqname, i, "시가")
            high    = self._comm_get_data(trcode, "", rqname, i, "고가")
            low     = self._comm_get_data(trcode, "", rqname, i, "저가")
            close   = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume  = self._comm_get_data(trcode, "", rqname, i, "거래량")

            self.ohlcv['date'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))
            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))

            self.ohlcv_count += 1

            # check requested data count
            if self.ohlcv_req_count is not None and self.ohlcv_count >= self.ohlcv_req_count:
                self.remained_data = False
                break

            dt = datetime.strptime(date, "%Y%m%d")
            delta = dt - self.ohlcv_start

            if delta.days <= 0:
                self.remained_data = False
                break