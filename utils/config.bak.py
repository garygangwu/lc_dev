
account_name = 'test'

account_settings = {
    'test': {
        'id': 12345,
        'email': 'test@gmail.com',
        'password': 'test',
        'api_token': 'test', # Get it from https://www.lendingclub.com/account/profile.action
        'portfolio_id': 123456
    }
}

def get_account_id():
  return account_settings[account_name]['id']

def get_login_email():
  return account_settings[account_name]['email']

def get_login_password():
  return account_settings[account_name]['password']

def get_api_token():
  return account_settings[account_name]['api_token']

def get_portfolio_id():
  return account_settings[account_name]['portfolio_id']


class StorageFile:
  loan_detail_file_in_htmls = '/Users/gary_wu/lending_club/data/raw_data/lc_loan_htmls.json'
  purchased_loan_detail_file = '/Users/gary_wu/lending_club/data/raw_data/lc_puchased_loans.json'
  purchased_note_status_file = '/Users/gary_wu/lending_club/data/raw_data/lc_puchased_notes.json'
  model_training_file = '/Users/gary_wu/lending_club/data/raw_data/lc_model_training.json'
  model_evaluating_file = '/Users/gary_wu/lending_club/data/raw_data/lc_model_evaluating.json'

  LC_LOAN_SOURCE_DATA =  '/Users/gary_wu/lending_club/data/raw_data/LC_loan_source_data.json'
  LC_LOAN_EXTENDED_DATA =  '/Users/gary_wu/lending_club/data/raw_data/LC_loan_extended_data.json'
  LC_2017_Q1_LOAN_FILE = '/Users/gary_wu/lending_club/data/raw_data/LoanStats_securev1_2017Q1.csv'
  LC_2016_Q1_LOAN_FILE = '/Users/gary_wu/lending_club/data/raw_data/LoanStats_securev1_2016Q1.csv'
  LC_2016_Q2_LOAN_FILE = '/Users/gary_wu/lending_club/data/raw_data/LoanStats_securev1_2016Q2.csv'
  LC_2016_Q3_LOAN_FILE = '/Users/gary_wu/lending_club/data/raw_data/LoanStats_securev1_2016Q3.csv'
  LC_2016_Q4_LOAN_FILE = '/Users/gary_wu/lending_club/data/raw_data/LoanStats_securev1_2016Q4.csv'
  LC_2015_LOAN_FILE = '/Users/gary_wu/lending_club/data/raw_data/LoanStats_securev1_2015.csv'

  LC_random_forest_model = '/Users/gary_wu/lending_club/data/model/random_forest_model.pkl'
  LC_extra_tree_model = '/Users/gary_wu/lending_club/data/model/extra_tree_model.pkl'
  LC_adaptive_boosting_model = '/Users/gary_wu/lending_club/data/model/adaptive_boosting_model.pkl'
  LC_gradient_boosting_model = '/Users/gary_wu/lending_club/data/model/gradient_boosting_model.pkl'

  LC_bidded_loans_file = '/Users/gary_wu/lending_club/data/bidding/bidded_loans.json'
  LC_predicted_loans_ids = '/Users/gary_wu/lending_club/data/bidding/predicted_loans_ids'

class LoanStaticData:
  loan_value_to_key_map = {
    'credit card refinancing': 'credit_card',
    'debt consolidation': 'debt_consolidation',
    'home improvement': 'home_improvement',
    'major purchase': 'major_purchase',
    'business': 'small_business',
    'medical expenses': 'medical',
    'car financing': 'car',
    'vacation': 'vacation',
    'other': 'other',
    'moving and relocation': 'moving',
    'home buying': 'house',
    'wedding expenses' : 'wedding',

    # Unverified keys
    'green loan': 'renewable_energy',
    'educational' : 'educational'
  }

  note_attribute_key_to_value_map = {
    'noteAmount': 'NOTE_AMOUNT',
    'paymentsReceived': 'PAYMENTS_RECIEVED',
    'interestReceived': 'ACCRUED_INTEREST',
    'loanStatus': 'LOAN_STATUS'
  }


  loan_attribute_key_to_value_map = {
    'accNowDelinq': 'ACCOUNTS_NOW_DELINQUENT',
    'accOpenPast24Mths': 'ACCOUNTS_OPEN_IN_PAST_24_MTHS',
    'acceptD': 'ACCEPTED_DATE',
    'addrState': 'ADDRESS_STATE',
    'addrZip': 'ADDRESS_ZIP',
    'allUtil': 'ALL_UTIL',
    'annualInc': 'ANNUAL_INCOME',
    'annualIncJoint': 'ANNUAL_INCOME_JOINT',
    'applicationType': 'APPLICATION_TYPE',
    'avgCurBal': 'AVG_CUR_BAL',
    'bcOpenToBuy': 'BANK_CARDS_AMOUNT_OPEN_TO_BUY',
    'bcUtil': 'BANK_CARDS_UTILIZATION_RATIO',
    'chargeoffWithin12Mths': 'CHARGEOFF_WITHIN_12_MTHS',
    'collections12MthsExMed': 'COLLECTIONS_12_MTHS_EXMED',
    'creditPullD': 'CREDIT_PULL_DATE',
    'delinq2Yrs': 'DELINQUENCIES_IN_LAST_2_YEARS',
    'delinqAmnt': 'DELINQUENT_AMOUNT',
    'desc': 'DESCRIPTION',
    'dti': 'DEBT_TO_INCOME_RATIO',
    'dtiJoint': 'DTI_JOINT',
    'earliestCrLine': 'EARLIEST_CREDIT_LINE_DATE',
    'empLength': 'EMPLOYMENT_LENGTH',
    'empTitle': 'EMP_TITLE',
    'expD': 'EXPIRATION_DATE',
    'expDefaultRate': 'EXPECTED_DEFAULT_RATE',
    'ficoRangeHigh': 'FICO_RANGE_HIGH',
    'ficoRangeLow': 'FICO_RANGE_LOW',
    'fundedAmount': 'FUNDED_AMOUNT',
    'grade': 'GRADE',
    'homeOwnership': 'HOME_OWNERSHIP',
    'housingPayment': 'HOUSING_PAYMENT',
    'iLUtil': 'IL_UTIL',
    'id': 'LOAN_ID',
    'ilsExpD': 'INITIAL_LIST_STATUS_EXPIRE_DATE',
    'initialListStatus': 'INITIAL_LIST_STATUS',
    'inqFi': 'INQ_FI',
    'inqLast12m': 'INQ_LAST_12M',
    'inqLast6Mths': 'INQUIRIES_IN_LAST_6_MONTHS',
    'installment': 'INSTALLMENT',
    'intRate': 'INTEREST_RATE',
    'investorCount': 'INVESTOR_COUNT',
    'isIncV': 'ANNUAL_INCOME_VERIFIED',
    'isIncVJoint': 'ANNUAL_INCOME_JOINT_VERIFIED',
    'listD': 'LISTING_DATE',
    'loanAmount': 'LOAN_AMOUNT',
    'maxBalBc': 'MAX_BAL_BC',
    'memberId': 'MEMBER_ID',
    'moSinOldIlAcct': 'MO_SIN_OLD_IL_ACCT',
    'moSinOldRevTlOp': 'MO_SIN_OLD_REV_TL_OP',
    'moSinRcntRevTlOp': 'MO_SIN_RCNT_REV_TL_OP',
    'moSinRcntTl': 'MO_SIN_RCNT_TL',
    'mortAcc': 'MORTGAGE_ACCOUNTS',
    'mtgPayment': 'MTG_PAYMENT',
    'mthsSinceLastDelinq': 'MONTHS_SINCE_LAST_DELINQUENCY',
    'mthsSinceLastMajorDerog': 'MTHS_SINCE_LAST_MAJOR_DEROG',
    'mthsSinceLastRecord': 'MONTHS_SINCE_LAST_RECORD',
    'mthsSinceRcntIl': 'MTHS_SINCE_RCNT_IL',
    'mthsSinceRecentBc': 'MONTHS_SINCE_RECENT_BANK_CARD',
    'mthsSinceRecentBcDlq': 'MTHS_SINCE_RECENT_BC_DLQ',
    'mthsSinceRecentInq': 'MONTHS_SINCE_LAST_INQUIRY',
    'mthsSinceRecentRevolDelinq': 'MONTHS_SINCE_RECENT_REVOLVING_DELINQUENCY',
    'numAcctsEver120Ppd': 'NUM_ACCTS_EVER_120_PPD',
    'numActvBcTl': 'NUM_ACTV_BC_TL',
    'numActvRevTl': 'NUM_ACTV_REV_TL',
    'numBcSats': 'NUM_BC_STATS',
    'numBcTl': 'NUM_BC_TL',
    'numIlTl': 'NUM_IL_TL',
    'numOpRevTl': 'NUM_OP_REV_TL',
    'numRevAccts': 'NUM_REV_ACCTS',
    'numRevTlBalGt0': 'NUM_REV_TL_BAL_GT0',
    'numSats': 'NUM_STATS',
    'numTl120dpd2m': 'NUM_TL_120_DPD_2_M',
    'numTl30dpd': 'NUM_TL_30_DPD',
    'numTl90gDpd24m': 'NUM_TL_90_G_DPD_24_M',
    'numTlOpPast12m': 'NUM_TL_OP_PAST_12_M',
    'openAcc': 'OPEN_ACCOUNTS',
    'openAcc6m': 'OPEN_ACC_6M',
    'openIl12m': 'OPEN_IL_12M',
    'openIl24m': 'OPEN_IL_24M',
    'openIl6m': 'OPEN_IL_6M',
    'openRv12m': 'OPEN_RV_12M',
    'openRv24m': 'OPEN_RV_24M',
    'pctTlNvrDlq': 'PCT_TL_NVR_DLQ',
    'percentBcGt75': 'PERCENT_OF_BANK_CARDS_OVER_75_PERCENT_UTIL',
    'pubRec': 'PUBLIC_RECORDS',
    'pubRecBankruptcies': 'PUB_REC_BANKRUPTCIES',
    'purpose': 'PURPOSE',
    'reviewStatus': 'REVIEW_STATUS',
    'reviewStatusD': 'REVIEW_STATUS_DATE',
    'revolBal': 'REVOLVING_BALANCE',
    'revolBalJoint': 'REVOL_BAL_JOINT',
    'revolUtil': 'REVOLVING_UTILIZATION',
    'secAppChargeoffWithin12Mths': 'SEC_APP_CHARGEOFF_WITHIN_12_MTHS',
    'secAppCollections12MthsExMed': 'SEC_APP_COLLECTIONS_12_MTHS_EXMED',
    'secAppEarliestCrLine': 'SEC_APP_EARLIEST_CR_LINE',
    'secAppFicoRangeHigh': 'SEC_APP_FICO_RANGE_HIGH',
    'secAppFicoRangeLow': 'SEC_APP_FICO_RANGE_LOW',
    'secAppInqLast6Mths': 'SEC_APP_INQ_LAST_6MTHS',
    'secAppMortAcc': 'SEC_APP_MORT_ACC',
    'secAppMthsSinceLastMajorDerog': 'SEC_APP_MTHS_SINCE_LAST_MAJOR_DEROG',
    'secAppNumRevAccts': 'SEC_APP_NUM_REV_ACCTS',
    'secAppOpenAcc': 'SEC_APP_OPEN_ACC',
    'secAppOpenIl6m': 'SEC_APP_OPEN_IL_6M',
    'secAppRevolUtil': 'SEC_APP_REVOL_UTIL',
    'serviceFeeRate': 'SERVICE_FEE_RATE',
    'subGrade': 'SUBGRADE',
    'taxLiens': 'TAX_LIENS',
    'term': 'TERM',
    'totCollAmt': 'TOT_COLL_AMT',
    'totCurBal': 'TO_CUR_BAL',
    'totHiCredLim': 'TO_HI_CRED_LIM',
    'totalAcc': 'TOTAL_ACCOUNTS',
    'totalBalExMort': 'TOTAL_BALANCE_EXCLUDING_MORTGAGE',
    'totalBalIl': 'TOTAL_BAL_IL',
    'totalBcLimit': 'TOTAL_BANK_CARD_LIMIT',
    'totalCuTl': 'TOTAL_CU_TL',
    'totalIlHighCreditLimit': 'TOTAL_IL_HIGH_CREDIT_LIMIT',
    'totalRevHiLim': 'TOTAL_REV_HI_LIM'
  }

class StorageConfig:
  loan_cvs_header_keys = [
    'id',
    'grade',
    'subGrade',
    'loanAmount',
    'term',
    'intRate',
    'purpose',
    'homeOwnership',
    'addrZip',
    'empTitle',
    'empLength',
    'annualInc',
    'isIncV',
    'delinqAmnt',
    'delinq2Yrs',
    'mthsSinceLastDelinq',
    'mthsSinceLastRecord',
    'mthsSinceLastMajorDerog',
    'pubRec',
    'accNowDelinq',
    'ficoRangeLow',
    'ficoRangeHigh',
    'inqLast6Mths',
    'openAcc',
    'totalAcc',
    'earliestCrLine',
    'dti',
    'revolBal',
    'revolUtil',
    'collections12MthsExMed'
  ]

  note_cvs_header_keys = [
    'noteAmount',
    'paymentsReceived',
    'interestReceived',
    'loanStatus'
  ]
