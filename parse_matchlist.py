#!/usr/bin/python

import unicodecsv as csv
import re
from bs4 import BeautifulSoup
import urllib2
import sys
import unicodedata
from roboscout import scout

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
                'roundnum': cells[0].string[2:],
                'redscore': scores[0],
                'bluescore': scores[1],
                'red1': team(cells[2].string),
                'blue1': team(cells[3].string)
            }
            matches.append(d)
        elif len(cells) > 1:
            matches[-1]['red2'] = team(cells[0].string)
            matches[-1]['blue2'] = team(cells[1].string)

    return matches

def save_matchlist(matchlist, filename):
    fieldnames = ['roundnum','red1','red2','blue1','blue2','redscore','bluescore']
    with open('matchlists/'+filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in matchlist:
            writer.writerow(row)

def details_to_matchlist(data, category='Tot'):
  matches = []
  if category not in ['Tot', 'Auto', 'Tele', 'EndG']:
    category = 'Tot' 
  for row in data:
    red = row['Red Teams'].split(' ')
    blue = row['Blue Teams'].split(' ');
    matches.append({
      'roundnum': row['Round #'],
      'red1': red[0],
      'red2': red[1],
      'blue1': blue[0],
      'blue2': blue[1],
      'redscore': row['Red ' + category],
      'bluescore': row['Blue ' + category]
      })
  return matches

def parse_details(html_doc):
  soup = BeautifulSoup(html_doc, 'html.parser')
  rows = soup.find_all('tr')[2:]
  matches = []
  for row in rows:
    cells = row.find_all('td')
    if row.attrs.get('align', '').lower() == 'center' and \
        len(cells) > 0 and \
        cells[0].string[0] == 'Q' and \
        int(cells[0].string[2:]) <= 144:
      matches.append({
        'Round #': cells[0].string[2:],
        'Red Teams': cells[2].string,
        'Blue Teams': cells[3].string,
        'Red Tot': int(cells[4].string), # - int(cells[9].string)
        'Red Auto': cells[5].string,
        'Red Tele': cells[7].string,
        'Red EndG': cells[8].string,
        'Blue Tot': int(cells[10].string), # - int(cells[15].string)
        'Blue Auto': cells[11].string,
        'Blue Tele': cells[13].string,
        'Blue EndG': cells[14].string
        })
  return matches

def get_playoff_details(html_doc):
  soup = BeautifulSoup(html_doc, 'html.parser')
  rows = soup.find_all('tr')[2:]
  alliances = [(), (), (), ()]
  finalalliance = [(), ()]
  red = 0
  blue = 0
  for row in rows:
    cells = row.find_all('td')
    if row.attrs.get('align', '').lower() != 'center' or len(cells) <= 0: 
      continue
    t = cells[0].string

    if t[:2] == 'SF':
      if t[3] == '1':
        alliances[0] = cells[2].string.strip().split(' ')
        alliances[3] = cells[3].string.strip().split(' ')
      elif t[3] == '2':
        alliances[1] = cells[2].string.strip().split(' ')
        alliances[2] = cells[3].string.strip().split(' ')
    if t[0] == 'F':
      w = cells[1].string.strip().split(' ')[-1]
      finalalliance[0] = cells[2].string.strip().split(' ')
      finalalliance[1] = cells[3].string.strip().split(' ')
      if w == 'R':
        red += 1
      elif w == 'B':
        blue += 1

  return (alliances, finalalliance[0] if red > blue else finalalliance[1])
    
  

def save_details(deets, filename):
  import operator
  fieldnames = ['Team','Tot','Auto','Tele','EndG']
  details = []
  for k, v in deets.iteritems():
    details.append({
      'Team': k, 
      'Tot': v['Tot'],
      'Auto': v['Auto'],
      'Tele': v['Tele'],
      'EndG': v['EndG']})

  details = sorted(details, key=operator.itemgetter('Tot'), reverse=True)
  with open('details/'+filename, 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      for row in details:
          writer.writerow(row)
if __name__ == '__main__':
    
    # mode = sys.argv[2]
    url = sys.argv[1]
    filename = sys.argv[2]

    if url.startswith('http'):
        html_doc = urllib2.urlopen(url).read()
    else:
        html_doc = open(url, 'r').read()

    html_doc = html_doc.replace("\xc2\xa0", " ")
    # if mode == 'match':
    #     matches = html_to_matchlist(html_doc)
    # elif mode in ['Tot', 'Auto', 'EndG', 'Tele']:
    #     matches = details_to_matchlist(parse_details(html_doc), mode)

    details = parse_details(html_doc)
    tms = {}
    for mode in ['Tot', 'Auto', 'EndG', 'Tele']:
      matches = details_to_matchlist(details, mode)
      save_matchlist(matches, filename+mode+'.csv')
      s = scout(matches)
      for k, v in s['expo'].iteritems():
        if k not in tms:
          tms[k] = {}
        tms[k][mode] = v

    save_details(tms, filename)
    # save_matchlist(matches, filename)
