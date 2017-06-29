# Given a input loan file, output the loan prediction results
import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import *
from bidding import bidding

from collections import defaultdict

def main(argv):
  if len(argv) < 2:
    argv.append('auto')

  loans = []
  if argv[1] == 'auto':
    loans = storage.load_from_file(config.StorageFile.LC_bidded_loans_file)
  elif argv[1] == 'lc':
    loans = storage.load_from_file(config.StorageFile.LC_purchased_loans_file)
  elif argv[1] == 'auto-past':
    loans = storage.load_from_file(config.StorageFile.AUTO_purchased_loans_file)

  good_loans = bidding.get_bid_results(loans)
  bidding.print_loan_summary(loans, good_loans)
  print
  bidding.print_loan_summary(loans, good_loans, 'loanStatus')

if __name__ == "__main__":
  main(sys.argv)
