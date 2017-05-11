import numpy as np

def simulate_match(m, s):
    red = 0
    blue = 0
    for x in xrange(10000):
        bluescore = 0
        redscore = 0
        for pos in ['Red 1', 'Red 2', 'Blue 1', 'Blue 2']:
            # pass
            team = m[pos]
            expo = s['expo'][team]
            std = s['variance'][team]
            score = np.random.normal(expo, std)
            if 'Red' in pos:
                redscore += score
            else:
                bluescore += score
        if redscore > bluescore:
            red += 1
        else:
            blue += 1
    return (float(red)/(red+blue)*100, float(blue)/(red+blue)*100)

def simulate_matchlist(matchlist, scout, start):
    result = []
    for match in matchlist[start:]:
        m = match.copy()
        m['prediction'] = simulate_match(match, scout)
        result.append(m)
    return result