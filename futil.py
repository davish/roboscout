def avg(l):
  s = 0.0
  for o in l:
    s = s + o
  return float('NaN') if len(l) == 0 else round(s / len(l),5)

def mapd(f, d):
  """
    Variant of map() that applies a function to each value
    and associates it with the same key as the original dict
  """
  r = {}
  for k, v in d.iteritems():
    r[k] = f(v)
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