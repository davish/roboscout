from roboscout import *
from officialparser import *
from metatournament import *
from futil import *
from parse_matchlist import *

def print_table(h, d):
  print ("%s\t| "*len(h)) % tuple(h)
  for row in d:
    s = ""
    for x in xrange(len(h)):
      s = s + str(row[x]) + "\t| "
    print s

if __name__ == '__main__':
    
