# -*- coding:utf-8 -*- 

import requests
from bs4 import BeautifulSoup
import re
import os
import time
import sys

req_header={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

req_url_base='http://www.wandaxs.com/wanda.asp?id='

def get_text(tid):
  res=requests.get(req_url_base+str(tid),params=req_header)
  res.encoding = 'gb2312'
  soup=BeautifulSoup(res.text,"html.parser")
  
  title=soup.select('.lookmc strong')[0].text
  print(title)
  filename=title+'.txt'
  filename_down=title+'.txt.download'

  fo=open(filename_down, "wb+")
  fo.write((title+"\r\n").encode('UTF-8'))
  fo.write(("******************\r\n").encode('UTF-8'))

  sections={}
  links=soup.select('.mread')[0].findAll('a', limit=500)
  for link in links:
    match_obj=re.match(r'第(.+)章', link.text, re.M|re.I)
    if match_obj:
      sid = link['href'].split('=')[1]
      sections[sid]=(link.text, link['href'])

  sortedIds = sorted(sections.keys())
  for sid in sortedIds:
    (sec_title, sec_url)=sections[sid]
    print(sec_title)
    print(sec_url)

    res=requests.get(sec_url,params=req_header)
    res.encoding = 'gb2312'
    soup=BeautifulSoup(res.text,"html.parser")

    sec_txt=soup.findAll('table')[3].findAll('tr')[2].findAll('td')[0].text
    sec_txt=re.sub( '\s+', '\r\n\t', sec_txt).strip('\r\n')

    fo.write(('\r\n'+sec_title+'\r\n').encode('UTF-8'))
    fo.write(('\r\n'+sec_txt+'\r\n').encode('UTF-8'))

    time.sleep(1)
 
  fo.close()
  if os.path.exists(filename):
    os.remove(filename)
  os.rename(filename_down, filename)

    
if __name__ == "__main__":
  get_text(47512)

  
  
