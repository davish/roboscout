import roboscout

HIGH_GOAL=7
LOW_GOAL=8
MID_GOAL=9
HANG=13

def best_robots(ts):
  ranks = {}
  oar = {}
  caps = {}
  for tourney, matches in ts.iteritems():
    s = roboscout.scout(matches)
    highcap = capabilities(s, HIGH_GOAL)
    midcap = capabilities(s, MID_GOAL)
    lowcap = capabilities(s, LOW_GOAL)
    hangcap = capabilities(s, HANG)
    for team, expo in s['expo'].iteritems():
      if team in ranks:
        if expo < ranks[team]:
          continue
      ranks[team] = expo
      oar[team] = s['variance'][team]
      caps[team] = {
      'high': highcap[team],
      'mid': midcap[team],
      'low': lowcap[team],
      'hang': hangcap[team]
      }
  return ranks, oar, caps

import futil


def capabilities(s, i):
  tc = futil.mapd(lambda matches: map(
      lambda m: m[m['team']+' Breakdown'][i], matches), s['m'])
  cap = roboscout.scout({}, s['m'], tc)
  return cap['expo']