import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import *
from feature_processing import feature

from collections import defaultdict
import random
import os
from datetime import datetime

bidding_grades = {
  'A' : 1,
  'B' : 1,
  'C' : 1,
  'D' : 1,
  'E' : 1,
  'F' : 1
}
purchase_accounts = ['yimeng', 'gang']
max_spending = 200
max_num_notes_per_grade = 3
purchase_unit = 25


def filter_bidded_loans(loans):
  bidded_loan_ids = []
  bidded_loans = storage.load_from_file(config.StorageFile.LC_bidded_loans_file)
  for loan in bidded_loans:
    bidded_loan_ids.append(loan['id'])

  filtered_loans = []
  for loan in loans:
    if not loan['id'] in bidded_loan_ids:
      filtered_loans.append(loan)
  return filtered_loans


def get_bid_results(avail_loans):
  models = predict.load_models_per_grade(bidding_grades.keys(), production=True)
  bid_loans = []
  for loan in avail_loans:
    if predict.ensemble_prediction(loan, models):
      bid_loans.append(loan)
  return bid_loans


def get_stats(loans, key = 'grade'):
  stats = defaultdict(lambda: 0)
  for loan in loans:
    stats[loan[key]] += 1
  return stats


def prepare_loans_for_purchase(loans):
  loans_for_purchase = {}
  for grade in bidding_grades.keys():
    loans_for_purchase[grade] = []
  for loan in loans:
    grade = loan['grade']
    loans_for_purchase[grade].append(loan)
  for grade in bidding_grades.keys():
    random.shuffle(loans_for_purchase[grade])
  return loans_for_purchase


def print_loan_summary(avail_loans, bid_loans, key = 'grade'):
  orig_stats = get_stats(avail_loans, key)
  bid_stats = get_stats(bid_loans, key)
  print "summary:"
  print orig_stats
  print bid_stats


def purchase_loans(loans):
  loans_for_purchase = prepare_loans_for_purchase(loans)
  submited_loans = []
  for account_name in purchase_accounts:
    config.account_name = account_name
    loans_to_submit = []
    available_cash = min(max_spending, lending_club.get_available_cash())
    if available_cash < purchase_unit:
      continue
    used_cash = 0
    num_purchased_notes = defaultdict(lambda: 0)
    while used_cash + purchase_unit <= available_cash:
      previous_used_cash = used_cash
      for grade in sorted(bidding_grades.keys()):
        num = bidding_grades[grade]
        for i in xrange(num):
          if num_purchased_notes[grade] >= max_num_notes_per_grade:
            continue
          if len(loans_for_purchase[grade]) == 0:
            continue
          loan = loans_for_purchase[grade].pop()
          loans_to_submit.append(loan)
          num_purchased_notes[grade] += 1
          submited_loans.append(loan)
          used_cash += purchase_unit
          if used_cash + purchase_unit > available_cash:
            break
        if used_cash + purchase_unit > available_cash:
          break
      if previous_used_cash >= used_cash: # meaning no more notes to purchased in the for loop
        break
    result = lending_club.submit_order(loans_to_submit, purchase_unit)
  save_submited_loans_to_files(submited_loans)
  return submited_loans


def save_submited_loans_to_files(new_loans):
  saved_loan_ids = []
  saved_loans = storage.load_from_file(config.StorageFile.LC_bidded_loans_file)
  for loan in saved_loans:
    saved_loan_ids.append(loan['id'])

  for loan in new_loans:
    if not loan['id'] in saved_loan_ids:
      saved_loans.append(loan)

  storage.save_to_file(saved_loans, config.StorageFile.LC_bidded_loans_file)


def save_prediction_results(avail_loans, bid_loans):
  record = storage.load_from_file(config.StorageFile.LC_predicted_loans_ids)
  good_ids = set(record['good'])
  bad_ids = set(record['bad'])
  bid_ids = []
  for loan in bid_loans:
    bid_ids.append(loan['id'])
  for loan in avail_loans:
    loan_id = loan['id']
    if loan_id in bid_ids:
      good_ids.add(loan_id)
    else:
      bad_ids.add(loan_id)
  record['good'] = list(good_ids)
  record['bad'] = list(bad_ids)
  storage.save_to_file(record, config.StorageFile.LC_predicted_loans_ids)


def action():
  avail_loans = lending_club.get_available_loan_listings()
  avail_loans = filter_bidded_loans(avail_loans)
  bid_loans = get_bid_results(avail_loans)
  save_prediction_results(avail_loans, bid_loans)
  print_loan_summary(avail_loans, bid_loans)
  purchased_loans = purchase_loans(bid_loans)
  stats = get_stats(purchased_loans)
  print "Purchased Summary:"
  print stats


def simulation():
  print "This is a simulation:"
  avail_loans = lending_club.get_available_loan_listings()
  record = storage.load_from_file(config.StorageFile.LC_predicted_loans_ids)
  tracked_ids = set(record['good'] + record['bad'])
  unseen = 0
  total_avail = len(avail_loans)
  for loan in avail_loans:
    if not loan['id'] in tracked_ids:
      unseen += 1
  print "Unseen loan percentage: %4.1f%%" % (unseen * 100.0 / total_avail)
  print

  avail_loans = filter_bidded_loans(avail_loans)
  bid_loans = get_bid_results(avail_loans)
  print_loan_summary(avail_loans, bid_loans)
  print "Unseen loan percentage: %4.1f%%" % (unseen * 100.0 / total_avail)


def print_model_release_time():
  filename = config.StorageProductionFile.LC_gradient_boosting_model + '_grade_C'
  timestamp = os.path.getmtime(filename)
  d = datetime.fromtimestamp(timestamp)
  print
  print "Model release time:\t%s" % str(d)


def main(argv):
  if len(argv) == 2 and argv[1].lower() == 'action':
    action()
  else:
    simulation()
  print_model_release_time()
  print "Current Time: \t\t%s" % str(datetime.now())
  print

if __name__ == "__main__":
  main(sys.argv)
