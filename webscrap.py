#!/usr/bin/env python
#usage ./webscrap --name (userfriendly name or code) 

import sys,os
from urllib import urlopen
from bs4 import BeautifulSoup
from urlstore import urldata
import copy
import pickle
from datetime import datetime

DATA_DIR = "DataLib/"
'''Fetch div data from the web(moneycontrol)'''
def get_dividend_history(name):
    div_records = []
    keys = ['announce', 'effective', 'type', 'percentage', 'remarks']
    values = []
    for item in urldata:
        for n in item['name']:
          if n == name:
            url = item['div_history']
            break
        if url != "":
           break


    if url != '':
        html = urlopen(url)
    else:
        print "url not found(dividend)!!!"
        sys.exit()
    
    bs = BeautifulSoup(html.read(), features="html.parser")
    for f in  bs.find("table", {'class':"mctable1"}).findChildren("td"):
        values.append(f.get_text())
        if len(values) == len(keys):
            d = dict(zip(keys,values))
            div_records.append(d)
            values = []
    return div_records

         
'''consolidate div data per year basis(one entry per year)'''
def calculate_annual_dividend(hist_records):
    cons = {}
    for r in hist_records:
      year = int(r['effective'].split('-')[-1])
      div_per = float(r['percentage']) 
      if year not in cons.keys():
          cons.update({year:div_per})
      else:
          cons[year] = cons[year] + div_per
    return cons

''' Collect financial ratios from moneycontrol and return it in dictionary format'''
def collect_ratios(name):
   #import pdb
   #pdb.set_trace()
   years = []
   ratio = {}
   #report = {}
   #max_count = 0
   data_index = 0
   ratio_key = ""

   report = Load_from_disk('RATIOS', name)
   if report != None:
      return report
   else:
      report = {}


   for item in urldata:
        for id in item['name']:
            if id == name:
              url = item['ratios']
              print url
              break
        if url != '':
          break

   if url != '':
      html = urlopen(url)
   else:
      print "url not found!!"
      sys.exit()
   bs = BeautifulSoup(html.read(), features = "html.parser")
   #count = 0; 
   for f in bs.find("table",{"class":"table4", "width":"744", "cellspacing":"0", "cellpadding":"0", "bgcolor":"#ffffff"}).find_next_sibling("table").findChildren("td", {"class": ["det", "detb"]}):
      data = f.get_text()
      if data.startswith('Mar ') and data[-2:].isnumeric():
         '''Capture year as column headers '''  
         years.append('20' + str(data.split()[-1]))

      elif data.lstrip('-').replace('.','').replace(',','').isdigit():
         '''Check if it's a numeric data, it has to be a value'''  
         ratio[ratio_key] = data.replace(',','')
         if not report.has_key(years[data_index]):
            report[years[data_index]] = {}
         report[years[data_index]].update(ratio)
         ratio = {}
         data_index += 1
     
      elif data == '' or data.endswith('Ratios'):
         '''ignore empty fields including sub-section headers''' 
         continue

      elif data == '-':
         '''unavailable data mentioned as - '''
         ratio[ratio_key] = (float(0))
         if not report.has_key(years[data_index]):
            report[years[data_index]] = {}
         report[years[data_index]].update(ratio)
         #print ratio
         #print report[years[data_index]]
         ratio = {}
         data_index += 1



      elif data[0].isalpha() and len(data) > 5:
         '''Capture field names''' 
         ratio_key = copy.deepcopy(str(data))
         data_index = 0

      else:
         continue
   save_to_disk('RATIOS', report, name)
   return report
'''print financial ratios to console'''
def print_annual_ratios(report):
    #import pdb
    #pdb.set_trace()
    years = report.keys()
    years.sort(reverse = True)
    years_p = [item.rjust(16,' ') for item in years ]
    years_str = "\t"*4 + "".join(years_p)
    print years_str
    for k in report[years[0]].keys():
        val = k + "\t"
        for y in years:
            val += str(report.get(y).get(k,'***')) + "\t\t"
        print val

'''Fetch div data and consolidate'''
def fetch_div_record(name):
    cons_rec = Load_from_disk('DIV', name)
    if cons_rec == None:
      hist_record = get_dividend_history(name)
      cons_rec = calculate_annual_dividend(hist_record)
      save_to_disk('DIV', cons_rec, name)
    return cons_rec

''' create dump of dividend data in a format that can be used for further processing '''
def dump_dividend_history(div_data, dump_name):
    f_name = DATA_DIR + dump_name + ".data"
    lines = ""
    with open(f_name, "w") as f:
      for key in div_data:
          lines = lines +  str(key)[2:] + '\t' + str(div_data[key]) + "\n"

      l = lines.split("\n")
      l.sort(reverse = True)
      lines_sorted =  "\n".join(l)
      print lines_sorted
      f.write(lines_sorted)

'''Fetch corporate actions history (splits, dividends, bonuses etc.)'''
def fetch_corp_actions(com_name):
    div_keys = ['announce', 'effective', 'type', 'percentage', 'remarks']
    div_values  = []
    for item in urldata:
      for n in item['name']:
        if n == name:
          url = item['div_history']
          break
        if url != "":
          break

    if url != '':
      html = urlopen(url)
    else:
      print "url not found(dividend)!!!"
      sys.exit()

    bs = BeautifulSoup(html.read(), features="html.parser")
    for f in  bs.find("table", {'class':"mctable1"}).findChildren("td"):
      values.append(f.get_text())

'''Save data to disk'''
''' TYPE = ('DIV', 'RATIOS', 'CALENDAR') '''
def save_to_disk(TYPE, data, c_name):
    cache = {}
    if TYPE not in  ('DIV', 'RATIOS', 'CALENDAR'):
      print "invalid TYPE, cannot cache!!"
      return False
  
    modified_on = datetime.now()
    f_name = DATA_DIR + c_name + ".cache"
    
    if os.path.exists(f_name):
      cache = pickle.load(open(f_name, "rb"))

    cache[TYPE] = (modified_on, data)
    pickle.dump(cache, open(f_name, "wb"))
    return True 

'''Load cached data from disk'''
''' TYPE = ('DIV', 'RATIOS', 'CALENDAR') '''
''' Returns none for data older than 300 seconds (5 minutes) '''
def Load_from_disk(TYPE, c_name):
    if TYPE not in  ('DIV', 'RATIOS', 'CALENDAR'):
      print "invalid TYPE, cannot cache!!"
      return None
  
    time_now = datetime.now()
    f_name = DATA_DIR + c_name + ".cache"

    if os.path.exists(f_name):
      cache = pickle.load(open(f_name, "rb"))
    else:
      return None

    if cache.has_key(TYPE):
      time_stamp = cache[TYPE][0]
    else:
      return None

    if (time_now - time_stamp).total_seconds() > 300:
       return None       

    return cache[TYPE][1]

def main():
  name = ''  
  if len(sys.argv) > 1:
     if '--name' in sys.argv:
        index = sys.argv.index('--name')
        name = sys.argv[ index + 1 ]

  if name != '':
     dividend = fetch_div_record(name.lower())
     print dividend
     dump_dividend_history(dividend, name.lower())

     report = collect_ratios(name.lower())
     print_annual_ratios(report)
     

if __name__ == "__main__" :
  main()
  
