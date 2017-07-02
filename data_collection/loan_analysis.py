import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from collections import defaultdict
import pprint
import enchant
from feature_processing import feature


def print_per_key_stats(loans, key):
  stats = defaultdict(lambda: 0)
  for loan in loans:
    value = loan[key]
    if value == None:
      value = 'None'
    stats[str(value)] += 1
  pp = pprint.PrettyPrinter(indent=4)
  pp.pprint(stats)


def func_spell(loans):
  d = enchant.Dict("en_US")
  for loan in loans:
    results = feature.get_employment_title_features(loan)
    if results[2] == 1:
      print loan['empTitle']
