import config
from feature_processing import feature

from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.externals import joblib


def load_models():
  models = {}
  models['extra_tree'] = joblib.load(config.StorageFile.LC_extra_tree_model)
  models['random_forest'] = joblib.load(config.StorageFile.LC_random_forest_model)
  models['adaptive_boosting'] = joblib.load(config.StorageFile.LC_adaptive_boosting_model)
  models['gradient_boosting'] = joblib.load(config.StorageFile.LC_gradient_boosting_model)
  return models


def load_models_per_grade(grades_for_prediction, production=False):
  if production == True:
    p = config.StorageProductionFile
  else:
    p = config.StorageFile

  models = {}
  for grade in grades_for_prediction:
    models[grade] = {}
    models[grade]['extra_tree'] = joblib.load(p.LC_extra_tree_model + '_grade_' + grade)
    models[grade]['random_forest'] = joblib.load(p.LC_random_forest_model + '_grade_' + grade)
    models[grade]['adaptive_boosting'] = joblib.load(p.LC_adaptive_boosting_model + '_grade_' + grade)
    models[grade]['gradient_boosting'] = joblib.load(p.LC_gradient_boosting_model + '_grade_' + grade)
  return models


def ensemble_prediction(loan, models):
  grade = loan['grade']
  if models.get(grade) is None:
    return False
  features = feature.get_features(loan)
  feature.validate(features)
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
