import roboscout

HIGH_GOAL=7
LOW_GOAL=8
MID_GOAL=9
HANG=13


def progression(ts):
  teams = {}
  for tourney, matches in ts.iteritems():
    robots = robot_stats(matches)
    for team, robot in robots.iteritems():
      if team not in teams:
        teams[team] = []
      teams[team].append({'tournament': tourney, 'robot': robot})
  return teams


def robot_stats(t):
  s = roboscout.scout(t)
  highcap = capabilities(s, HIGH_GOAL)
  midcap = capabilities(s, MID_GOAL)
  lowcap = capabilities(s, LOW_GOAL)
  hangcap = capabilities(s, HANG)
  auto = auto_expo(s)
  teams = {}
  for team in highcap.keys():
    teams[team] = {
    'expo': s['expo'][team],
    'variance': s['variance'][team],
    'caps': {
      'high': highcap[team],
      'mid': midcap[team],
      'low': lowcap[team],
      'hang': hangcap[team],
      'auto': auto[team]
      }
    }

  return teams

def best_robots(ts):
  ranks = {}
  oar = {}
  caps = {}
  for tourney, matches in ts.iteritems():
    robots = robot_stats(matches)
    for team, robot in robots.iteritems():
      # if team in TESLA:
      if team in ranks:
        if robot['expo'] < ranks[team]:
          continue
      ranks[team] = robot['expo']
      oar[team] = robot['variance']
      caps[team] = robot['caps']

  return ranks, oar, caps

import futil

def auto_expo(s):
  ac = futil.mapd(lambda matches: map(
      lambda m: m[m['team']+' Auto'], matches), s['m'])
  auto = roboscout.scout({}, s['m'], ac)
  return auto['expo']

def capabilities(s, i):
  tc = futil.mapd(lambda matches: map(
      lambda m: m[m['team']+' Breakdown'][i], matches), s['m'])
  cap = roboscout.scout({}, s['m'], tc)
  return cap['expo']
