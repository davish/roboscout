"""
futil.py

Contains utilities for dealing with dictionaries in a functional manner.
"""

def avg(l):
  """
  Average of elements of a list.
  """
  s = 0.0
  for o in l:
    s = s + o
  return float('NaN') if len(l) == 0 else round(s / len(l),5)

def mapd(f, d):
  """
    Analog of of map() for dictionaries. Applies a function to each value
    and associates it with the same key as the original dict
  """
  r = {}
  for k, v in d.iteritems():
    r[k] = f(v)
  return r

def include(f, l):
    """
    f is a function that returns a boolean.
    Filter elements of a list by whether f(e) returns true, where e is an
    element of the list.
    """
    r = []
    for e in l:
        if f(e):
            r.append(e)
    return r

def filter_dict(f, d):
    """
    f is a function that returns a boolean. If f(key) == True, then
    the key and value are inserted into the result dictionary.
    """
    r = {}
    for k, v in d.iteritems():
        if f(k):
            r[k] = v
    return r

def zipd(k, v):
  """
    Create a dictionary from two lists, one keys, one values.
  """
  return dict(zip(k, v))

def mapzip(f, l):
  """
    Similar to mapd, but f is passed the key as a part of list l
    instead of a dictionary value
  """
  return zipd(l, map(f, l))
