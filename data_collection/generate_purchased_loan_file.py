import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import *

def main(argv):
  auto_portfolio_ids = [
    config.account_settings['gang']['portfolio_id'],
    config.account_settings['yimeng']['portfolio_id']
  ]
  notes = []
  for account_name in ['gang', 'yimeng']:
    config.account_name = account_name
    notes += lending_club.get_purchased_notes_detail_statuses()
  lc_puchased_loan_ids = {}
  auto_puchased_loan_ids = {}
  for note in notes:
    loan_id = note['loanId']
    portfolio_id = note['portfolioId']
    if portfolio_id in auto_portfolio_ids:
      auto_puchased_loan_ids[loan_id] = note['loanStatus']
    else:
      lc_puchased_loan_ids[loan_id] = note['loanStatus']

  loans = storage.load_from_file(config.StorageFile.LC_LOAN_EXTENDED_DATA)
  lc_puchased_loans = []
  auto_puchased_loas = []
  for loan in loans:
    loan_id = loan['id']
    if lc_puchased_loan_ids.get(loan_id) is not None:
      loan['loanStatus'] = lc_puchased_loan_ids[loan_id]
      lc_puchased_loans.append(loan)
    elif auto_puchased_loan_ids.get(loan_id) is not None:
      loan['loanStatus'] = auto_puchased_loan_ids[loan_id]
      auto_puchased_loas.append(loan)

  storage.save_to_file(lc_puchased_loans, config.StorageFile.LC_purchased_loans_file)
  print "Saved %d (out of %d) loans to %s" % (
    len(lc_puchased_loans),
    len(lc_puchased_loan_ids),
    config.StorageFile.LC_purchased_loans_file
  )
  storage.save_to_file(auto_puchased_loas, config.StorageFile.AUTO_purchased_loans_file)
  print "Saved %d (out of %d) loans to %s" % (
    len(auto_puchased_loas),
    len(auto_puchased_loan_ids),
    config.StorageFile.AUTO_purchased_loans_file
  )


if __name__ == "__main__":
  main(sys.argv)
