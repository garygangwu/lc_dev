import sys
import os.path
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path + "/..")

from utils import *
import csv
from datetime import datetime
from collections import defaultdict

def convert_term(value):
  return int(value.split(' ')[0])

def convert_percentage(value):
  v = value.strip('%')
  if len(v) == 0:
    return 0.0
  return float(v)

def convert_emp_length(value):
  value = value.lower()
  if len(value) == 0 or value == 'n/a' or value == '< 1 year':
    return 0
  return int(value.split(' ')[0].strip('+')) * 12

def convert_emp_title(value):
  return unicode(value.decode('utf-8').strip())

def convert_verification_status(value):
  if len(value) == 0:
    return None
  return unicode(value.strip().upper().replace(' ', '_'))

def convert_month_year_date(value):
  return unicode(datetime.strptime(value.strip(), '%b-%Y').isoformat())

def convert_int_default(value):
  return convert_type_default(value, 'int')

def convert_float_default(value):
  return convert_type_default(value, 'float')

def convert_type_default(value, to_type):
  if len(value) == 0:
    return None
  return eval("%s(value)" % to_type)

loan_csv_header_to_key_map = {
  'id' : ('id', 'int'),
  'member_id' : ('', 'unicode'),
  'loan_amnt' : ('loanAmount', 'float'),
  'funded_amnt' : ('', 'str'),
  'funded_amnt_inv' : ('', 'str'),
  'term' : ('term', 'convert_term'),
  'int_rate' : ('intRate', 'convert_percentage'),
  'installment' : ('', 'str'),
  'grade' : ('grade', 'unicode'),
  'sub_grade' : ('subGrade', 'unicode'),
  'emp_title' : ('empTitle', 'convert_emp_title'),
  'emp_length' : ('empLength', 'convert_emp_length'),
  'home_ownership' : ('homeOwnership', 'unicode'),
  'annual_inc' : ('annualInc', 'convert_float_default'),
  'verification_status' : ('isIncV', 'convert_verification_status'),
  'issue_d' : ('acceptD', 'convert_month_year_date'),
  'loan_status': ('loanStatus', 'str'),
  'pymnt_plan' : ('', 'str'),
  'url' : ('', 'str'),
  'desc' : ('', 'str'),
  'purpose' : ('purpose', 'unicode'),
  'title' : ('', 'str'),
  'zip_code' : ('addrZip', 'unicode'),
  'addr_state' : ('addrState', 'unicode'),
  'dti' : ('dti', 'convert_float_default'),
  'delinq_2yrs' : ('delinq2Yrs', 'int'),
  'earliest_cr_line' : ('earliestCrLine', 'convert_month_year_date'),
  'fico_range_low' : ('ficoRangeLow', 'int'),
  'fico_range_high' : ('ficoRangeHigh', 'int'),
  'inq_last_6mths' : ('inqLast6Mths', 'convert_int_default'),
  'mths_since_last_delinq' : ('mthsSinceLastDelinq', 'convert_int_default'),
  'mths_since_last_record' : ('mthsSinceLastRecord', 'convert_int_default'),
  'open_acc' : ('openAcc', 'int'),
  'pub_rec' : ('pubRec', 'int'),
  'revol_bal' : ('revolBal', 'convert_float_default'),
  'revol_util' : ('revolUtil', 'convert_percentage'),
  'total_acc' : ('totalAcc', 'int'),
  'initial_list_status' : ('', 'str'),
  'out_prncp' : ('', 'str'),
  'out_prncp_inv' : ('', 'str'),
  'total_pymnt' : ('', 'str'),
  'total_pymnt_inv' : ('', 'str'),
  'total_rec_prncp' : ('', 'str'),
  'total_rec_int' : ('', 'str'),
  'total_rec_late_fee' : ('', 'str'),
  'recoveries' : ('', 'str'),
  'collection_recovery_fee' : ('', 'str'),
  'last_pymnt_d' : ('', 'str'),
  'last_pymnt_amnt' : ('', 'str'),
  'next_pymnt_d' : ('', 'str'),
  'last_credit_pull_d' : ('', 'str'),
  'last_fico_range_high' : ('', 'str'),
  'last_fico_range_low' : ('', 'str'),
  'collections_12_mths_ex_med' : ('collections12MthsExMed', 'int'),
  'mths_since_last_major_derog' : ('mthsSinceLastMajorDerog', 'convert_int_default'),
  'policy_code' : ('', 'str'),
  'application_type' : ('applicationType', 'unicode'),
  'annual_inc_joint' : ('annualIncJoint', 'convert_float_default'),
  'dti_joint' : ('dtiJoint', 'convert_float_default'),
  'verification_status_joint' : ('isIncVJoint', 'convert_verification_status'),
  'acc_now_delinq' : ('accNowDelinq', 'int'),
  'tot_coll_amt' : ('totCollAmt', 'int'),
  'tot_cur_bal' : ('totCurBal', 'int'),
  'open_acc_6m' : ('openAcc6m', 'convert_int_default'),
  'open_il_6m' : ('openIl6m', 'convert_int_default'),
  'open_il_12m' : ('openIl12m', 'convert_int_default'),
  'open_il_24m' : ('openIl24m', 'convert_int_default'),
  'mths_since_rcnt_il' : ('mthsSinceRcntIl', 'convert_int_default'),
  'total_bal_il' : ('totalBalIl', 'convert_float_default'),
  'il_util' : ('iLUtil', 'convert_float_default'),
  'open_rv_12m' : ('openRv12m', 'convert_int_default'),
  'open_rv_24m' : ('openRv24m', 'convert_int_default'),
  'max_bal_bc' : ('maxBalBc', 'convert_float_default'),
  'all_util' : ('allUtil', 'convert_float_default'),
  'total_rev_hi_lim' : ('totalRevHiLim', 'int'),
  'inq_fi' : ('inqFi', 'convert_int_default'),
  'total_cu_tl' : ('totalCuTl', 'convert_int_default'),
  'inq_last_12m' : ('inqLast12m', 'convert_int_default'),
  'acc_open_past_24mths' : ('accOpenPast24Mths', 'convert_int_default'),
  'avg_cur_bal' : ('avgCurBal', 'int'),
  'bc_open_to_buy' : ('bcOpenToBuy', 'convert_int_default'),
  'bc_util' : ('bcUtil', 'convert_float_default'),
  'chargeoff_within_12_mths' : ('chargeoffWithin12Mths', 'int'),
  'delinq_amnt' : ('delinqAmnt', 'float'),
  'mo_sin_old_il_acct' : ('moSinOldIlAcct', 'convert_int_default'),
  'mo_sin_old_rev_tl_op' : ('moSinOldRevTlOp', 'int'),
  'mo_sin_rcnt_rev_tl_op' : ('moSinRcntRevTlOp', 'int'),
  'mo_sin_rcnt_tl' : ('moSinRcntTl', 'int'),
  'mort_acc' : ('mortAcc', 'int'),
  'mths_since_recent_bc' : ('mthsSinceRecentBc', 'convert_int_default'),
  'mths_since_recent_bc_dlq' : ('mthsSinceRecentBcDlq', 'convert_int_default'),
  'mths_since_recent_inq' : ('mthsSinceRecentInq', 'convert_int_default'),
  'mths_since_recent_revol_delinq' : ('mthsSinceRecentRevolDelinq', 'convert_int_default'),
  'num_accts_ever_120_pd' : ('numAcctsEver120Ppd', 'int'),
  'num_actv_bc_tl' : ('numActvBcTl', 'int'),
  'num_actv_rev_tl' : ('numActvRevTl', 'int'),
  'num_bc_sats' : ('numBcSats', 'int'),
  'num_bc_tl' : ('numBcTl', 'int'),
  'num_il_tl' : ('numIlTl', 'int'),
  'num_op_rev_tl' : ('numOpRevTl', 'int'),
  'num_rev_accts' : ('numRevAccts', 'convert_int_default'),
  'num_rev_tl_bal_gt_0' : ('numRevTlBalGt0', 'int'),
  'num_sats' : ('numSats', 'int'),
  'num_tl_120dpd_2m' : ('numTl120dpd2m', 'convert_int_default'),
  'num_tl_30dpd' : ('numTl30dpd', 'int'),
  'num_tl_90g_dpd_24m' : ('numTl90gDpd24m', 'int'),
  'num_tl_op_past_12m' : ('numTlOpPast12m', 'int'),
  'pct_tl_nvr_dlq' : ('pctTlNvrDlq', 'float'),
  'percent_bc_gt_75' : ('percentBcGt75', 'convert_float_default'),
  'pub_rec_bankruptcies' : ('pubRecBankruptcies', 'int'),
  'tax_liens' : ('taxLiens', 'int'),
  'tot_hi_cred_lim' : ('totHiCredLim', 'int'),
  'total_bal_ex_mort' : ('totalBalExMort', 'int'),
  'total_bc_limit' : ('totalBalIl', 'float'),
  'total_il_high_credit_limit' : ('totalIlHighCreditLimit', 'int'),
  'revol_bal_joint' : ('revolBalJoint', 'convert_float_default'),
  'sec_app_fico_range_low' : ('', 'str'),
  'sec_app_fico_range_high' : ('', 'str'),
  'sec_app_earliest_cr_line' : ('', 'str'),
  'sec_app_inq_last_6mths' : ('', 'str'),
  'sec_app_mort_acc' : ('', 'str'),
  'sec_app_open_acc' : ('', 'str'),
  'sec_app_revol_util' : ('', 'str'),
  'sec_app_open_il_6m' : ('', 'str'),
  'sec_app_num_rev_accts' : ('', 'str'),
  'sec_app_chargeoff_within_12_mths' : ('', 'str'),
  'sec_app_collections_12_mths_ex_med' : ('', 'str'),
  'sec_app_mths_since_last_major_derog' : ('', 'str')
}

useful_status_list = ['Current', 'Late (31-120 days)', 'Fully Paid', 'Default', 'Charged Off']

def convert_row_to_loan(row, header):
  loan = {}
  for i in list(range(0, len(header))):
    field = header[i]
    value = row[i].strip()
    key, method = loan_csv_header_to_key_map[field]
    if len(key) == 0:
      continue
    try:
      loan[key] = eval("%s(value)" % method)
    except Exception as e:
      print e
      print "ID %d -- %s -- %s -- value: '%s'" % (loan['id'], field, key, value)
      raise Exception('stop here!')
  return loan


def print_loan_feature_stats(past_loans, avail_loans, keys):
  past_stats = {}
  avail_stats = {}
  for key in keys:
    past_stats[key] = {'total': 0, 'non_empty': 0}
    avail_stats[key] = {'total': 0, 'non_empty': 0}

  for loan in past_loans:
    for key, value in loan.iteritems():
      if key in keys:
        past_stats[key]['total'] += 1
        if value is not None:
          past_stats[key]['non_empty'] += 1

  for loan in avail_loans:
    for key, value in loan.iteritems():
      if key in keys:
        avail_stats[key]['total'] += 1
        if value is not None:
          avail_stats[key]['non_empty'] += 1

  for key, value in past_stats.iteritems():
    past_s = 1.0 * value['non_empty'] / value['total'] * 100
    avail_value = avail_stats[key]
    avail_s = 1.0 * avail_value['non_empty'] / avail_value['total'] * 100
    print "%30s : \t%-3.3f%%\t%-3.3f%%" % (key, past_s, avail_s)


def main(argv):
  csv_file_source = {
    config.StorageFile.LC_2017_Q1_LOAN_FILE : ['Late (31-120 days)', 'Default', 'Charged Off'],
    config.StorageFile.LC_2016_Q1_LOAN_FILE : useful_status_list,
    config.StorageFile.LC_2016_Q2_LOAN_FILE : useful_status_list,
    config.StorageFile.LC_2016_Q3_LOAN_FILE : useful_status_list,
    config.StorageFile.LC_2016_Q4_LOAN_FILE : ['Late (31-120 days)', 'Fully Paid', 'Default', 'Charged Off'],
    config.StorageFile.LC_2015_LOAN_FILE : useful_status_list
  }

  loans = []
  stats = defaultdict(lambda: 0)
  for filename, status_list in csv_file_source.iteritems():
    reader = csv.reader(open(filename))
    reader.next()
    header = reader.next()
    for row in reader:
      if len(row) < 10:
        continue
      loan = convert_row_to_loan(row, header)
      if loan['loanStatus'] in status_list:
        loans.append(loan)
        stats[loan['loanStatus']] += 1

  keys = loans[0].keys()
  keys.remove('loanStatus')
  avail_loans = lending_club.get_available_loan_listings()
  print_loan_feature_stats(loans, avail_loans, keys)

  storage.save_to_file(loans, config.StorageFile.LC_LOAN_SOURCE_DATA)
  print "Save %d loans to %s" % (len(loans), config.StorageFile.LC_LOAN_SOURCE_DATA)
  print
  print "Loan status distribution: "
  print stats


if __name__ == "__main__":
  main(sys.argv)
