from roboscout import *
from officialparser import *
from metatournament import *
from futil import *
from parse_matchlist import *

def print_table(h, d):
  print ("%s\t| "*len(h)) % tuple(h)
  for row in d:
    s = ""
    for x in xrange(len(h)):
      s = s + str(row[x]) + "\t| "
    print s

if __name__ == '__main__':
    import operator

    teams = ['4174', '7117', '8645', '7486', '5484', '9773', '3737']

    matches = getData('matchlists/hopperendg.csv')
    matches.extend(getData('matchlists/teslaendg.csv'))
    s = scout(matches)
    for t in teams:
        print '%s \t: %s' % (t, s['expo'][t])
