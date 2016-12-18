# pykiwoom
Python module for Kiwoom Open API+

# usages

```python
import pykiwoom
df1 = pykiwoom.get_daily_data("000660", end="20161218", req_count=20)
df2 = pykiwoom.get_daily_data("000660", start="20161201", end="20161218")

print(df1.head())
print(df2.head())
```
