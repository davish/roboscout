from roboscout import *
from officialparser import *
from metatournament import *
from futil import *

def print_table(h, d):
  print ("%s\t| "*len(h)) % tuple(h)
  for row in d:
    s = ""
    for x in xrange(len(h)):
      s = s + str(row[x]) + "\t| "
    print s

if __name__ == '__main__':
  t = get_tournaments()
  
  teams = progression(t)
  print map(lambda d: d['tournament'] + ": " + str(d['robot']['caps']['high']), 
    teams['4997'])

  # expos, oars, caps = best_robots(t)

  # import operator
  # rank = sorted(expos.items(), key=operator.itemgetter(1))
  # rank.reverse()

  # h = ['team', 'indo', 'var', 'auto', 'high', 'mid', 'hang?']
  # d = []

  # c=1
  # for team, r in rank:
  #   # if caps[team]['high'] > 2:
  #   d.append([
  #     team, 
  #     round(r), 
  #     round(oars[team]), 
  #     round(caps[team]['auto'], 2),
  #     round(caps[team]['high'],2), 
  #     round(caps[team]['mid'],2), 
  #     round(caps[team]['hang'],2)
  #     ])
  #   c+=1

   # print caps['6051']['auto']
  # d = sorted(d[:20], key=operator.itemgetter(1), reverse=True)
  # print_table(h, d)

  



 