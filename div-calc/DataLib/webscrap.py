#!/usr/bin/env python
#usage ./webscrap --name (userfriendly name or code) 

import sys
from urllib import urlopen
from bs4 import BeautifulSoup
from urlstore import urldata


def get_dividend_history(name):
    div_records = []
    keys = ['announce', 'effective', 'type', 'percentage', 'remarks']
    values = []
    for item in urldata:
        for name in item['name']:
            url = item['history']
            break
    if url != '':
        html = urlopen(url)
    
    bs = BeautifulSoup(html.read(), features="html.parser")
    for f in  bs.find("table", {'class':"tbldivid"}).findChildren("td"):
        values.append(f.get_text())
        if len(values) == len(keys):
            d = dict(zip(keys,values))
            div_records.append(d)
            values = []
    return div_records

         

def calculate_annual_dividend(hist_records):
    cons = {}
    for r in hist_records:
      year = int(r['effective'].split('-')[-1]) + 2000
      div_per = float(r['percentage']) 
      if year not in cons.keys():
          cons.update({year:div_per})
      else:
          cons[year] = cons[year] + div_per
    return cons


    


def fetch_record(name):
    hist_record = get_dividend_history(name)
    cons_rec = calculate_annual_dividend(hist_record)
    print cons_rec


def main():
  name = ''  
  if len(sys.argv) > 1:
     if '--name' in sys.argv:
        index = sys.argv.index('--name')
        name = sys.argv[ index + 1 ]

  if name != '':
     fetch_record(name.lower())
     




if __name__ == "__main__" :
  main()
  
