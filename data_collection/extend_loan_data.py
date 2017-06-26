import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import *
from utils import scraper
from datetime import datetime

def main(argv):
  filename = config.StorageFile.LC_LOAN_EXTENDED_DATA
  if len(argv) == 2:
     file_id = int(argv[1])
     filename = config.StorageFile.LC_LOAN_EXTENDED_DATA + "_sub_%d" % file_id
  print "Load data from %s" % filename

  loans = storage.load_from_file(filename)
  session = lending_club.get_web_login_session()
  today = datetime.now()
  c = 0
  processed = 0
  total = len(loans)
  for i in xrange(len(loans)):
    processed += 1
    if loans[i].get('numInvestors') != None:
      continue
    td = today - datetime.strptime(loans[i]['acceptD'].split('T')[0], "%Y-%m-%d")
    if td.days >= 365 and loans[i]['loanStatus'] == 'Current':
      htmls = lending_club.get_purchased_loan_listings_in_html([ loans[i]['id'] ], session)
      if htmls[0].find('An Error Has Occurred') > 0:
        print "Failed to fetch loan id %d" % loans[i]['id']
        continue
      web_loan = scraper.fetch_loan_detail_from_html(htmls[0])
      loans[i]['numInvestors'] = web_loan['numInvestors']
      loans[i]['loanStatus'] = web_loan['loanStatus']
      c += 1
    if c >= 50:
      c = 0
      now = datetime.now()
      storage.save_to_file(loans, filename)
      print "Save %d loans to %s took %d seconds -- %4.1f%% processed" % (
        len(loans),
        filename,
        (datetime.now() - now).seconds,
        processed * 100.0 / total
      )
  storage.save_to_file(loans, filename)

if __name__ == "__main__":
  main(sys.argv)
