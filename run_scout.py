#!/usr/bin/python

"""
run_scout.py

Script to run roboscout on a specific match, displaying teams
in order of best to wors ("best" being decided by which team's expected output is most above average).

Takes the path to a matchlist as a command-line argument.
"""

from roboscout import *
from futil import *
import sys

def print_table(h, d):
    print ("%s\t| "*len(h)) % tuple(h)
    for row in d:
        s = ""
        for x in xrange(len(h)):
            s = s + str(row[x]) + "\t| "
        print s

if __name__ == '__main__':
    import operator
    f = sys.argv[1] if len(sys.argv) > 1 else 'matchlists/scoreboard.csv'
    s = scout(getData(f))
    h = ['team', 'opar', 'expo', 'var']

    d = []
    for team in s['opar'].keys():
        d.append([team,
                  s['opar'][team],
                  s['expo'][team],
                  s['variance'][team]])

    d = sorted(d, key=operator.itemgetter(2), reverse=True)
    print_table(h, d)
