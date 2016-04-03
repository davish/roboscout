from roboscout import *
from officialparser import *
from metatournament import *
from futil import *

WORLDS = ['535', '2997', '3141', '3415', '3486', '3491', '3537', '3595', '3658', '3664', '3781', '4029', '4082', '4130', '4143', '4290', '4318', '4444', '4717', '4855', '4924', '4997', '5009', '5070', '5110', '5169', '5202', '5220', '5229', '5380', '5385', '5795', '5890', '5899', '5916', '5942', '5943', '5975', '6022', '6047', '6051', '6055', '6081', '6109', '6123', '6134', '6137', '6209', '6220', '6299', '6377', '6389', '6451', '6899', '6913', '6981', '7013', '7117', '7149', '7152', '7172', '7209', '7242', '7300', '7314', '7350', '7351', '7393', '7477', '7486', '7550', '7591', '7655', '8189', '8221', '8327', '8372', '8375', '8466', '8471', '8390', '8528', '8606', '8620', '8644', '8660', '8668', '8681', '8686', '8907', '8913', '8995', '9048', '9205', '9662', '9789', '9794', '9804', '9851', '9945', '10030', '10060', '10165', '10392', '10479', '11040', '11041', '11042', '11043', '11044', '11047', '11048', '11051', '11053', '11050', 11052]

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
    scouted = mapd(scout, parse_SR())
    teamToRegion = {}
    regionToName = {'WG': 'West',
                    'EH': 'East',
                    'NO': 'North',
                    'SO': 'South',
                    'SB': 'South',
                    'ET': 'East',
                    'NR': 'North',
                    'WS': 'West'}
    s = {}
    for tourney, stats in scouted.iteritems():
        for category, teams in stats.iteritems():
            if category not in s:
                s[category] = {}
            teams = filter_dict(lambda t: t in WORLDS, teams)
            s[category].update(teams)
            for t in teams.keys():
                teamToRegion[t] = tourney

    avgexpo = avg(s['expo'].values())
    opar = mapd(lambda o: round(o/avgexpo,1), s['expo'])

    h = ['team', 'expo', 'var', 'opar', 'region']
    d = map(lambda t: [t,
                       s['expo'][t],
                       round(s['variance'][t]),
                       opar[t],
                       regionToName[teamToRegion[t]]], s['expo'].keys())
    d = sorted(d, key=operator.itemgetter(1), reverse=True)
    print_table(h, d)
