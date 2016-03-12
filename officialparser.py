def count_score(l):
  scores = [
      auto_pos(l[0]), # ending position
      auto_pos(l[1]),
      l[2]*20, # beacon
      l[3]*10, # climbers
      auto_pos(l[4]), # ending position
      auto_pos(l[5]), # ending position
      l[6]*1, # floor goal
      l[7]*15, # high goal
      l[8]*5, # low goal
      l[9]*10, # mid goal
      l[10]*10, # climbers in shelter
      l[11]*20, # Zipliners
      l[12]*20, # All clear
      l[13]*80, # Hang
      l[16]*10,
      l[17]*40
  ]
  # print scores
  return sum(scores)

def auto_score(l):
  scores = [
      auto_pos(l[0]), # ending position
      auto_pos(l[1]),
      l[2]*20, # beacon
      l[3]*10, # climbers
  ]
  return sum(scores)


def auto_pos(n):
  if n == 0: return 0
  elif n <= 3: return 5
  elif n == 4: return 10
  elif n == 5: return 20
  elif n == 6: return 40

regions = [
  "New Jersey",
  "New York",
  "Maryland",
  "Massachusettes",
  "Connecticut",
  "Virginia",
  "Vermont",
  "Massachusetts"
]

import csv
def get_tournaments():
  tournaments = {}

  with open('holygrail.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
      if row[1] not in tournaments:
        tournaments[row[1]] = []

      if row[5] == '1': # only scrape qualification matches
        rs = map(int, row[26:44])
        bs = map(int, row[44:-1])
        tournaments[row[1]].append({
          'type': row[5],
          'match #': row[6],
          'Red 1': row[7],
          'Red 2': row[8],
          'Red 3': row[9],
          'Blue 1': row[10],
          'Blue 2': row[11],
          'Blue 3': row[12],
          'Blue Breakdown': bs,
          'Red Breakdown': rs,
          'Blue Score': count_score(bs),
          'Red Score': count_score(rs),
          'Red Auto': auto_score(rs),
          'Blue Auto': auto_score(bs)
          })
  return tournaments
