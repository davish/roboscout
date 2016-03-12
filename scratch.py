from roboscout import *
from officialparser import *
from metatournament import *
from futil import *

HOPPER = [
'18',
'248',
'3371',
'3415',
'4029',
'4096',
'4137',
'4286',
'4347',
'4486',
'5017',
'5163',
'5421',
'5485',
'6029',
'6040',
'6055',
'6341',
'6527',
'6899',
'7117',
'7164',
'7314',
'7393',
'7486',
'8221',
'8390',
'8509',
'8528',
'8619',
'8645',
'8702',
'9372',
'9845',
'9927',
'10392'
]

TESLA = [
'121',
'2818',
'3397',
'3737',
'4082',
'4107',
'4244',
'4318',
'4419',
'4924',
'5069',
'5169',
'5484',
'5916',
'6037',
'6051',
'6081',
'6347',
'6700',
'6955',
'7149',
'7182',
'7350',
'7423',
'7988',
'8297',
'8498',
'8526',
'8574',
'8644',
'8681',
'9371',
'9794',
'9901',
'10358',
'10815'
]

EAST = HOPPER + TESLA

def print_table(h, d):
  print ("%s\t| "*len(h)) % tuple(h)
  for row in d:
    s = ""
    for x in xrange(len(h)):
      s = s + str(row[x]) + "\t| "
    print s

if __name__ == '__main__':
  t = get_tournaments()

  # print mapd(mode, auto_ending_pos(scout(t['Hudson Valley Championship'])))

  # teams = progression(t)
  # print map(lambda d: d['tournament'] + ": " + str(d['robot']['caps']['auto']),
  #   teams['6081'])

  expos, oars, caps = best_robots(t)

  import operator
  rank = sorted(expos.items(), key=operator.itemgetter(1))
  rank.reverse()

  h = ['team', 'indo', 'auto', 'high', 'mid', 'hang?']
  # h = ['team', 'indo', 'auto', 'end']
  d = []

  c=1
  for team, r in rank:
    # if caps[team]['high'] > 2:
    # if True:
    if team in TESLA:
    #   if caps[team]['high'] > 2:
      if True:
        d.append([
          team,
          round(r),
          # round(oars[team]),
          round(caps[team]['auto'], 2),
        #   round(caps[team]['autopos'], 2),
          round(caps[team]['high'],2),
          round(caps[team]['mid'],2),
          round(caps[team]['hang'],2)
          ])
        c+=1

  d = sorted(d, key=operator.itemgetter(3), reverse=True)
  print_table(h, d[:20])
