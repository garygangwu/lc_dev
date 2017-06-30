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

def init_training_data_stats(lc_data):
  tot = sum(lc_data['training']['targets'])
  num = len(lc_data['training']['targets'])
  print 'training targets: %d positve, %d negative' % (tot, num - tot)
  tot = sum(lc_data['testing']['targets'])
  num = len(lc_data['testing']['targets'])
  GlobalV.benchmark = (num - tot) * 1.0 / num
  print 'testing targets: %d positve, %d negative' % (tot, num - tot)
  print '%20s:\t  actual default rate: %f on %6d' % ('Testing set', GlobalV.benchmark, num)


def print_predict_results(predict_targets, lc_data, algo_name):
  #print predict_targets
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
  #print "%s #wrong_predictions : %d" % (algo_name, len(wrong_predictions))
  #print "  # false predicted 0 (lose opportunity): %d, # false predicted 1 (lose money): %d" % \
  #  (len(wrong_predictions) - sum(wrong_predictions), sum(wrong_predictions))


def fit_and_predict(lc_data, filename_suffix = ''):
  models = {}
  predict_targets = {}
  X, Y = lc_data['training']['data'], lc_data['training']['targets']
  X_test, Y_test = lc_data['testing']['data'], lc_data['testing']['targets']

  models['extra_tree'] = ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
  models['extra_tree'].fit(X, Y)
  predict_targets['extra_tree'] = models['extra_tree'].predict(X_test)
  joblib.dump(models['extra_tree'], config.StorageFile.LC_extra_tree_model + filename_suffix)

  models['random_forest'] = RandomForestClassifier(n_estimators=10, verbose=False)
  models['random_forest'].fit(X, Y)
  predict_targets['random_forest'] = models['random_forest'].predict(X_test)
  joblib.dump(models['random_forest'], config.StorageFile.LC_random_forest_model + filename_suffix)

  models['adaptive_boosting'] = AdaBoostClassifier(n_estimators=100)
  scores = cross_val_score(models['adaptive_boosting'], X, Y)
  models['adaptive_boosting'].fit(X, Y)
  predict_targets['adaptive_boosting'] = models['adaptive_boosting'].predict(X_test)
  joblib.dump(models['adaptive_boosting'], config.StorageFile.LC_adaptive_boosting_model + filename_suffix)

  models['gradient_boosting'] = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
  models['gradient_boosting'].fit(X, Y)
  predict_targets['gradient_boosting'] = models['gradient_boosting'].predict(X_test)
  joblib.dump(models['gradient_boosting'], config.StorageFile.LC_gradient_boosting_model + filename_suffix)

  generate_prediction_results(models, lc_data)


def generate_prediction_results(models, lc_data):
  init_training_data_stats(lc_data)
  X_test = lc_data['testing']['data']
  predict_targets = {}
  predict_targets['extra_tree'] = models['extra_tree'].predict(X_test)
  print_predict_results(predict_targets['extra_tree'], lc_data, 'extra_tree')
  predict_targets['random_forest'] = models['random_forest'].predict(X_test)
  print_predict_results(predict_targets['random_forest'], lc_data, 'Random Forest')
  predict_targets['adaptive_boosting'] = models['adaptive_boosting'].predict(X_test)
  print_predict_results(predict_targets['adaptive_boosting'], lc_data, 'Adaptive boosting')
  predict_targets['gradient_boosting'] = models['gradient_boosting'].predict(X_test)
  print_predict_results(predict_targets['gradient_boosting'], lc_data, 'Gradient Boosting')

  predict_targets['combine_all'] = []
  for i in xrange(len(predict_targets['gradient_boosting'])):
    predict_targets['combine_all'].append(
      predict_targets['extra_tree'][i] &
      predict_targets['random_forest'][i] &
      predict_targets['adaptive_boosting'][i] &
      predict_targets['gradient_boosting'][i]
    )
  print_predict_results(predict_targets['combine_all'], lc_data, 'combined all')

  predict_targets['combine_top_3'] = []
  for i in xrange(len(predict_targets['gradient_boosting'])):
    predict_targets['combine_top_3'].append(
      predict_targets['random_forest'][i] &
      predict_targets['adaptive_boosting'][i] &
      predict_targets['gradient_boosting'][i]
    )
  print_predict_results(predict_targets['combine_top_3'], lc_data, 'combined top 3')


def evaluate_batch_model_per_grade(lc_super_data):
  models = predict.load_models()
  for grade, lc_data in lc_super_data.iteritems():
    print
    print "Grade %s" % grade
    generate_prediction_results(models, lc_data)


def batch_train():
  lc_super_data = storage.load_from_file(config.StorageFile.model_training_file)
  merged_lc_data = {
    'training': { 'data': [], 'targets': [] },
    'testing' : { 'data': [], 'targets': [] }
  }
  for grade, lc_data in lc_super_data.iteritems():
    merged_lc_data['training']['data'] += lc_data['training']['data']
    merged_lc_data['training']['targets'] += lc_data['training']['targets']
    merged_lc_data['testing']['data'] += lc_data['testing']['data']
    merged_lc_data['testing']['targets'] += lc_data['testing']['targets']
  init_training_data_stats(merged_lc_data)
  fit_and_predict(merged_lc_data)
  evaluate_batch_model_per_grade(lc_super_data)


def train_per_grade():
  lc_super_data = storage.load_from_file(config.StorageFile.model_training_file)
  for grade, lc_data in lc_super_data.iteritems():
    print
    print "Grade %s" % grade
    init_training_data_stats(lc_data)
    predict_targets = fit_and_predict(lc_data, '_grade_' + grade)


def main(argv):
  if len(argv) <= 1:
    argv.append('default')

  if argv[1] == 'default':
    train_per_grade()
  elif argv[1] == 'batch':
    batch_train()

if __name__ == "__main__":
  main(sys.argv)
