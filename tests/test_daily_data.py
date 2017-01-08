from pykiwoom.kiwoom import *
from pykiwoom.wrapper import *

kiwoom = Kiwoom()
kiwoom.comm_connect()

wrapper = KiwoomWrapper(kiwoom)
df = wrapper.get_daily_data('000660', start='20161201', end='20161210')
pbr = wrapper.get_pbr('000660')
per = wrapper.get_per('000660')
print(pbr, per)

print("test mo")
