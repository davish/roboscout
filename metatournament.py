import roboscout
from futil import *

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
  autoend = futil.mapd(max, auto_ending_pos(s))
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
      'auto': auto[team],
      'autopos': autoend[team]
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
  ac = futil.mapd(
      lambda matches: map(lambda m: m[m['team']+' Auto'], matches), s['m'])
  auto = roboscout.scout({}, s['m'], ac)
  return auto['expo']

def capabilities(s, i):
  tc = futil.mapd(lambda matches: map(
      lambda m: m[m['team']+' Breakdown'][i], matches), s['m'])
  cap = roboscout.scout({}, s['m'], tc)
  return cap['expo']

def auto_ending_pos(s):
    ap = futil.mapd(lambda matches: map(
        lambda m: m[m['team']+' Breakdown'][0]
        if m['position'] == 0 else
        m[m['team']+' Breakdown'][1], matches), s['m'])

    return ap

def mode(list):

	d = {}
	for elm in list:
		try:
			d[elm] += 1
		except(KeyError):
			d[elm] = 1

	keys = d.keys()
	max = d[keys[0]]

	for key in keys[1:]:
		if d[key] > max:
			max = d[key]

	max_k = []
	for key in keys:
		if d[key] == max:
			max_k.append(key),
	return max_k[0]

def scout_SR(parsed):
    scouted = mapd(roboscout.scout, parsed)
    # teamToRegion = {}
    s = {}
    for tourney, stats in scouted.iteritems():
        for category, teams in stats.iteritems():
            if category not in s:
                s[category] = {}
            # teams = filter_dict(lambda t: t in WORLDS, teams)
            s[category].update(teams)
    return s
