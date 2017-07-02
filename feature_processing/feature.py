from datetime import datetime
import enchant

class Conf:
  loan_term_feature_map = {
    36: [1, 0],
    60: [0, 1]
  }

  loan_purpose_feature_map = {
    'credit_card'         : [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'debt_consolidation'  : [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'home_improvement'    : [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'major_purchase'      : [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'small_business'      : [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'medical'             : [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    'car'                 : [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    'vacation'            : [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    'other'               : [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    'moving'              : [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    'house'               : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    'renewable_energy'    : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    'wedding'             : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    'educational'         : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  }

  home_ownership_feature_map = {
    'RENT'    : [1, 0, 0, 0],
    'MORTGAGE': [0, 1, 0, 0],
    'OWN'     : [0, 0, 1, 0],
    'UNKNOWN' : [0, 0, 0, 1]
  }

  is_income_verified_feature_map = {
    'VERIFIED'          : [1, 0, 0],
    'SOURCE_VERIFIED'   : [0, 1, 0],
    'NOT_VERIFIED'      : [0, 0, 1]
  }

  application_type_feature_map = {
    'INDIVIDUAL'  : [1, 0, 0],
    'JOINT'       : [0, 1, 0],
    'DIRECT_PAY'  : [0, 0, 1]
  }

  feature_method_map = {
    'loan_grade': 'get_loan_grade',
    'loan_amount': 'get_loan_amount',
    'loan_term': 'get_loan_term',
    'interest_rate': 'get_interest_rate',
    'loan_purpose': 'get_loan_purpose',
    'home_ownership': 'get_home_ownership',
    'employment_length': 'get_employment_length',
    'employment_title': 'get_employment_title_features',
    'annual_income': 'get_annual_income',
    'delinquency': 'get_delinquency_features',
    'public_record': 'get_public_record_features',
    'major_derogatory': 'get_major_derogatory',
    'credit_score': 'get_credit_score_features',
    'credit_account': 'get_credit_account_features',
    'excluding_medical': 'get_excluding_medical',
    'open_rv': 'get_rv_features',
    'num': 'get_num_related_features',
    'il': 'get_open_il_features',
    'tot': 'get_tot_features',
    'tl': 'get_tl_features',
    'bc': 'get_bc_features',
    'app_type': 'get_application_type',
    'rev': 'get_rev_features',
#    'location': 'get_location_features',
    'balance': 'get_bal_features',
    'tax': 'get_tax_features'
  }


def idx(m, key, default_value):
  if m.get(key) == None:
    return default_value
  return m[key]


def print_feature_name_idx(loan):
  idx = 0
  for key, method in Conf.feature_method_map.iteritems():
    values = globals()[method](loan)
    print "%s: %d -- %d" % (method, idx, idx + len(values) - 1)
    idx += len(values)


def idx_to_feature_map(loan):
  feature_map = {}
  idx = 0
  for key, method in Conf.feature_method_map.iteritems():
    values = globals()[method](loan)
    i = idx
    while i < idx + len(values):
      feature_map[i] = {
        'name': method,
        'start': idx,
        'end': idx + len(values) - 1
      }
      i += 1
    idx += len(values)
  return feature_map


def validate(features):
  i = 0
  for feature in features:
    if feature is None:
      raise Exception('bad value at idx: %d' % i)
    if not isinstance(feature, int) and not isinstance(feature, float):
      raise Exception('bad value at idx: %d -- value: %s' % (i, str(feature)))
    i += 1


def get_features(loan):
  features = []
  for key, method in Conf.feature_method_map.iteritems():
    values = globals()[method](loan)
    features += values
  return features


def get_loan_grade(loan):
  grade = loan['subGrade']
  sub_grade = float(grade[1:]) * 10 / 6.0
  if sub_grade >= 10:
    raise Exception("bad loan grade %s" % grade)
  value = (ord(grade[0].upper()) - ord('A')) * 10 + sub_grade
  return [ value ]


def get_loan_amount(loan):
  return [ loan['loanAmount'] ]


def get_loan_term(loan):
  if Conf.loan_term_feature_map.get(loan['term']) is None:
    raise Exception("Unrecoginzed loan term : %d" % loan['term'])
  return Conf.loan_term_feature_map[ loan['term'] ]


def get_interest_rate(loan):
  return [ loan['intRate'] ]


def get_loan_purpose(loan):
  if Conf.loan_purpose_feature_map.get(loan['purpose']) is None:
    raise Exception("Unrecoginzed loan purpose : %s" % loan['purpose'])
  return Conf.loan_purpose_feature_map[ loan['purpose'] ]


def get_home_ownership(loan):
  home_ownership = loan['homeOwnership'].upper().strip()
  if Conf.home_ownership_feature_map.get(home_ownership) is None:
    home_ownership = 'UNKNOWN'
  return Conf.home_ownership_feature_map[home_ownership]


def get_employment_length(loan):
  return [
    idx(loan, 'empLength', 0)
  ]


special_chars = set(['\\', '/', '&', '(', ')', '.', '-', ','])
def clean_up_title(title):
  ret = ''
  for i in xrange(len(title)):
    if title[i] in special_chars:
      ret += ' '
    else:
      ret += (title[i])
  return ret


dict_en = enchant.Dict("en_US")
valid_words = set(['admin', 'Admin', 'realtor', 'Realtor', 'DevOps', 'Fedex', 'PayPal', 'AutoTech', 'fulltime', 'Fulltime', 'Postdoc'])
def get_employment_title_features(loan):
  title = loan['empTitle'] or 'n/a'
  has_misspell_word = 0
  if title == 'n/a':
    with_title = 0
    num_words = 0
  else:
    title = clean_up_title(title)
    with_title = 1
    words = filter(lambda k: len(k) != 0, title.split(' '))
    num_words = len(words)
    for word in words:
      if len(word) > 4 and not word in valid_words and not dict_en.check(word):
        has_misspell_word = 1
  return [with_title, num_words, has_misspell_word]


def get_annual_income(loan):
  is_verified = loan['isIncV'].upper().strip()
  if Conf.is_income_verified_feature_map.get(is_verified) is None:
    raise Exception("Unrecoginzed status of verified income : %s" % is_verified)
  return [ idx(loan, 'annualInc', 0) ] + Conf.is_income_verified_feature_map[is_verified]


def get_delinquency_features(loan):
  return [
    loan['delinq2Yrs'],           # DELINQUENCIES_IN_LAST_2_YEARS
    loan['delinqAmnt'],           # DELINQUENT_AMOUNT
    loan['accNowDelinq'],         # ACCOUNTS_NOW_DELINQUENT
    idx(loan, 'mthsSinceLastDelinq', 480), # default for 480 months no delinquency
    idx(loan, 'mthsSinceRecentRevolDelinq', 480)
  ]


def get_public_record_features(loan):
  return [
    loan['pubRec'],
    idx(loan, 'mthsSinceLastRecord', -1)
  ]


def get_major_derogatory(loan):
  if loan['mthsSinceLastMajorDerog'] is not None:
    flag = 1
    months = loan['mthsSinceLastMajorDerog']
  else:
    flag = 0
    months = -1
  return [
    flag,
    months
  ]


def get_credit_score_features(loan):
  return [
    loan['ficoRangeLow'],   # FICO_RANGE_LOW
    loan['ficoRangeHigh'],  # FICO_RANGE_HIGH
    idx(loan, 'inqLast6Mths', 0),    # INQUIRIES_IN_LAST_6_MONTHS
    idx(loan, 'inqLast12m', 0),
    idx(loan, 'inqFi', 0),
    idx(loan, 'mthsSinceRecentInq', 0)
  ]


def get_credit_account_features(loan):
  # months between loan submit date and earliest credit line
  accept_date = datetime.strptime(loan['acceptD'].split('T')[0], "%Y-%m-%d")
  earliest_credit_date = datetime.strptime(loan['earliestCrLine'].split('T')[0], "%Y-%m-%d")
  td = accept_date - earliest_credit_date
  return [
    idx(loan, 'revolBal', 0),
    idx(loan, 'revolUtil', 0),  # REVOLVING_UTILIZATION
    loan['dti'],        # DEBT_TO_INCOME_RATIO
    td.days / 30,       # diff in months
    loan['openAcc'],    # OPEN_ACCOUNTS
    idx(loan, 'openAcc6m', 0),
    idx(loan, 'totalAcc', 0),   # TOTAL_ACCOUNTS
    idx(loan, 'mortAcc', 0),
    idx(loan, 'accOpenPast24Mths', 0),
    idx(loan, 'inqLast6Mths', 0),
    idx(loan, 'tot_hi_cred_lim', 0),
    idx(loan, 'allUtil', 0),
    idx(loan, 'totalIlHighCreditLimit', 0),
    idx(loan, 'chargeoffWithin12Mths', 0)
  ]


def get_excluding_medical(loan):
  return [ loan['collections12MthsExMed'] ]


def get_rv_features(loan):
  return [
    idx(loan, 'openRv12m', -1),
    idx(loan, 'openRv24m', -1)
  ]

def get_num_related_features(loan):
  return [
    idx(loan, 'numSats', 0),
    idx(loan, 'numIlTl', 0),
    idx(loan, 'numAcctsEver120Ppd', 0)
  ]

def get_open_il_features(loan):
  return [
    idx(loan, 'openIl6m', 0),
    idx(loan, 'openIl12m', 0),
    idx(loan, 'openIl24m', 0),
    idx(loan, 'iLUtil', 0),
    idx(loan, 'totalBalIl', 0),
    idx(loan, 'moSinOldIlAcct', 0)
  ]

def get_tot_features(loan):
  return [
    idx(loan, 'totCollAmt', 0),
    idx(loan, 'totCurBal', 0),
    idx(loan, 'totalRevHiLim', 0)
  ]

def get_tl_features(loan):
  return [
    idx(loan, 'numTlOpPast12m', 0),
    idx(loan, 'numTl90gDpd24m', 0),
    idx(loan, 'numTl30dpd', 0),
    idx(loan, 'numTl120dpd2m', 0),
    idx(loan, 'moSinOldRevTlOp', 0),
    idx(loan, 'pct_tl_nvr_dlq', 0),
    idx(loan, 'totalCuTl', 0),
    idx(loan, 'moSinRcntTl', 0)
  ]

def get_bc_features(loan):
  return [
    idx(loan, 'maxBalBc', 0),
    idx(loan, 'mthsSinceRecentBc', 0),
    idx(loan, 'mthsSinceRecentBcDlq', 480),
    idx(loan, 'numActvBcTl', 0),
    idx(loan, 'numBcSats', 0),
    idx(loan, 'numBcTl', 0),
    idx(loan, 'percentBcGt75', 0),
    idx(loan, 'bcUtil', 0),
    idx(loan, 'bcOpenToBuy', 0)
  ]

def get_application_type(loan):
  return Conf.application_type_feature_map[loan['applicationType'].upper()]

def get_rev_features(loan):
  return [
    idx(loan, 'numRevAccts', 0),
    idx(loan, 'numRevTlBalGt0', 0),
    idx(loan, 'moSinRcntRevTlOp', 0)
  ]

def get_location_features(loan):
  return [
    loan['addrState'].upper()
  ]

def get_bal_features(loan):
  return [
    idx(loan, 'totalBalExMort', 0),
    idx(loan, 'avgCurBal', 0)
  ]

def get_tax_features(loan):
  return [
    idx(loan, 'taxLiens', 0)
  ]
