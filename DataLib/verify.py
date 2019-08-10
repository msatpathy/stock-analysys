#!/usr/bin/env python
'''This script can be used to verify difference between 
actual annual report, copy pasted from webpage vs recovered annual report 
via webspcrap.py and printed to console using print_annual_ratios() funstion call
ex. ./verify.py source.txt dest.txt
'''


import sys
import re

ls = []
ld = []

source_file = sys.argv[1]
dest_file = sys.argv[2]

with open(source_file) as fs:
  ls = fs.readlines()
  ls = [re.sub("\s+", " ", l) for l in ls]
  ls.sort()

with open(dest_file) as fd:
  ld = fd.readlines()
  ld = [re.sub("\s+", " ", l) for l in ld]
  ld.sort()

l = len(ls)
for i in range(0,l):
    if str(ls[i]) != str(ld[i]):
        print "\n"
        print "+[%s: Line %d]: "    % ( source_file, i) + ls[i]
        print "-[%s: Line %d]: "  % ( dest_file, i)   + ld[i]
print "\n"
    

  
