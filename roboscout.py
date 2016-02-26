import csv
import copy

def getData():
  data = []
  with open('scoreboard.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      if row['Red 1'] != '':
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

def teamToAlliancePartners(teams):
  """
    Take teams/matches and return a list of alliance partners
  """
  allies = {}
  for team, matches in teams.iteritems():
    allies[team] = []
    for match in matches:
      num = int(match['position'][-1])
      teammate = match['team'] + ' ' + str(num%2 +1)
      allies[team].append(match[teammate])
  return allies

def teamToAllianceAverage(teams):
  """
    Take a teams/matches and return their average score.
  """
  avgs = {}
  for team, matches in teams.iteritems():
    scores = [float(r[r['team']+' Score']) for r in matches]
    avgs[team] = avg(scores)
  return avgs

def teamToPartnerAverages(allies, averages):
  """ Take Alliance partners, and team averages, and return teams as keys and
      a list of partner averages as the value
  """
  avgs = {}
  for team, allies in allies.iteritems():
    avgs[team] = []
    for tm in allies:
      avgs[team].append(averages[tm])
  return avgs

def teamToMod(tavg, pavg):
  mod = {}
  for team, averg in tavg.iteritems():
    mod[team] = round(tavg[team] - avg(pavg[team]), 3)
  return mod

def teamToEO(tavg, mod):
  expo = {}
  for team in tavg.keys():
    expo[team] = (tavg[team] + mod[team])/2
  return expo

def teamToOPAR(expo):
  avexpo = avg(expo.values())
  opar = {}
  for team, eo in expo.iteritems():
    opar[team] = round(eo / avexpo, 1)
  return opar
def avg(l):
  s = 0.0
  for o in l:
    s = s + o
  return s / len(l)

if __name__ == '__main__':
  tm = teamToMatch(getData())
  ta = teamToAllianceAverage(tm)
  tp = teamToAlliancePartners(tm)
  tpa = teamToPartnerAverages(tp, ta)
  mod = teamToMod(ta, tpa)
  expo = teamToEO(ta, mod)
  opar = teamToOPAR(expo)
  print opar['6081']
  # for match in tm['8391']:
  #   print match
  # print tp['6081']
  # avg(tpa['6081'])
