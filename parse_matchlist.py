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
        elif len(cells) > 1:
            matches[-1]['Red 2'] = team(cells[0].string)
            matches[-1]['Blue 2'] = team(cells[1].string)

    return matches

def save_matchlist(matchlist, filename):
    fieldnames = ['Round #','Red 1','Red 2','Blue 1','Blue 2','Red Score','Blue Score']
    with open('matchlists/'+filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in matchlist:
            writer.writerow(row)

def details_to_matchlist(data, category):
  matches = []
  if category not in ['Tot', 'Auto', 'Tele', 'EndG']:
    category = 'Tot' 
  for row in data:
    red = row['Red Teams'].split(' ')
    blue = row['Blue Teams'].split(' ');
    matches.append({
      'Red 1': red[0],
      'Red 2': red[1],
      'Blue 1': blue[0],
      'Blue 2': blue[1],
      'Red Score': row['Red ' + category],
      'Blue Score': row['Blue ' + category]
      })
  return matches

def parse_details(html_doc):
  soup = BeautifulSoup(html_doc, 'html.parser')
  rows = soup.find_all('tr')[2:]
  matches = []
  for row in rows:
    cells = row.find_all('td')
    if cells[0].string[0] == 'Q':
      matches.append({
        'Red Teams': cells[2].string,
        'Blue Teams': cells[3].string,
        'Red Tot': cells[4].string,
        'Red Auto': cells[5].string,
        'Red Tele': cells[7].string,
        'Red EndG': cells[8].string,
        'Blue Tot': cells[10].string,
        'Blue Auto': cells[11].string,
        'Blue Tele': cells[13].string,
        'Blue EndG': cells[14].string
        })
  return matches

if __name__ == '__main__':
    
    mode = sys.argv[2]
    url = sys.argv[1]
    filename = sys.argv[3]

    html_doc = urllib2.urlopen(url).read()
    if mode == 'match':
        matches = html_to_matchlist(html_doc)
    elif mode in ['Tot', 'Auto', 'EndG', 'Tele']:
        matches = details_to_matchlist(parse_details(html_doc), mode)
    else:
        matches = []

    save_matchlist(matches, filename)
