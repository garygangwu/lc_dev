from collections import defaultdict
import pprint

def print_per_key_stats(loans, key):
  stats = defaultdict(lambda: 0)
  for loan in loans:
    value = loan[key]
    if value == None:
      value = 'None'
    stats[str(value)] += 1
  pp = pprint.PrettyPrinter(indent=4)
  pp.pprint(stats)
