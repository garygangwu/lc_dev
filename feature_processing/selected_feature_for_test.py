import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import storage
from utils import config
import feature
from datetime import datetime
import random

bad_status_list = ['Late (16-30 days)', 'Late (31-120 days)', 'Default', 'Charged Off']
good_status_list = ['Current', 'Fully Paid']
valid_grades = ['A', 'B', 'C', 'D', 'E']
valid_status_list = bad_status_list + good_status_list

def need_to_drop(loan):
  if not loan['loanStatus'] in ['Current', 'Fully Paid']:
    return True

  if not loan['grade'] in valid_grades:
    return True

  if loan['loanStatus'] == 'Current':
    if loan.get('numInvestors') is None:
      return True
    if loan['numInvestors'] < 10:
      return True

  date_str = loan['acceptD'].split('T')[0]
  issue_date = datetime.strptime(date_str, "%Y-%m-%d")
  dt = datetime.now() - issue_date
  if dt.days < 365 and loan['loanStatus'] == 'Current':
    return True # skip all fresh loans in the past X days

  return False


def print_training_data_stats(lc_super_data):
  for grade in valid_grades:
    lc_data = lc_super_data[grade]
    tot = sum(lc_data['testing']['targets'])
    num = len(lc_data['testing']['targets'])
    print 'Grade %s: testing targets: %d positve, %d negative, %f%%' % (
      grade, tot, num - tot, (num - tot)*100.0/num)


def main():
  lc_super_data = {}
  for grade in valid_grades:
    lc_super_data[grade] = {
      'training': { 'data': [], 'targets': [] },
      'testing' : { 'data': [], 'targets': [] }
    }
  train_data = storage.load_from_file(config.StorageFile.model_training_file)
  for grade, lc_data in train_data.iteritems():
    if not grade in valid_grades:
      continue
    for i in xrange(len(lc_data['testing']['targets'])):
      if lc_data['testing']['targets'][i] == 0:
        lc_super_data[grade]['testing']['targets'].append(0)
        lc_super_data[grade]['testing']['data'].append(lc_data['testing']['data'][i])
  print_training_data_stats(lc_super_data)

  loans = storage.load_from_file(config.StorageFile.LC_LOAN_EXTENDED_DATA)
  feature.print_feature_name_idx(loans[0])

  for loan in loans:
    if need_to_drop(loan):
      continue

    grade = loan['grade'].upper()
    if loan['loanStatus'] in good_status_list:
      target = 1
    elif loan['loanStatus'] in bad_status_list:
      target = 0
    else:
      raise Exception("bad loan status input: " + loan['loanStatus'])

    if target == 0:
      raise Exception("Not possible")

    features = feature.get_features(loan)
    feature.validate(features)

    if target == 1:
      if grade == 'A' and random.random() >= 0.02:
        continue
      if grade == 'B' and random.random() >= 0.04:
        continue
      if grade == 'C' and random.random() >= 0.05:
        continue
      if grade == 'D' and random.random() >= 0.1:
        continue
      if grade == 'E' and random.random() >= 0.1:
        continue

    lc_super_data[grade]['testing']['data'].append(features)
    lc_super_data[grade]['testing']['targets'].append(target)

  print_training_data_stats(lc_super_data)
  storage.save_to_file(lc_super_data, config.StorageFile.model_evaluating_file)
  print "Saved model training data to %s" % config.StorageFile.model_evaluating_file


if __name__ == "__main__":
  main()
