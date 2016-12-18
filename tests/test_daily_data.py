import pykiwoom

df1 = pykiwoom.get_daily_data('000660', start='20161205', end='20161216')
df2 = pykiwoom.get_daily_data('000660', end='20161216', req_count=20)

print(df1)
print(df2)


