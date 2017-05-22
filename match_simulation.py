import numpy as np
import random


def normal(expo, std):
    return np.random.normal(expo, std)

def discrete(contrib):
    return random.choice(contrib) if len(contrib) > 0 else 0

def discrete_dist(contrib, std):
    return normal(discrete(contrib), 40)

def simulate_round(m, s, dist):
    bluescore = 0
    redscore = 0
    for pos in ['red1', 'red2', 'blue1', 'blue2']:
        team = m[pos]
        expo = s['expo'][team]
        std = s['variance'][team]
        if dist == 'discrete':
            score = discrete(s['contribution'][team])
        elif dist == 'normal':
            score = normal(expo, std)
        elif dist == 'discretedist':
            score = discrete_dist(s['contribution'][team], std)
        if 'red' in pos:
            redscore += score
        else:
            bluescore += score
    if redscore > bluescore:
        return 'red'
    elif bluescore > redscore:
        return 'blue'
    else:
        return 'tie'


def simulate_match(m, s, dist):
    red = 0
    blue = 0
    for x in xrange(10000):
        res = simulate_round(m, s, dist)
        if res == 'red':
            red += 1
        elif res == 'blue':
            blue += 1
    return (float(red)/(red+blue)*100, float(blue)/(red+blue)*100)

def simulate_matchlist(matchlist, scout, start, dist='discrete'):
    result = []
    for match in matchlist[(start-1):]:
        m = match.copy()
        m['prediction'] = simulate_match(match, scout, dist)
        result.append(m)
    return result

def simulate_series(red_alliance, blue_alliance, scout, dist='discrete'):
    red = 0
    blue = 0
    details = [{'red': 0, 'blue': 0, 'tie': 0}, {'red': 0, 'blue': 0, 'tie': 0}, {'red': 0, 'blue': 0, 'tie': 0}]
    for _ in xrange(10000):
        wins = {'red': 0, 'blue': 0, 'tie': 0}
        alt = False
        r = 0
        while wins['red'] < 2 and wins['blue'] < 2:
            match, alt = arrange_match(red_alliance, blue_alliance, alt)
            result = simulate_round(match, scout, dist)
            wins[result] += 1
            details[r][result] += 1
            if result != 'tie': r += 1

        if wins['red'] > wins['blue']:
            red += 1
        else:
            blue += 1

    try:
        d = [(round(float(f['red'])/(f['red']+f['blue'])*100), round(float(f['blue'])/(f['red']+f['blue'])*100)) for f in details]
    except Exception:
        d = [(0, 0) for f in details]
    winner = red_alliance if red > blue else blue_alliance
    return (winner, (round(float(red)/(red+blue)*100, 1), round(float(blue)/(red+blue)*100, 1)), d)

def get_other_alliance(a, a1, a2):
    if set(a) == set(a1):
        return a2
    else:
        return a1

def simulate_playoffs(alliances, scout, dist='discrete'):
    onefour, prob1, d1 = simulate_series(alliances[0], alliances[3], scout, dist)
    twothree, prob2, d2 = simulate_series(alliances[1], alliances[2], scout, dist)

    loser1 = get_other_alliance(onefour, alliances[0], alliances[3])
    loser2 = get_other_alliance(twothree, alliances[1], alliances[2])

    loserwin1, prob4, d4 = simulate_series(onefour, loser2, scout, dist)
    loserwin2, prob5, d5 = simulate_series(loser1, twothree, scout, dist)
    losers, prob6, d6 = simulate_series(loser1, loser2, scout, dist)

    winner, prob3, d3 = simulate_series(onefour, twothree, scout, dist)

    # return {'SF-1': (onefour, prob1, d1), 'SF-2': (twothree, prob2, d2), 'F': (winner, prob3, d3)}

    return ({
        str(onefour): {
            'seed': '1' if set(onefour) == set(alliances[0]) else '4',
            'SF': {
                'prob': prob1,
                'details': d1
            },
            'F': {
                str(twothree): {
                    'prob': prob3,
                    'details': d3
                },
                str(loser2): {
                    'prob': prob4,
                    'details': d4
                }
            }
        },
        str(loser1): {
            'seed': '1' if set(loser1) == set(alliances[0]) else '4',
            'SF': {
                'prob': prob1,
                'details': d1
            },
            'F': {
                str(twothree): {
                    'prob': prob5,
                    'details': d5
                },
                str(loser2): {
                    'prob': prob6,
                    'details': d6
                }
            }
        },
        str(twothree): {
            'seed': '2' if set(twothree) == set(alliances[1]) else '3',
            'SF': {
                'prob': prob2,
                'details': d2,
            },
            'F': {
                str(onefour): {
                    'prob': prob3,
                    'details': d3
                },
                str(loser1): {
                    'prob': prob5,
                    'details': d5
                }
            }
        },
        str(loser2): {
            'seed': '2' if set(loser2) == set(alliances[1]) else '3',
            'SF': {
                'prob': prob2,
                'details': d2,
            },
            'F': {
                str(onefour): {
                    'prob': prob4,
                    'details': d4
                },
                str(loser1): {
                    'prob': prob6,
                    'details': d6
                }
            }
        },
    }, {'SF-1': (onefour, prob1, d1), 'SF-2': (twothree, prob2, d2), 'F': (winner, prob3, d3)})


def arrange_match(red_alliance, blue_alliance, alternate=False):
    if alternate:
        return ({
            'red1': red_alliance[0], 'red2': red_alliance[2], 
            'blue1': blue_alliance[0], 'blue2': blue_alliance[2]
            }, not alternate)
    else:
        return ({
            'red1': red_alliance[0], 'red2': red_alliance[1], 
            'blue1': blue_alliance[0], 'blue2': blue_alliance[1]
            }, not alternate)


