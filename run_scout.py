#!/usr/bin/python

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
    s = scout(getData(sys.argv[1] if len(sys.argv) > 1 else 'scoreboard.csv'))
    h = ['#', 'opar', 'oar']

    d = []
    for team in s['opar'].keys():
        d.append([team,
                  s['opar'][team],
                  s['oar'][team]])

    d = sorted(d, key=operator.itemgetter(1), reverse=True)
    print_table(h, d)
