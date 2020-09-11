import os
import logging
import requests
from lxml import etree
import json
import hmac
import hashlib
import base64
import urllib
import pandas as pd
from datetime import datetime, timedelta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58',
}

class BaseControl:
    
    @classmethod
    def send_requests(cls, url, method="GET", headers=headers):
        try:
            resp = requests.request(method, url, headers=headers, timeout=8)
        except Exception as e:
            resp = requests.Response()
            resp.status_code = 400
            resp.json = {"err_msg": str(e)}
        return resp

    @classmethod
    def parse_html(cls, html, reg_exp):
        text = etree.HTML(html)
        return text.xpath(reg_exp)

    @classmethod
    def unpack_row(cls, row, sp_treat={}):
        elts = row.xpath(f'.//td')
        resp = []
        for idx, val in enumerate(elts):
            treat = sp_treat.get(idx, "")
            if treat:
                val = ''.join(val.xpath(treat))
            else:
                val = val.text
            resp.append(val)
        return resp

    @classmethod
    def get_webtable(cls, url, encoding="utf-8"):
        return pd.read_html(url, encoding=encoding)

    @classmethod
    def DataFrame(cls, matrix, columns=None):
        return pd.DataFrame(matrix, columns=columns)