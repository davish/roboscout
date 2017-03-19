#!/usr/bin/python

import csv
import re
from bs4 import BeautifulSoup
import urllib2
import sys
import unicodedata

def team(s):
    if s[-1] == '*':
        return s[:-1]
    else:
        return s

def html_to_matchlist(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    rows = soup.find_all('tr')[1:]
    matches = []
    scorematcher = re.compile(r"(\d+)-(\d+) ([R|B|T])")

    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 2 and cells[0].string[:2] == 'Q-': # if this row is a new qualifying match,
            sm = scorematcher.match(cells[1].string)
            if sm:
                scores = sm.groups()
            elif len(cells) == 2:
                scores = ('', '')
            d = {
                'Round #': cells[0].string[2:],
                'Red Score': scores[0],
                'Blue Score': scores[1],
                'Red 1': team(cells[2].string),
                'Blue 1': team(cells[3].string)
            }
            matches.append(d)
        else:
            matches[-1]['Red 2'] = team(cells[0].string)
            matches[-1]['Blue 2'] = team(cells[1].string)

    return matches

def save_matchlist(matchlist, filename):
    fieldnames = ['Round #','Red 1','Red 2','Blue 1','Blue 2','Red Score','Blue Score']
    with open('matchlists/'+filename+'.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in matchlist:
            writer.writerow(row)

if __name__ == '__main__':
    # f = open(sys.argv[1], 'r')
    # html_doc = f.read()
    html_doc = urllib2.urlopen('http://scoring.ftceast.org/cache/MatchResults_East_Super-Regional_Hopper.html').read()
    # html_doc = unicodedata.normalize("NFKD", html_doc)
    # f.close()
    matches = html_to_matchlist(html_doc)
    save_matchlist(matches, 'hopper1')
