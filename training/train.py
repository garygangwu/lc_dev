import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import storage
from utils import config

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



def main(argv):
  lc_super_data = storage.load_from_file(config.StorageFile.model_training_file)
  for grade, lc_data in lc_super_data.iteritems():
    print
    print "Grade %s" % grade
    print_training_data_stats(lc_data)
    X, Y = lc_data['training']['data'], lc_data['training']['targets']
    X_test = lc_data['testing']['data']
    Y_test = lc_data['testing']['targets']

    #clf = svm.SVC(gamma=0.001, C=100., verbose=True)
    #clf.fit(X, Y)
    #predict_targets = clf.predict(X_test)
    #print_predict_results(predict_targets, lc_data, 'SVC standard')

    #clf = svm.SVC()
    #clf.set_params(kernel='linear').fit(X, y)
    #predict_targets = clf.predict(X_test)
    #print_predict_results(predict_targets, lc_data, 'SVC linear')

    # clf_svm = svm.SVC()
    # clf_svm.set_params(kernel='rbf').fit(X, Y)
    # predict_targets_svm = clf_svm.predict(X_test)
    # print_predict_results(predict_targets_svm, lc_data, 'SVC rbf')

    clf_extra_tree = ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
    clf_extra_tree.fit(X, Y)
    predict_targets_extra_tree = clf_extra_tree.predict(X_test)
    print_predict_results(predict_targets_extra_tree, lc_data, 'extra_tree')
    joblib.dump(clf_extra_tree, config.StorageFile.LC_extra_tree_model + '_grade_' + grade)

    clf_forest = RandomForestClassifier(n_estimators=10, verbose=False)
    clf_forest.fit(X, Y)
    predict_targets_forest = clf_forest.predict(X_test)
    print_predict_results(predict_targets_forest, lc_data, 'Random Forest')
    joblib.dump(clf_forest, config.StorageFile.LC_random_forest_model + '_grade_' + grade)

    clf_adaptive = AdaBoostClassifier(n_estimators=100)
    scores = cross_val_score(clf_adaptive, X, Y)
    #print scores.mean()
    clf_adaptive.fit(X, Y)
    predict_targets_adaptive = clf_adaptive.predict(X_test)
    print_predict_results(predict_targets_adaptive, lc_data, 'AdaBoost')
    joblib.dump(clf_adaptive, config.StorageFile.LC_adaptive_boosting_model + '_grade_' + grade)

    clf_gradient = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
    clf_gradient.fit(X, Y)
    predict_targets_gradient = clf_gradient.predict(X_test)
    print_predict_results(predict_targets_gradient, lc_data, 'Gradient Boosting')
    #print clf_gradient.score(X, Y)
    #print clf_gradient.score(X_test, Y_test)
    joblib.dump(clf_gradient, config.StorageFile.LC_gradient_boosting_model + '_grade_' + grade)

    predict_targets_combined = []
    for i in xrange(len(predict_targets_gradient)):
      predict_targets_combined.append(
        predict_targets_forest[i] &
        predict_targets_adaptive[i] &
        predict_targets_gradient[i] &
        predict_targets_extra_tree[i]
      )
    print_predict_results(predict_targets_combined, lc_data, 'combined all')

    predict_targets_combined_2 = []
    for i in xrange(len(predict_targets_gradient)):
      predict_targets_combined_2.append(
        predict_targets_forest[i] &
        predict_targets_adaptive[i] &
        predict_targets_gradient[i]
      )
    print_predict_results(predict_targets_combined_2, lc_data, 'combined top 3')

if __name__ == "__main__":
  main(sys.argv)
