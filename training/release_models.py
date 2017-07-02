import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import storage
from utils import config
from utils import predict

from sklearn.externals import joblib

release_grades = ['A', 'B', 'C', 'D', 'E', 'F']
command_map = {
  'b': 'batch',
  's': 'single'
}

def release_models(grade, models):
  p = config.StorageProductionFile
  filename_suffix = '_grade_' + grade

  filename = p.LC_extra_tree_model + filename_suffix
  joblib.dump(models['extra_tree'], filename)
  print "Saved %s" % filename

  filename = p.LC_random_forest_model + filename_suffix
  joblib.dump(models['random_forest'], filename)
  print "Saved %s" % filename

  filename = p.LC_adaptive_boosting_model + filename_suffix
  joblib.dump(models['adaptive_boosting'], filename)
  print "Saved %s" % filename

  filename = p.LC_gradient_boosting_model + filename_suffix
  joblib.dump(models['gradient_boosting'], filename)
  print "Saved %s" % filename


def main(argv):
  models_per_grade = predict.load_models_per_grade(release_grades)
  models_batch = predict.load_models()

  for grade in release_grades:
    print "Grade: %s -- Batch model (b) or Single model (s):" % grade
    cmd = ''
    while cmd not in command_map.keys():
      cmd = sys.stdin.readline().strip()
      if cmd not in command_map.keys():
        print "Enter one of %s for Grade %s" % (str(command_map.keys()), grade)
    if command_map[cmd] == 'batch':
      print "relase batch models"
      release_models(grade, models_batch)
    else:
      print "relase per grade models"
      release_models(grade, models_per_grade[grade])
    print


if __name__ == "__main__":
  main(sys.argv)
