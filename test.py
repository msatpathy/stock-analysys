#!/usr/bin/env python
import annual as core

c = core.getKeyList('IOC')
for y in c['years']:
      print y + ' : ' + core.filterData('IOC',  'Return on Networth/Equity (%)', y)

d = core.filterDataSet('IOC', 'Return on Networth/Equity (%)')
print d
