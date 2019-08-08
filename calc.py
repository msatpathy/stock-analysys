#!/usr/bin/env python
import os,sys
import functools

DATA_DIR = "DataLib/"

f_in = sys.argv[1]
f_out = DATA_DIR + f_in + '.data'

''' pass x & y axes as dictionaries, e.g {'years':[2001,2002,2003]}'''
def csv_linechart(x_axis, y_axis, csv = ''):
   x  = []
   y = []
   if csv == '':
     csv = DATA_DIR + f_in + '.csv'
   with open(csv,"a+") as f:
      x.append(x_axis.keys()[0])
      x.extend(x_axis.values()[0])
      y.append(y_axis.keys()[0])
      y.extend(y_axis.values()[0])
      f.write(' '.join(x))
      f.write('\n')
      f.write(' '.join(y))


'''Filter required columns from raw data '''
os.system("$(pwd)/process.sh %s > %s" % (f_in, f_out))
all_items = []
yearly_pay =  [[-1, 0.0]]
years = []
pays = []
''' Organise data from file into list year:dividend % '''
with open(f_out) as datafile:
   lines = datafile.readlines()
   for line in lines:
     x,y = line.split()
     all_items.append([int(x),float(y)])
     all_items.sort()

''' Consolidate multiple dividend payouts during same year into single yearly payout '''
for item in all_items:
  if item[0] != yearly_pay[-1][0]:
     yearly_pay.append(item)
  else:
     yearly_pay[-1][1] += item[1]

''' incremental chronological order '''
yearly_pay = yearly_pay[1:-1]

''' check discontinuation '''
discont = []
for i in range(0,len(yearly_pay)-1):
  if yearly_pay[i][1] == 0:
    discont.append(yearly_pay[i][0])
    

  if i == 0:
    continue
  else:
     if (yearly_pay[i][0] - yearly_pay[i-1][0] != 1 ):
        diff = yearly_pay[i][0] - yearly_pay[i-1][0]
        for j in range(1,diff):
           print yearly_pay[i-1][0] 
           print j
           discont.append(yearly_pay[i-1][0] + j)
  


''' List year to year growth in payout '''
growth_pattern = []
last = 0.0
cut_count = 0
for item in yearly_pay:
  growth_pattern.append(item[1] - last)
  ''' Count cut in div payout '''
  if item[1] < last:
    cut_count += 1

  last = item[1]

''' Calculate CAGR growth rate at different intervals '''
CAGR_ALL = ((float(yearly_pay[-1][1]/yearly_pay[0][1])) ** (1/float(len(yearly_pay))) - 1 ) * 100
CAGR_10 = ((float(yearly_pay[-1][1]/yearly_pay[-11][1])) ** (1/float(10)) - 1 ) * 100
CAGR_5 = ((float(yearly_pay[-1][1]/yearly_pay[-6][1])) ** (1/float(5)) - 1 ) * 100
CAGR_3 = ((float(yearly_pay[-1][1]/yearly_pay[-4][1])) ** (1/float(3)) - 1 ) * 100
CAGR_3S = []
CAGR_5S = []
CAGR_10S = []
''' CAGRs at multiple windows of 3/5/10 years ''' 
for i in range(0,len(yearly_pay)-3):
  if yearly_pay[-i-4][1] != 0:
    CAGR = ((float(yearly_pay[-i-1][1]/yearly_pay[-i-4][1])) ** (1/float(3)) - 1 ) * 100
    CAGR_3S.append(CAGR)

CAGR_5S = []
for i in range(0,len(yearly_pay)-5):
  if yearly_pay[-i-6][1] != 0:
    CAGR = ((float(yearly_pay[-i-1][1]/yearly_pay[-i-6][1])) ** (1/float(5)) - 1 ) * 100
    CAGR_5S.append(CAGR)

for i in range(0,len(yearly_pay)-10):
  if yearly_pay[-i-11][1] != 0:
    CAGR = ((float(yearly_pay[-i-1][1]/yearly_pay[-i-11][1])) ** (1/float(10)) - 1 ) * 100
    CAGR_10S.append(CAGR)

if len(sys.argv) >= 3 :
  opts = sys.argv[2:]
else:
  opts = '--summary'

if '--all' in opts:

  print "Yearly pay %:"
  print yearly_pay
  print ""
  print "Growth pattern in %:" 
  print growth_pattern
  average_growth = functools.reduce(lambda x,y:x+y,growth_pattern)/len(growth_pattern)
  print ""
  print "average growth %:" 
  print average_growth
  print ""
  print "Number of times growth was cut:"
  print str(cut_count) + '/' + str(len(growth_pattern))
  print ""
  print "Discontinued:"
  print "Total:" + str(len(discont))
  print discont
  print ""
  print "CAGR for :" + str(len(yearly_pay)) + " Years"
  print CAGR_ALL
  print ""
  print "CAGR for 10 YRS:"
  print CAGR_10
  print "CAGR accross all 10 year windows:"
  print CAGR_10S[-1:0:-1]
  print ""
  print "CAGR for 5 YRS:"
  print CAGR_5
  print "CAGR accross all 5 year windows:"
  print CAGR_5S[-1:0:-1]
  print ""
  print "CAGR for 3 YRS:"
  print CAGR_3
  print "CAGR accross all 3 year windows:"
  print CAGR_3S[-1:0:-1]
  
else:

  average_growth = functools.reduce(lambda x,y:x+y,growth_pattern)/len(growth_pattern)
  print ""
  print "average growth %:"
  print average_growth
  print ""
  print "Number of times growth was cut:"
  print str(cut_count) + '/' + str(len(growth_pattern))
  print ""
  print "Discontinued:"
  print "Total:" + str(len(discont))
  print discont
  print ""
  print "CAGR for :" + str(len(yearly_pay)) + " Years"
  print CAGR_ALL
  print ""
  print "CAGR for 10 YRS:"
  print CAGR_10
  print ""
  print "CAGR for 5 YRS:"
  print CAGR_5
  print ""
  print "CAGR for 3 YRS:"
  print CAGR_3

if '--dump' in opts:
  csv_linechart({'years' : [str(i[0] + 2000) for i in yearly_pay]},{'Div%' : [str(i[1]) for i in yearly_pay] }) 



