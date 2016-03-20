import roboscout
import metatournament
import officialparser
import scratch
from futil import *

def predict_tournament(f, ts):
    expos, vars, caps = metatournament.best_robots(
        officialparser.get_tournaments())

    expos = filter_dict(lambda t: t in ts, expos)
    vals = expos.values()
    expo_avg = avg(vals)

    for team in ts:
        if team not in expos:
            expos[team] = expo_avg

    matches = roboscout.getData(f, True)
    for match in matches:
        rs = round(expos[match['Red 1']] + expos[match['Red 2']])
        bs = round(expos[match['Blue 1']] + expos[match['Blue 2']])
        match['Red Score'] = rs
        match['Blue Score'] = bs



    return matches, map(lambda m: [m['Round #'],
                                   m['Red Score'],
                                   m['Blue Score']], matches)

if __name__ == '__main__':
    predicted_matches, scores = predict_tournament('matchlist_hopper.csv',
                       scratch.HOPPER)

    real_matches = roboscout.getData('scoreboard_hppr.csv')

    confirmation = []

    for x in xrange(len(predicted_matches)):
        p = predicted_matches[x]
        r = real_matches[x]
        pw = 'Red' if p['Red Score'] > p['Blue Score'] else 'Blue'
        rw = 'Red' if int(r['Red Score']) > int(r['Blue Score']) else 'Blue'

        confirmation.append({'Round #': p['Round #'],
                             'Red Diff': p['Red Score'] - int(r['Red Score']),
                             'Blue Diff': p['Blue Score'] - int(r['Blue Score']),
                             'Win Predicted': pw == rw
        })

    h = ['Round #', 'Red Diff', 'Blue Diff', 'Win Predicted']

    d = map(lambda n: [n['Round #'],
                       n['Red Diff'],
                       n['Blue Diff'],
                       n['Win Predicted']
                       ], confirmation)
    print round(sum(map(lambda n: 1 if n['Win Predicted'] else 0, confirmation))/81.0, 3)

    # scratch.print_table(h, d)


    # scratch.print_table(['#', 'Red', 'Blue'], scores)
