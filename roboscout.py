# -*- coding: utf8 -*-

"""
roboscout.py

Functions for parsing matchlists and calculating statistics about individual teams.
"""
import csv
import copy
import numpy
from futil import *

def getData(csv_file='scoreboard.csv', empty=False):
  """Parse matchlist from CSV file."""
  data = []
  with open(csv_file, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      # If a row is not empty (or if we want to include empty rows)
      if empty or row['Red Score'] != '':
        data.append(row)
  return data

def teamToMatch(data):
  """Take matchlist, return dict of teams as keys and a list of their matches as values"""
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
  """Return dict associating teams with their match scores."""
  ms = {}
  for team, matches in teams.iteritems():
    ms[team] = [float(r[r['team']+' Score']) for r in matches]
  return ms

def get_partners(matches):
  """Return list of match partners given a matchlist."""
  r = []
  for match in matches:
    num = int(match['position'][-1]) # Find our team number.
    # Our teammate's number will be associated with Red2 if we are Red1 and
    # vice versa.
    teammate = match['team'] + ' ' + str(num%2 +1)
    r.append(match[teammate])
  return r

def display(opar, oar):
  """Display statistics for debugging."""
  import operator
  rank = sorted(opar.items(), key=operator.itemgetter(1))
  rank.reverse()

  for team, r in rank:
    s= team + " opar:" + str(opar[team]) + " oar:" + str(oar[team])
    print s


def scout(d, m=None, tm=None):
  """
  Pull individual robot performance out of a matchlist where scores are shown for two-on-two matches.

  Basic assumption: If a robot’s average in all of its matches is higher than the averages of its alliance partners,
  then its likely that that robot contributed more points to the final match score than its partner.
  """
  if m is None:
    m = teamToMatch(d)
  if tm is None:
    tm = teamToMatchScores(m)

  teams = tm.keys()
  tp = mapd(get_partners, m)
  ta = mapd(lambda a: avg(a), tm) # average of all the team's matches
  # the average of each team's alliance partners' averages
  # map(ta.get, tms) gets each alliance partner's average
  tpa = mapd(lambda tms: avg(map(ta.get, tms)), tp)

  # Difference between a team's average and their alliance partner's
  mod = mapzip(lambda t: round(ta[t]-tpa[t],3), teams)
  # Expected output per round of the team given their average and modifier
  # The team average is divided by two since it is assumed that the "baseline"
  # is that teams are scoring equally before adding their modifiers.
  expo = mapzip(lambda t: round(ta[t]/2+mod[t]), teams)
  avgexpo = avg(expo.values())

  # "OPAR" describes how much a team's expected
  # output is  above or below the average. OPAR of 1.0 is an average team.
  opar = mapd(lambda x: 0, expo) if avgexpo==0 else mapd(lambda o: round(o/avgexpo,1), expo)

  # standard deviation of each round's expected individual output
  # based on the individual round score and the team's modifier
  stdev = mapzip(lambda t: round(numpy.std(
    map(lambda match: round(match/2+mod[t], 3),tm[t])), 1), teams)
  # Percent deviation, taking the standard deviation divided by the
  # expected output
  pdev = mapzip(lambda t: round(div(stdev[t], expo[t]), 3), teams)
  # Percent deviation times OPAR gives the possible variance in OPAR
  # from round-to-round
  oar = mapzip(lambda t: round(opar[t] * pdev[t], 1), teams)

  return {
    'm': m,
    'tp': tp,
    'tm': tm,
    'ta': ta,
    'expo': expo,
    'opar': opar,
    'variance': stdev,
    'oar': oar,
    # 'avg': avgexpo
  }

if __name__ == '__main__':
  pass
