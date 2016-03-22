import roboscout
import metatournament
import officialparser
import scratch
from futil import *

def predict_tournament(matchlist_file, start=0):
    """
        - Given a matchlist for a tournament, predict the winner of each match.
        - If only the matchlist file is given, predict the tournament based
        on previous match data.
        - If a starting round is specified, predict the tournament based on
        previously available match data when available, falling back on
        old data when necessary.
    """
    # Parse Matchlist
    matches = roboscout.getData(matchlist_file, True)
    # Get a list of teams from the matchlist
    teams = []
    for match in matches:
        positions = ['Red 1', 'Red 2', 'Blue 1', 'Blue 2']
        for n in positions:
            if match[n] not in teams:
                teams.append(match[n])

    # Pre-scout from the main match pool
    expos, vars, caps = metatournament.best_robots(
        officialparser.get_tournaments())

    # filter expo to only include teams we care about
    expos = filter_dict(lambda t: t in teams, expos)

    # Run roboscout on the first n rounds to get more accurate
    # expected output when possible.

    s = roboscout.scout(matches[:start])

    for team in teams:
        if team in s['expo']:
            expos[team] = s['expo'][team]

    # Get an average for teams with no data
    expo_avg = avg(expos.values())
    for team in teams:
        if team not in expos:
            expos[team] = expo_avg

    # Fill in match predictions based on expected output for each team
    for match in matches:
        rs = round(expos[match['Red 1']] + expos[match['Red 2']])
        bs = round(expos[match['Blue 1']] + expos[match['Blue 2']])
        match['Red Score'] = rs
        match['Blue Score'] = bs

    return matches

def compare_matchlists(m1, m2):
    """
        Given two matchlists, compare how different their scores are
        for each round, and if the alliance who won was the same
    """
    confirmation = []
    for x in xrange(len(m1)):
        p = m1[x]
        r = m2[x]
        pw = 'Red' if p['Red Score'] > p['Blue Score'] else 'Blue'
        rw = 'Red' if int(r['Red Score']) > int(r['Blue Score']) else 'Blue'

        confirmation.append({
            'Round #': p['Round #'],
            'Red Diff': p['Red Score'] - int(r['Red Score']),
            'Blue Diff': p['Blue Score'] - int(r['Blue Score']),
            'Win Predicted': pw == rw
        })
    return confirmation

if __name__ == '__main__':
    confirmation = compare_matchlists(
        predict_tournament('scoreboard_tesla.csv'),
        roboscout.getData('scoreboard_tesla.csv'))

    h = ['Round #', 'Red Diff', 'Blue Diff', 'Win Predicted']

    d = map(lambda n: [n['Round #'],
                       n['Red Diff'],
                       n['Blue Diff'],
                       n['Win Predicted']
                       ], confirmation)
    print round(sum(map(
        lambda n: 1 if n['Win Predicted'] else 0,
        confirmation))/float(len(confirmation)), 2)
