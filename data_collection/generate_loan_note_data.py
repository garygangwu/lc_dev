import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import *


def main(argv):
  html_to_loan = len(argv) <= 1 or argv[1].lower() == 'loans'
  pull_notes = len(argv) <= 1 or argv[1].lower() == 'notes'

  if html_to_loan:
    htmls = storage.load_from_file(config.StorageFile.loan_detail_file_in_htmls)
    loans = lending_club.get_loans_from_htmls(htmls.values())
    storage.save_to_file(loans, config.StorageFile.purchased_loan_detail_file)
    print 'Saved purchased loans to %s' % config.StorageFile.purchased_loan_detail_file

  if pull_notes:
    account_names = ['gang', 'yimeng']
    notes = []
    for name in account_names:
      notes += lending_club.get_purchased_notes_detail_statuses()
    storage.save_to_file(notes, config.StorageFile.purchased_note_status_file)
    print "Saved notes' statuses to %s" % config.StorageFile.purchased_note_status_file


if __name__ == "__main__":
  main(sys.argv)
