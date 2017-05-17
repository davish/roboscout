import numpy as np
import random


def normal(expo, std):
    return np.random.normal(expo, std)

def discrete(contrib):
    return random.choice(contrib) if len(contrib) > 0 else 0

def discrete_dist(contrib, std):
    return normal(discrete(contrib), std)


def simulate_match(m, s, dist):
    red = 0
    blue = 0
    for x in xrange(10000):
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
            red += 1
        else:
            blue += 1
    return (float(red)/(red+blue)*100, float(blue)/(red+blue)*100)

def simulate_matchlist(matchlist, scout, start, dist='discrete'):
    result = []
    for match in matchlist[(start-1):]:
        m = match.copy()
        m['prediction'] = simulate_match(match, scout, dist)
        result.append(m)
    return result
