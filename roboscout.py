import csv
import copy
import numpy

def avg(l):
  s = 0.0
  for o in l:
    s = s + o
  return s / len(l)

def getData():
  data = []
  with open('scoreboard.csv', 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      if row['Red Score'] != '':
        data.append(row)
  return data

def teamToMatch(data):
  teams = {}
  teamNames = ['Red 1', 'Red 2', 'Blue 1', 'Blue 2']
  for row in data:
    for n in teamNames:
      if row[n] not in teams:
        teams[row[n]] = []
      r = copy.copy(row)
      if n.find('Red') == 0:
        r['team'] = 'Red'
      else:
        r['team'] = 'Blue'
      r['position'] = n
      teams[row[n]].append(r)
  return teams

def teamToMatchScores(teams):
  ms = {}
  for team, matches in teams.iteritems():
    ms[team] = [float(r[r['team']+' Score']) for r in matches]
  return ms

def get_partners(matches):
  r = []
  for match in matches:
    num = int(match['position'][-1])
    teammate = match['team'] + ' ' + str(num%2 +1)
    r.append(match[teammate])
  return r

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
  return dict(zip(k, v))

def mapzip(f, l):
  return zipd(l, map(f, l))

if __name__ == '__main__':
  m = teamToMatch(getData())
  teams = m.keys()

  tm = teamToMatchScores(m)
  tp = mapd(get_partners, m)
  ta = mapd(lambda a: avg(a), tm)
  tpa = mapd(lambda tms: avg(map(ta.get, tms)), tp)
 
  mod = mapzip(lambda t: round(ta[t]-tpa[t],3), teams)
  expo = mapzip(lambda t: round((ta[t]+mod[t])/2,3), teams)
  
  avgexpo = avg(expo.values())
  opar = mapd(lambda o: round(o/avgexpo,1), expo)
  
  stdev = mapzip(lambda t: numpy.std(
    map(lambda match: round((match + mod[t])/2, 3),tm[t])), teams)

  pdev = mapzip(lambda t: round(stdev[t] / expo[t], 3), teams)
  oar = mapzip(lambda t: round(opar[t] * pdev[t], 1), teams)


  import operator
  rank = sorted(opar.items(), key=operator.itemgetter(1))
  rank.reverse()

  for team, r in rank:
    print team + " opar:" + str(opar[team]) + " oar:" + str(oar[team])
