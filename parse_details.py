import csv

def parse_details(csv_file, category):
  data = []
  if category not in ['Tot', 'Auto', 'Tele', 'EndG']:
    category = 'Tot'
  with open(csv_file, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      red = row['Red Teams'].split(' ')
      blue = row['Blue Teams'].split(' ');
      data.append({
        'Red 1': red[0],
        'Red 2': red[1],
        'Blue 1': blue[0],
        'Blue 2': blue[1],
        'Red Score': row['Red ' + category],
        'Blue Score': row['Blue ' + category]
        })
  return data

if __name__ == '__main__':
  import operator
  from roboscout import *
  from officialparser import *
  from metatournament import *
  from futil import *
  from scratch import print_table
  s = scout(parse_details('matchlists/penndetails.csv', 'EndG'))
  h = ['team', 'expo', 'var', 'opar']
  d = map(lambda t: [t,
                       s['expo'][t],
                       round(s['variance'][t]),
                       s['opar'][t]],
                       s['expo'].keys())
  d = sorted(d, key=operator.itemgetter(1), reverse=True)
  print_table(h, d)