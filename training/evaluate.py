import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import storage
from utils import config
from utils import predict

from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.externals import joblib

class GlobalV:
  benchmark = 1

def print_training_data_stats(lc_data):
  tot = sum(lc_data['testing']['targets'])
  num = len(lc_data['testing']['targets'])
  GlobalV.benchmark = (num - tot) * 1.0 / num + 0.01
  print '\t\ttesting targets: %d positve, %d negative' % (tot, num - tot)
  print '%20s:\t  actual default rate: %f on %6d' % ('Testing set', GlobalV.benchmark, num)

def print_predict_results(predict_targets, lc_data, algo_name):
  wrong_predictions = []
  correct_0 = 0
  correct_1 = 0
  for i in list(range(0, len(predict_targets))):
    if predict_targets[i] != lc_data['testing']['targets'][i]:
      wrong_predictions.append(predict_targets[i])
    else:
      if lc_data['testing']['targets'][i] == 0:
        correct_0 += 1
      else:
        correct_1 += 1
  actual_0 = len(lc_data['testing']['targets']) - sum(lc_data['testing']['targets'])
  actual_1 = sum(lc_data['testing']['targets'])
  prediction_0 = len(predict_targets) - sum(predict_targets)
  prediction_1 = sum(predict_targets)
  # print "%s prediction: %d positve, %d negative" % (
  #   algo_name, prediction_1, prediction_0)
  # print "%s correct prediction: %d positve, %d negative" % (
  #   algo_name, correct_1, correct_0)
  if prediction_1 == 0:
    return
  expected_default_rate = (actual_0 - correct_0) * 1.0 / prediction_1
  print "%20s:\texpected default rate: %f on %6d,\t %2.2f%%" % (
    algo_name,
    expected_default_rate,
    prediction_1,
    (GlobalV.benchmark - expected_default_rate) * 100.0 / GlobalV.benchmark
  )


def main(argv):
  lc_super_data = storage.load_from_file(config.StorageFile.model_evaluating_file)

  if mode == 'batch':
    clf = {}
    for grade in lc_super_data.keys():
      clf[grade] = predict.load_models()
  else:
    clf = predict.load_models_per_grade(lc_super_data.keys())

  for grade in sorted(lc_super_data.keys()):
    lc_data = lc_super_data[grade]
    X_test = lc_data['testing']['data']
    Y_test = lc_data['testing']['targets']

    print "Grade %s" % grade
    print_training_data_stats(lc_data)

    times = 1
    for i in xrange(times):
      predict_targets_extra_tree = clf[grade]['extra_tree'].predict(X_test)
      print_predict_results(predict_targets_extra_tree, lc_data, 'extra_tree')

    for i in xrange(times):
      predict_targets_random_forest = clf[grade]['random_forest'].predict(X_test)
      print_predict_results(predict_targets_random_forest, lc_data, 'random_forest')

    for i in xrange(times):
      predict_targets_adaptive_boosting = clf[grade]['adaptive_boosting'].predict(X_test)
      print_predict_results(predict_targets_adaptive_boosting, lc_data, 'adaptive_boosting')

    for i in xrange(times):
      predict_targets_gradient_boosting = clf[grade]['gradient_boosting'].predict(X_test)
      print_predict_results(predict_targets_gradient_boosting, lc_data, 'gradient_boosting')

    predict_targets_combined = []
    for i in xrange(len(predict_targets_gradient_boosting)):
      predict_targets_combined.append(
        predict_targets_random_forest[i] &
        predict_targets_adaptive_boosting[i] &
        predict_targets_gradient_boosting[i] &
        predict_targets_extra_tree[i]
      )
    print_predict_results(predict_targets_combined, lc_data, 'combined everything')

    predict_targets_combined_2 = []
    for i in xrange(len(predict_targets_gradient_boosting)):
      predict_targets_combined_2.append(
        predict_targets_random_forest[i] &
        predict_targets_adaptive_boosting[i] &
        predict_targets_gradient_boosting[i]
      )
    print_predict_results(predict_targets_combined_2, lc_data, 'combined top 3')
    print

if __name__ == "__main__":
  mode = ''
  if len(sys.argv) == 2 and sys.argv[1] == 'batch':
    mode = 'batch'
  main(mode)
