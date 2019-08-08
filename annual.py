#!/usr/bin/env python
import sys
years = []
keys = []
yearly_report = {}

'''convert csv format annual reports from external source to dictionaries'''
def processAnnualReports(filename):
  inputFile = "DataLib/"+ filename
  with open(inputFile) as f:
    years = f.readline().rstrip().split('|')
    years = [ i for i in years if i != '']
    
  for year in years:
    inx = years.index(year)
    keys = []
    vals = []
    with open(inputFile) as f:
      next(f)
      for line in f:
        l = line.rstrip().split('|')
        keys.append(l[0])
        vals.append(l[inx + 1])
      yearly_record = dict(zip(keys,vals))
    yearly_report[year] = yearly_record
  return yearly_report
            
#processAnnualReports(sys.argv[1])

'''Pick data from annual report for given year'''
def filterData(comp, keyString, year):
   filename = comp + "_annual"
   records = processAnnualReports(filename)
   return records[year][keyString]

'''Filter specific data from annual report for all years'''
def filterDataSet(comp, keyString):
   data_set = {}
   values = {}
   data_set['name'] = keyString
   data_set['id'] = comp
   filename = comp + "_annual"
   records = processAnnualReports(filename)
   for year in records.keys():
     values[year] = records[year][keyString]
   data_set['values'] = values
   return data_set

'''List of Keys'''
def getKeyList(comp):
   years = []
   keys = []
   allKeys = {}
   filename = comp + "_annual"
   records = processAnnualReports(filename)
   years = records.keys()
   for year in years:
      keys = records[year].keys()
      break;
   allKeys['years'] = sorted(years)
   allKeys['keys'] = sorted(keys)
   return allKeys 

'''Share comparision data for any field for two companies'''
#def getComparision(field, comp1, comp2):
      
