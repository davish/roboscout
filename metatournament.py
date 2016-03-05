import roboscout

HIGH_GOAL=7
LOW_GOAL=8
MID_GOAL=9
HANG=13

ALLOWED_TEAMS = ['6081','5017','4286','8221','5916','7423','7182','7393','5421','9794','8702','4318','7988','6029','4029','6055','6040','3737','8681','4096','8644','7350','248','7486','6037','8574','3415','7149','4082','4107','6347','5485','4347','5069','6051','4344','18','3371','6899','5163','4137','10392','9372','9321','7164','8528','8645','2818','7314','5169','8509','5484','121','10815','6527','8526','6955','3397','8297','4419','9901','10358','6700','8390','9845','8498','6341','4924','7117','8619']

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
      if team in ALLOWED_TEAMS:
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