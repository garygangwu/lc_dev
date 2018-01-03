import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import config
from utils import storage
from datetime import datetime
from collections import defaultdict

grade_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def print_usage():
  print
  print "python split_merge_loan_datap.py split|freshsplit|merge|stats|substats"
  print


def split():
  divided_loans = {}
  for i in list(range(0, 10)):
    divided_loans[i] = []
  loans = storage.load_from_file(config.StorageFile.LC_LOAN_EXTENDED_DATA)
  x = 0
  today = datetime.now()
  for loan in loans:
    if loan.get('numInvestors') != None:
      continue
    td = today - datetime.strptime(loan['acceptD'].split('T')[0], "%Y-%m-%d")
    if td.days >= 365 and loan['loanStatus'] == 'Current':
      divided_loans[x].append(loan)
      x += 1
      if x >= 10:
        x = 0
  for k,v in divided_loans.iteritems():
    storage.save_to_file(v, config.StorageFile.LC_LOAN_EXTENDED_DATA + "_sub_%d" % k)


def freshsplit():
  divided_loans = {}
  for i in list(range(0, 10)):
    divided_loans[i] = []
  loans = storage.load_from_file(config.StorageFile.LC_LOAN_EXTENDED_DATA)
  x = 0
  today = datetime.now()
  for loan in loans:
    loan['numInvestors'] = None
    td = today - datetime.strptime(loan['acceptD'].split('T')[0], "%Y-%m-%d")
    if loan['loanStatus'] != 'Fully Paid':
      divided_loans[x].append(loan)
      x += 1
      if x >= 10:
        x = 0
  for k,v in divided_loans.iteritems():
    storage.save_to_file(v, config.StorageFile.LC_LOAN_EXTENDED_DATA + "_sub_%d" % k)


def merge():
  loan_hash = {}
  for k in list(range(0, 10)):
    loans = storage.load_from_file(config.StorageFile.LC_LOAN_EXTENDED_DATA + "_sub_%d" % k)
    for loan in loans:
      loan_hash[ loan['id'] ] = loan
  loans = storage.load_from_file(config.StorageFile.LC_LOAN_EXTENDED_DATA)
  for i in xrange(len(loans)):
    loan_id = loans[i]['id']
    if loan_hash.get(loan_id) == None:
      continue
    if loan_hash[loan_id].get('numInvestors') == None:
      continue
    loans[i]['numInvestors'] = loan_hash[loan_id]['numInvestors']
    loans[i]['loanStatus'] = loan_hash[loan_id]['loanStatus']
  storage.save_to_file(loans, config.StorageFile.LC_LOAN_EXTENDED_DATA)

def stats():
  loans = storage.load_from_file(config.StorageFile.LC_LOAN_EXTENDED_DATA)
  today = datetime.now()
  c = 0
  cc = 0
  stats = defaultdict(lambda: 0)
  stats_by_grade = {}
  for grade in grade_list:
    stats_by_grade[grade] = defaultdict(lambda: 0)
  for loan in loans:
    grade = loan['grade']
    stats[loan['loanStatus']] += 1
    stats_by_grade[grade][loan['loanStatus']] += 1
    if loan.get('numInvestors') != None:
      c += 1
    td = today - datetime.strptime(loan['acceptD'].split('T')[0], "%Y-%m-%d")
    if td.days >= 365 and loan['loanStatus'] == 'Current':
      cc += 1
  print "Total %d loans in %s" % (len(loans), config.StorageFile.LC_LOAN_EXTENDED_DATA)
  print "%d loans updated" % c
  print "%d loans that should be updated" % cc
  print "%d loans remaining" % (cc - c)
  print stats
  for grade in grade_list:
    print "grade = " + grade
    print stats_by_grade[grade]

def substats():
  total = 0
  processed = 0
  stats = defaultdict(lambda: 0)
  stats_by_grade = {}
  for grade in grade_list:
    stats_by_grade[grade] = defaultdict(lambda: 0)
  for k in list(range(0, 10)):
    loans = storage.load_from_file(config.StorageFile.LC_LOAN_EXTENDED_DATA + "_sub_%d" % k)
    total += len(loans)
    for loan in loans:
      grade = loan['grade']
      stats[loan['loanStatus']] += 1
      stats_by_grade[grade][loan['loanStatus']] += 1
      if loan.get('numInvestors') != None:
        processed += 1
  print "Total %d loans in splited files" % total
  print "%d loans updated" % processed
  print stats
  for grade in grade_list:
    print "grade = " + grade
    print stats_by_grade[grade]

def main(argv):
  if len(argv) != 2:
    print_usage()
    return
  if argv[1] == 'split':
    split()
  elif argv[1] == 'freshsplit':
    freshsplit()
  elif argv[1] == 'merge':
    merge()
  elif argv[1] == 'stats':
    stats()
  elif argv[1] == 'substats':
    substats()


if __name__ == "__main__":
  main(sys.argv)
