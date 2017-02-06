import csv
import re
from bs4 import BeautifulSoup
import urllib2

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
    r = urllib2.urlopen('http://csis.pace.edu/~firsttech/live/cache/MatchResults_Hudson_Valley_Championship.html')
    html_doc = r.read()
    matches = html_to_matchlist(html_doc)
    save_matchlist(matches, 'test')
