#!/usr/bin/env python
# coding: utf-8

# In[136]:


from io import BytesIO
from urllib import request
import requests
import gzip

import json
from datetime import datetime, timedelta
import pandas as pd
import numpy


# In[137]:


today = datetime.today().strftime("%Y%m%d")
delta_datetime = timedelta(days=-365)
before_year = (datetime.today() + delta_datetime).strftime("%Y%m%d")

headers = {
    "Host": "marketdata.krx.co.kr",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "http://marketdata.krx.co.kr/mdi",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,ja;q=0.7,ru;q=0.6"
    }
path = f"http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?name=fileDown&filetype=csv&url=MKD/13/1302/13020302/mkd13020302_01&ind_tp=ALL&type=1&period_strt_dd={before_year}&period_end_dd={today}&etctype=ST&pagePath=%2Fcontents%2FMKD%2F13%2F1302%2F13020302%2FMKD13020302.jsp"

otp_req = request.Request(path, headers=headers)
otp_code = request.urlopen(otp_req).read().decode()
# print(otp_code)


# In[138]:


headers = {
    "Host": "file.krx.co.kr",
    "Origin": "http://marketdata.krx.co.kr",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer": "http://marketdata.krx.co.kr/mdi",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,ja;q=0.7,ru;q=0.6"
    }

req_url = 'http://file.krx.co.kr/download.jspx?code=' + otp_code
req = request.Request(req_url, headers=headers)  # 헤더(리퍼러) 추가
# byte_data = request.urlopen(req).read()
# df = pd.read_excel(BytesIO(byte_data))

byte_data = request.urlopen(req).read()

# with gzip.open(byte_data,'rb') as f:
#     print(f.readlines())

with open("개인일별추이.csv", "wb") as f:
    f.write(byte_data)

# with open(byte_data, 'rb') as csvfile:
#     df = pd.read_csv(csvfile, compression='gzip')
    
print("저장끝")
df = pd.read_csv("개인일별추이.csv")
print(df)


# In[ ]:


# from pykrx import stock

# df = stock.get_market_trading_value_by_date(before_year, today, "ALL")
# df = stock.get_market_trading_value_and_volume_by_ticker("20201224", market="ALL", investor="개인")
# print(df.head())
# print(df.columns)

# df = stock.get_market_trading_value_and_volume_by_ticker("20201224", market="ALL", investor="외국인")
# print(df.head())
# print(df.columns)

# df = stock.get_market_trading_volume_by_date("20200519", "20200526", "KOSPI")
# print(df.head())
# print(df.columns)


# In[ ]:




