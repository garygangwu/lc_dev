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
valid_grades = ['A', 'B', 'C', 'D', 'E', 'F']
valid_status_list = bad_status_list + good_status_list

def need_to_drop(loan):
  if not loan['loanStatus'] in ['Current', 'Fully Paid', 'Late (31-120 days)', 'Default', 'Charged Off']:
    return True

  if not loan['grade'] in valid_grades:
    return True

  if loan['loanStatus'] == 'Current':
    if loan.get('numInvestors') is None:
      return True

    if loan['grade'] in ['A', 'B']:
      return True

    date_str = loan['acceptD'].split('T')[0]
    issue_date = datetime.strptime(date_str, "%Y-%m-%d")
    dt = datetime.now() - issue_date
    if dt.days < 365*1.5 and loan['loanStatus'] == 'Current':
      return True # skip all fresh loans in the past X days

    #if loan['numInvestors'] != 1:
    #  return True

  #date_str = note['issueDate'].split('.')[0]
  #issue_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
  #dt = datetime.now() - issue_date
  #if dt.days < 90:
  #  return True # skip all fresh notes in the past 90 days
  #if dt.days < 120 and note['loanStatus'] == 'Current':
  #  return True # ignore relative new notes

  #if note['grade'].upper() < 'B' and note['loanStatus'] == 'Current':
  #  return True

  return False


def print_training_data_stats(lc_super_data):
  for grade in valid_grades:
    lc_data = lc_super_data[grade]
    tot = sum(lc_data['training']['targets'])
    num = len(lc_data['training']['targets'])
    print 'Grade %s: training targets: %d positve, %d negative' % (grade, tot, num - tot)
    tot = sum(lc_data['testing']['targets'])
    num = len(lc_data['testing']['targets'])
    print 'Grade %s: testing targets: %d positve, %d negative' % (grade, tot, num - tot)


def main():
  lc_super_data = {}
  for grade in valid_grades:
    lc_super_data[grade] = {
      'training': { 'data': [], 'targets': [] },
      'testing' : { 'data': [], 'targets': [] }
    }

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

    features = feature.get_features(loan)
    feature.validate(features)

    if random.random() >= 0.1:
      key = 'training'
    else:
      key = 'testing'

    if target == 1:
      if grade == 'A' and random.random() >= 0.301:
        key = 'testing'
      if grade == 'B' and random.random() >= 0.706:
        key = 'testing'
      if grade == 'C' and random.random() >= 0.5:
        key = 'testing'
      if grade == 'D' and random.random() >= 0.8:
        key = 'testing'
      if grade == 'E' and random.random() >= 0.8:
        key = 'testing'

    lc_super_data[grade][key]['data'].append(features)
    lc_super_data[grade][key]['targets'].append(target)

  print_training_data_stats(lc_super_data)
  storage.save_to_file(lc_super_data, config.StorageFile.model_training_file)
  print "Saved model training data to %s" % config.StorageFile.model_training_file


if __name__ == "__main__":
  main()
