import csv
import glob
from web_scraper import *

tracking_quarters = [
  ('2017-Q1', ['2017-01', '2017-02', '2017-03']),
  ('2017-Q2', ['2017-04', '2017-05', '2017-06']),
  ('2017-Q3', ['2017-07', '2017-08', '2017-09']),
  ('2017-Q4', ['2017-10', '2017-11', '2017-12']),
  ('2018-Q1', ['2018-01', '2018-02', '2018-03'])
]

def append_loans(filename, loans, excluded_loans):
  csv_file = open(filename, 'r')
  reader = csv.DictReader(csv_file)
  for row in reader:
    loan_id = row['loan_id']
    if loan_id in excluded_loans:
      continue
    loan_amount = row['loan_amount']
    loans[loan_id] = int(loan_amount)
  return loans

def unique_loans(months, excluded_loans):
  loans = {}
  for month in months:
    filenames = glob.glob(SecStaticData.quarter_raw_sec_fold + month + '/*.csv')
    for filename in filenames:
      loans = append_loans(filename, loans, excluded_loans)
  return loans

def dump_quarter_raw_summary(quarter, loans):
  filename = SecStaticData.quarter_raw_sec_fold + quarter + '_raw_loans.csv'
  fieldnames = ['loan_id', 'loan_amount']
  csvfile = open(filename, 'w')
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
  for loan_id, loan_amount in loans.iteritems():
    writer.writerow({'loan_id': loan_id, 'loan_amount': loan_amount})
  print "Dumpped loan data to " + filename 

previous_quarter = {}
for item in tracking_quarters:
  quarter, months = item
  quarter_loans = unique_loans(months, previous_quarter)
  previous_quarter = quarter_loans.copy()
  print quarter
  print len(quarter_loans)
  print sum(v for v in quarter_loans.values())
  dump_quarter_raw_summary(quarter, quarter_loans)
