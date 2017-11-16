# -*- coding: UTF-8 -*-
"""Simple FunkLoad test


$Id$
"""
import json
import requests
import time

url = "http://192.168.202.24:9091/begin/aes"

dataSecretkey = "UocOo3tWNrc2p28PXgf1ow=="
AESdata = "EjXgadzhqG4svlkigAwwF/tVtGGChFpxhjvLr7uyM6dt2jLqxOjqZFhbX2+O6zKo0Ba7eLy7dPbAuT2Fml5JSZgbn4/FqawfutG2r2nLKu1G9gdptjsnQYxxX+LM86nFeqLurKUaSYrkBrllHcOXXMGMEg8fNndtL9hR/ZlK7yebv/7p4BZotYSU+9DTuoEEzA+7cEBf0R59GrUK3hJnr5y0IAh4c7W2LjlOyOh95/JimTkd1vK3ONXAWI5btwOxSzYXW9iuxvauqiMZhcoJxERRntF34W45Q9z6ZaPgbIEgRa25OPAeL14Sibv55HHPjIc8mn2RZ+GVSiegG1zcWbiuflD9HUx09Wv6OPFPUv3FE2+eE5DkYzjm1DPW6b3QGno+b6e/bV/KortH3++1EOdd99erdMdQMKNB/KjbvTxxwNEsdwxdQ3f2xbmTCNSART0jYLdKOiiaW8aHlNz6zx3EyHJeyPwAXMSoYwAzAcbk+fQhvNJU4X3SQos9BHFME4pPyhoQViTSElQXE1dyHtAYkXsjZ+anSFjStfLL8v6Qv/iXY13uBIHTJcJZwpnFsSVsYQ+66f08VM0vmHXhEKb/Vk+1jpuwqsG3CfH8YP0="

payload = {'dataSecretkey':dataSecretkey,'AESdata':AESdata}

d = {'dataSecretkey':dataSecretkey,'AESdata':AESdata}
#payload = "dataSecretkey=UocOo3tWNrc2p28PXgf1ow%3D%3D&AESdata=EjXgadzhqG4svlkigAwwF%2FtVtGGChFpxhjvLr7uyM6dt2jLqxOjqZFhbX2%2BO6zKo0Ba7eLy7dPbAuT2Fml5JSZgbn4%2FFqawfutG2r2nLKu1G9gdptjsnQYxxX%2BLM86nFeqLurKUaSYrkBrllHcOXXMGMEg8fNndtL9hR%2FZlK7yebv%2F7p4BZotYSU%2B9DTuoEEzA%2B7cEBf0R59GrUK3hJnr5y0IAh4c7W2LjlOyOh95%2FJimTkd1vK3ONXAWI5btwOxSzYXW9iuxvauqiMZhcoJxERRntF34W45Q9z6ZaPgbIEgRa25OPAeL14Sibv55HHPjIc8mn2RZ%2BGVSiegG1zcWbiuflD9HUx09Wv6OPFPUv3FE2%2BeE5DkYzjm1DPW6b3QGno%2Bb6e%2FbV%2FKortH3%2B%2B1EOdd99erdMdQMKNB%2FKjbvTxxwNEsdwxdQ3f2xbmTCNSART0jYLdKOiiaW8aHlNz6zx3EyHJeyPwAXMSoYwAzAcbk%2BfQhvNJU4X3SQos9BHFME4pPyhoQViTSElQXE1dyHtAYkXsjZ%2BanSFjStfLL8v6Qv%2FiXY13uBIHTJcJZwpnFsSVsYQ%2B66f08VM0vmHXhEKb%2FVk%2B1jpuwqsG3CfH8YP0%3D"
headers = {
    'content-type': "application/x-www-form-urlencoded"
    }
print json.dumps(payload)
response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
#response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
