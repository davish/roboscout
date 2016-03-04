from roboscout import *
from officialparser import *
from metatournament import *


if __name__ == '__main__':
  t = get_tournaments()
  
  s = scout(t['Hudson Valley Championship'])

  # print capabilities(s, MID_GOAL)['6051']

  expos, oars, caps = best_robots(t)

  import operator
  rank = sorted(expos.items(), key=operator.itemgetter(1))
  rank.reverse()

  print "team # \t| indo \t| high \t| mid \t| hang?"
  for team, r in rank[:20]:
    s = team + "\t| " + str(round(r)) + "\t| " + str(caps[team]['high']) + "\t| "+str(round(caps[team]['mid'],2)) + "\t| "+str(caps[team]['hang'])
    print s

  # s = scout(t['Hudson Valley Championship'])
  # print s['m']['6081'][0]
  # display(s['opar'], s['oar'])