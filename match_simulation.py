import numpy as np
import random


def normal(expo, std):
    return np.random.normal(expo, std)

def discrete(contrib):
    return random.choice(contrib)

def discrete_dist(contrib, std):
    return normal(discrete(contrib), std)


def simulate_match(m, s, dist='discrete'):
    red = 0
    blue = 0
    for x in xrange(10000):
        bluescore = 0
        redscore = 0
        for pos in ['Red 1', 'Red 2', 'Blue 1', 'Blue 2']:
            team = m[pos]
            expo = s['expo'][team]
            std = s['variance'][team]
            if dist == 'discrete':
                score = discrete(s['contribution'])
            elif dist == 'normal':
                score = normal(expo, std)
            elif dist == 'discretedist':
                score = discrete_dist(s['contribution'][team], std)
            if 'Red' in pos:
                redscore += score
            else:
                bluescore += score
        if redscore > bluescore:
            red += 1
        else:
            blue += 1
    return (float(red)/(red+blue)*100, float(blue)/(red+blue)*100)

def simulate_matchlist(matchlist, scout, start, dist='discrete'):
    result = []
    for match in matchlist[start:]:
        m = match.copy()
        m['prediction'] = simulate_match(match, scout, dist)
        result.append(m)
    return result
