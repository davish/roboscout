import csv
from bs4 import BeautifulSoup

def details_to_matchlist(data, category):
  matches = []
  if category not in ['Tot', 'Auto', 'Tele', 'EndG']:
    category = 'Tot' 
  for row in data:
    red = row['Red Teams'].split(' ')
    blue = row['Blue Teams'].split(' ');
    matchs.append({
      'Red 1': red[0],
      'Red 2': red[1],
      'Blue 1': blue[0],
      'Blue 2': blue[1],
      'Red Score': row['Red ' + category],
      'Blue Score': row['Blue ' + category]
      })
  return matches

def parse_details(details_file):
  soup = BeautifulSoup(html_doc, 'html.parser')
  rows = soup.find_all('tr')[2:]
  matches = []
  for row in rows:
    cells = row.find_all('td')
    print cells
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
  import operator
  from roboscout import *
  from officialparser import *
  from metatournament import *
  from futil import *
  from scratch import print_table
  import urllib2

  html_doc = urllib2.urlopen('http://scoring.ftceast.org/cache/MatchResultsDetails_East_Super-Regional_Tesla.html').read()
  s = scout(details_to_matchlist(parse_details(html_doc), 'EndG'))
  h = ['team', 'expo', 'var', 'opar']
  d = map(lambda t: [t,
                       s['expo'][t],
                       round(s['variance'][t]),
                       s['opar'][t]],
                       s['expo'].keys())
  d = sorted(d, key=operator.itemgetter(1), reverse=True)
  print_table(h, d)