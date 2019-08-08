#!/usr/bin/env python
import plotly.plotly as py
import plotly.graph_objs as go

def plotSingleBar(key_val_dict):

  values = key_val_dict['values']
  param = key_val_dict['name']
  cid = key_val_dict['id']

  x = [i for i in values.keys()]
  x.sort()

  y = [float(values[i]) for i in x]

  data = [ go.Bar(x=x, y=y) ]
  name = param + "(" + cid  + ")"
  print name
  py.iplot(data, filename = name)


