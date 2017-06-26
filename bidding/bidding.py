import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import *
from feature_processing import feature

from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.externals import joblib

from collections import defaultdict
import random

bidding_grades = {
  'A' : 1,
  'B' : 1,
  'C' : 1,
  'D' : 1,
  'E' : 1
}
purchase_accounts = ['gang', 'yimeng']
max_spending = 250
purchase_unit = 25

def load_models():
  models = {}
  for grade in bidding_grades.keys():
    models[grade] = {}
    models[grade]['extra_tree'] = joblib.load(config.StorageFile.LC_extra_tree_model + '_grade_' + grade)
    models[grade]['random_forest'] = joblib.load(config.StorageFile.LC_random_forest_model + '_grade_' + grade)
    models[grade]['adaptive_boosting'] = joblib.load(config.StorageFile.LC_adaptive_boosting_model + '_grade_' + grade)
    models[grade]['gradient_boosting'] = joblib.load(config.StorageFile.LC_gradient_boosting_model + '_grade_' + grade)
  return models


def bid(loan, models):
  grade = loan['grade']
  if not grade in bidding_grades.keys():
    return False
  features = feature.get_features(loan)
  decision = {}
  X = [ features ]
  final = 1
  for k, clf in models[grade].iteritems():
    result = clf.predict(X)
    decision[k] = result[0]
    final = final & result[0]
  print "%10d: subgrade %s, intRate %4.1f%%, purpose %25s, %d, decision %s" % (
    loan['id'],
    loan['subGrade'],
    loan['intRate'],
    loan['purpose'],
    final,
    str(decision)
  )
  return final == 1


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
  models = load_models()
  bid_loans = []
  for loan in avail_loans:
    if bid(loan, models):
      bid_loans.append(loan)
  return bid_loans


def get_stats(loans):
  stats = defaultdict(lambda: 0)
  for loan in loans:
    stats[loan['grade']] += 1
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


def print_loan_summary(avail_loans, bid_loans):
  orig_stats = get_stats(avail_loans)
  bid_stats = get_stats(bid_loans)
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
    while used_cash < available_cash:
      for grade, num in bidding_grades.iteritems():
        for i in xrange(num):
          loan = loans_for_purchase[grade].pop()
          loans_to_submit.append(loan)
          submited_loans.append(loan)
          used_cash += purchase_unit
          if used_cash >= available_cash:
            break
        if used_cash >= available_cash:
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
  avail_loans = filter_bidded_loans(avail_loans)
  bid_loans = get_bid_results(avail_loans)
  print_loan_summary(avail_loans, bid_loans)


def main(argv):
  if len(argv) == 2 and argv[1].lower() == 'action':
    action()
  else:
    simulation()

if __name__ == "__main__":
  main(sys.argv)
