import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import *


def get_missing_html_loan_ids(html_map):
  notes = lending_club.get_purchased_notes_detail_statuses()
  loan_ids = []
  for note in notes:
    loan_id = note['loanId']
    if html_map.get(str(loan_id)) == None:
      loan_ids.append(loan_id)
  return loan_ids


def main(argv):
  account_names = ['gang', 'yimeng']
  html_map = storage.load_from_file(config.StorageFile.loan_detail_file_in_htmls)
  original_num_keys = len(html_map.keys())
  print 'loaded %s with %d keys' % (config.StorageFile.loan_detail_file_in_htmls, original_num_keys)

  i = 0
  for name in account_names:
    config.account_name = name
    loan_ids_to_fetch_html = get_missing_html_loan_ids(html_map)

    session = lending_club.get_web_login_session()

    for loan_id in loan_ids_to_fetch_html:
      htmls = lending_club.get_purchased_loan_listings_in_html([loan_id], session)
      html_map[str(loan_id)] = htmls[0]
      if i >= 100:
        i = 0
        storage.save_to_file(html_map, config.StorageFile.loan_detail_file_in_htmls)
        print 'Saving %s with %d keys' % (config.StorageFile.loan_detail_file_in_htmls, len(html_map.keys()))
      i += 1

  if original_num_keys != len(html_map.keys()):
    storage.save_to_file(html_map, config.StorageFile.loan_detail_file_in_htmls)
    print 'Saving %s with %d keys' % (config.StorageFile.loan_detail_file_in_htmls, len(html_map.keys()))

if __name__ == "__main__":
  main(sys.argv)
