from roboscout import *
from officialparser import *
from metatournament import *
from futil import *

WORLDS = [
    '535',
'3141',
'3491',
'3595',
'3658',
'3664',
'4130',
'4318',
'4444',
'4717',
'4855',
'5009',
'5064',
'5070',
'5169',
'5229',
'5380',
'5843',
'5890',
'5899',
'5942',
'5943',
'6051',
'6055',
'6081',
'6123',
'6134',
'6209',
'6377',
'6899',
'6913',
'7013',
'7117',
'7149',
'7152',
'7300',
'7314',
'7393',
'7550',
'8189',
'8327',
'8372',
'8375',
'8471',
'8528',
'8620',
'8995',
'9048',
'9205',
'9662',
'9794',
'9804',
'9915',
'10030',
'10479',
'11041',
'11043',
'11047',
'11053',
'11056',
'11061',
'11064',
'11071',
'11080'
]
def print_table(h, d):
  print ("%s\t| "*len(h)) % tuple(h)
  for row in d:
    s = ""
    for x in xrange(len(h)):
      s = s + str(row[x]) + "\t| "
    print s

def top_teams():
    t = get_tournaments()

    expos, oars, caps = best_robots(t)

    import operator
    rank = sorted(expos.items(), key=operator.itemgetter(1))
    rank.reverse()

    h = ['team', 'indo', 'high', 'mid']
    # h = ['team', 'indo', 'auto', 'high', 'mid', 'hang?']
    # h = ['team', 'indo', 'auto', 'end']
    team_stats = []

    c=1
    for team, r in rank:
        # if caps[team]['high'] > 2:
        if True:
        # if team in TESLA:
            if caps[team]['high'] > 2:
            # if True:
                team_stats.append([
                team,
                round(r),
                # round(caps[team]['auto'], 2),
                round(caps[team]['high'],2),
                round(caps[team]['mid'],2),
                # round(caps[team]['hang'],2)
            ])
            c+=1

    d = sorted(team_stats, key=operator.itemgetter(2), reverse=True)
    print_table(h, d[:20])

if __name__ == '__main__':
    import operator
    # top_teams()
    # regionToName = {'WG': 'West',
    #                 'EH': 'East',
    #                 'NO': 'North',
    #                 'SO': 'South',
    #                 'SB': 'South',
    #                 'ET': 'East',
    #                 'NR': 'North',
    #                 'WS': 'West'}
    s = scout_SR(parse_SR())

    avgexpo = avg(s['expo'].values())
    opar = mapd(lambda o: round(o/avgexpo,1), s['expo'])

    h = ['team', 'expo', 'var', 'opar']
    d = map(lambda t: [t,
                       s['expo'][t],
                       round(s['variance'][t]),
                       opar[t]],
                       s['expo'].keys())
    d = sorted(d, key=operator.itemgetter(1), reverse=True)
    print_table(h, d)
