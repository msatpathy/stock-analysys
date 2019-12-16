#!/usr/bin/env python
#usage ./webscrap --name (userfriendly name or code) 

import sys
from urllib import urlopen
from bs4 import BeautifulSoup
from urlstore import urldata
import copy

DATA_DIR = "Datalib/"

def get_dividend_history(name):
    div_records = []
    keys = ['announce', 'effective', 'type', 'percentage', 'remarks']
    values = []
    for item in urldata:
        for n in item['name']:
          if n == name:
            url = item['history']
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


def collect_ratios(name):
   #import pdb
   #pdb.set_trace()
   years = []
   ratio = {}
   report = {}
   #max_count = 0
   data_index = 0
   ratio_key = ""
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

   return report

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


def fetch_record(name):
    hist_record = get_dividend_history(name)
    cons_rec = calculate_annual_dividend(hist_record)
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

      



def main():
  name = ''  
  if len(sys.argv) > 1:
     if '--name' in sys.argv:
        index = sys.argv.index('--name')
        name = sys.argv[ index + 1 ]

  if name != '':
     dividend = fetch_record(name.lower())
     print dividend
     dump_dividend_history(dividend, name.lower())

     report = collect_ratios(name.lower())
     print_annual_ratios(report)

if __name__ == "__main__" :
  main()
  
