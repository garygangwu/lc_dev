import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import storage
from utils import config
from utils import predict
from feature_processing import feature

def get_feature_mapping():
  loan = storage.load_from_file(config.StorageFile.LC_bidded_loans_file)[0]
  feature_map = feature.idx_to_feature_map(loan)
  for i in sorted(feature_map.keys()):
    print "%3d: %s" % (i, str(feature_map[i]))
  return feature_map


def importance_comp(x, y):
  if x['value'] < y['value']:
    return -1
  elif x['value'] > y['value']:
    return 1
  else:
    return x['idx'] - y['idx']


def print_top_features(feature_importances, feature_map):
  importance_list = []
  for i in xrange(len(feature_importances)):
    importance_list.append({'idx': i, 'value': feature_importances[i]})
  importance_list = sorted(importance_list, cmp=importance_comp, reverse=True)
  for item in importance_list:
    idx = item['idx']
    print "\t\t%3d, %8.6f, %30s %2d-%2d" % (
      idx,
      item['value'],
      feature_map[idx]['name'],
      feature_map[idx]['start'],
      feature_map[idx]['end']
    )


def main():
  feature_map = get_feature_mapping()
  models = predict.load_models_per_grade(['A', 'B', 'C', 'D', 'E', 'F'], production=True)
  for grade in sorted(models.keys()):
    print "Grade %s:" % grade
    for name, clf in models[grade].iteritems():
      print "Grade %s -- %s" % (grade, name)
      print_top_features(clf.feature_importances_, feature_map)


if __name__ == "__main__":
  main()
