import numpy as np
import random


def normal(expo, std):
    return np.random.normal(expo, std)

def discrete(contrib):
    return random.choice(contrib) if len(contrib) > 0 else 0

def discrete_dist(contrib, std):
    return normal(discrete(contrib), std)

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

    d = [(round(float(f['red'])/(f['red']+f['blue'])*100), round(float(f['blue'])/(f['red']+f['blue'])*100)) for f in details]
    winner = red_alliance if red > blue else blue_alliance
    return (winner, (round(float(red)/(red+blue)*100, 1), round(float(blue)/(red+blue)*100, 1)), d)

def simulate_playoffs(alliances, scout, dist='discrete'):
    onefour, prob1, d1 = simulate_series(alliances[0], alliances[3], scout, dist)
    twothree, prob2, d2 = simulate_series(alliances[1], alliances[2], scout, dist)

    winner, prob3, d3 = simulate_series(onefour, twothree, scout, dist)

    return {'SF-1': (onefour, prob1, d1), 'SF-2': (twothree, prob2, d2), 'F': (winner, prob3, d3)}


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




