from bs4 import BeautifulSoup
import datetime
import config

'''
loan details
{
    "accNowDelinq": 0,                                  # ACCOUNTS_NOW_DELINQUENT
    "accOpenPast24Mths": 10,                            # ACCOUNTS_OPEN_IN_PAST_24_MTHS
    "acceptD": "2017-05-18T13:59:47.000-07:00",         # ACCEPTED_DATE
    "addrState": "WI",                                  # ADDRESS_STATE
    "addrZip": "539xx",                                 # ADDRESS_ZIP
    "allUtil": 59.7,                                    # ALL_UTIL
    "annualInc": 45500.0,                               # ANNUAL_INCOME
    "annualIncJoint": null,                             # ANNUAL_INCOME_JOINT
    "applicationType": "INDIVIDUAL",                    # APPLICATION_TYPE
    "avgCurBal": 5385,                                  # AVG_CUR_BAL
    "bcOpenToBuy": 3669,                                # BANK_CARDS_AMOUNT_OPEN_TO_BUY
    "bcUtil": 80.8,                                     # BANK_CARDS_UTILIZATION_RATIO
    "chargeoffWithin12Mths": 0,                         # CHARGEOFF_WITHIN_12_MTHS
    "collections12MthsExMed": 0,                        # COLLECTIONS_12_MTHS_EXMED
    "creditPullD": "2017-05-18T13:55:13.000-07:00",     # CREDIT_PULL_DATE
    "delinq2Yrs": 0,                                    # DELINQUENCIES_IN_LAST_2_YEARS
    "delinqAmnt": 0.0,                                  # DELINQUENT_AMOUNT
    "desc": null,                                       # DESCRIPTION
    "dti": 19.28,                                       # DEBT_TO_INCOME_RATIO
    "dtiJoint": null,                                   # DTI_JOINT
    "earliestCrLine": "2007-07-17T17:00:00.000-07:00",  # EARLIEST_CREDIT_LINE_DATE
    "empLength": null,                                  # EMPLOYMENT_LENGTH
    "empTitle": null,                                   # EMP_TITLE
    "expD": "2017-06-29T18:00:00.000-07:00",            # EXPIRATION_DATE
    "expDefaultRate": 16.99,                            # EXPECTED_DEFAULT_RATE
    "ficoRangeHigh": 684,                               # FICO_RANGE_HIGH
    "ficoRangeLow": 680,                                # FICO_RANGE_LOW
    "fundedAmount": 16200.0,                            # FUNDED_AMOUNT
    "grade": "G",                                       # GRADE
    "homeOwnership": "MORTGAGE",                        # HOME_OWNERSHIP
    "housingPayment": 621.0,                            # HOUSING_PAYMENT
    "iLUtil": 6.4,                                      # IL_UTIL
    "id": 109514436,                                    # LOAN_ID
    "ilsExpD": "2017-05-30T18:00:00.000-07:00",         # INITIAL_LIST_STATUS_EXPIRE_DATE
    "initialListStatus": "F",                           # INITIAL_LIST_STATUS
    "inqFi": 0,                                         # INQ_FI
    "inqLast12m": 0,                                    # INQ_LAST_12M
    "inqLast6Mths": 0,                                  # INQUIRIES_IN_LAST_6_MONTHS
    "installment": 658.05,                              # INSTALLMENT
    "intRate": 30.89,                                   # INTEREST_RATE
    "investorCount": null,                              # INVESTOR_COUNT
    "isIncV": "VERIFIED",                               # ANNUAL_INCOME_VERIFIED
    "isIncVJoint": null,                                # ANNUAL_INCOME_JOINT_VERIFIED
    "listD": "2017-05-30T18:00:00.000-07:00",           # LISTING_DATE
    "loanAmount": 20000.0,                              # LOAN_AMOUNT
    "maxBalBc": 5349.0,                                 # MAX_BAL_BC
    "memberId": 117733148,                              # MEMBER_ID
    "moSinOldIlAcct": 118,                              # MO_SIN_OLD_IL_ACCT
    "moSinOldRevTlOp": 31,                              # MO_SIN_OLD_REV_TL_OP
    "moSinRcntRevTlOp": 1,                              # MO_SIN_RCNT_REV_TL_OP
    "moSinRcntTl": 1,                                   # MO_SIN_RCNT_TL
    "mortAcc": 2,                                       # MORTGAGE_ACCOUNTS
    "mtgPayment": 624.11,                               # MTG_PAYMENT
    "mthsSinceLastDelinq": null,                        # MONTHS_SINCE_LAST_DELINQUENCY
    "mthsSinceLastMajorDerog": null,                    # MTHS_SINCE_LAST_MAJOR_DEROG
    "mthsSinceLastRecord": null,                        # MONTHS_SINCE_LAST_RECORD
    "mthsSinceRcntIl": 36,                              # MTHS_SINCE_RCNT_IL
    "mthsSinceRecentBc": 10,                            # MONTHS_SINCE_RECENT_BANK_CARD
    "mthsSinceRecentBcDlq": null,                       # MTHS_SINCE_RECENT_BC_DLQ
    "mthsSinceRecentInq": 17,                           # MONTHS_SINCE_LAST_INQUIRY
    "mthsSinceRecentRevolDelinq": null,                 # MONTHS_SINCE_RECENT_REVOLVING_DELINQUENCY
    "numAcctsEver120Ppd": 0,                            # NUM_ACCTS_EVER_120_PPD
    "numActvBcTl": 6,                                   # NUM_ACTV_BC_TL
    "numActvRevTl": 8,                                  # NUM_ACTV_REV_TL
    "numBcSats": 9,                                     # NUM_BC_STATS
    "numBcTl": 9,                                       # NUM_BC_TL
    "numIlTl": 4,                                       # NUM_IL_TL
    "numOpRevTl": 15,                                   # NUM_OP_REV_TL
    "numRevAccts": 15,                                  # NUM_REV_ACCTS
    "numRevTlBalGt0": 8,                                # NUM_REV_TL_BAL_GT0
    "numSats": 17,                                      # NUM_STATS
    "numTl120dpd2m": 0,                                 # NUM_TL_120_DPD_2_M
    "numTl30dpd": 0,                                    # NUM_TL_30_DPD
    "numTl90gDpd24m": 0,                                # NUM_TL_90_G_DPD_24_M
    "numTlOpPast12m": 4,                                # NUM_TL_OP_PAST_12_M
    "openAcc": 17,                                      # OPEN_ACCOUNTS
    "openAcc6m": 1,                                     # OPEN_ACC_6M
    "openIl12m": 0,                                     # OPEN_IL_12M
    "openIl24m": 0,                                     # OPEN_IL_24M
    "openIl6m": 1,                                      # OPEN_IL_6M
    "openRv12m": 4,                                     # OPEN_RV_12M
    "openRv24m": 10,                                    # OPEN_RV_24M
    "pctTlNvrDlq": 100,                                 # PCT_TL_NVR_DLQ
    "percentBcGt75": 44.4,                              # PERCENT_OF_BANK_CARDS_OVER_75_PERCENT_UTIL
    "pubRec": 0,                                        # PUBLIC_RECORDS
    "pubRecBankruptcies": 0,                            # PUB_REC_BANKRUPTCIES
    "purpose": "debt_consolidation",                    # PURPOSE
    "reviewStatus": "APPROVED",                         # REVIEW_STATUS
    "reviewStatusD": "2017-05-30T12:45:21.000-07:00",   # REVIEW_STATUS_DATE
    "revolBal": 19574.0,                                # REVOLVING_BALANCE
    "revolBalJoint": null,                              # REVOL_BAL_JOINT
    "revolUtil": 65.7,                                  # REVOLVING_UTILIZATION
    "secAppChargeoffWithin12Mths": null,                # SEC_APP_CHARGEOFF_WITHIN_12_MTHS
    "secAppCollections12MthsExMed": null,               # SEC_APP_COLLECTIONS_12_MTHS_EXMED
    "secAppEarliestCrLine": null,                       # SEC_APP_EARLIEST_CR_LINE
    "secAppFicoRangeHigh": null,                        # SEC_APP_FICO_RANGE_HIGH
    "secAppFicoRangeLow": null,                         # SEC_APP_FICO_RANGE_LOW
    "secAppInqLast6Mths": null,                         # SEC_APP_INQ_LAST_6MTHS
    "secAppMortAcc": null,                              # SEC_APP_MORT_ACC
    "secAppMthsSinceLastMajorDerog": null,              # SEC_APP_MTHS_SINCE_LAST_MAJOR_DEROG
    "secAppNumRevAccts": null,                          # SEC_APP_NUM_REV_ACCTS
    "secAppOpenAcc": null,                              # SEC_APP_OPEN_ACC
    "secAppOpenIl6m": null,                             # SEC_APP_OPEN_IL_6M
    "secAppRevolUtil": null,                            # SEC_APP_REVOL_UTIL
    "serviceFeeRate": 1.21,                             # SERVICE_FEE_RATE
    "subGrade": "G3",                                   # SUBGRADE
    "taxLiens": 0,                                      # TAX_LIENS
    "term": 60,                                         # TERM
    "totCollAmt": 0,                                    # TOT_COLL_AMT
    "totCurBal": 91549,                                 # TO_CUR_BAL
    "totHiCredLim": 110140,                             # TO_HI_CRED_LIM
    "totalAcc": 21,                                     # TOTAL_ACCOUNTS
    "totalBalExMort": 19788,                            # TOTAL_BALANCE_EXCLUDING_MORTGAGE
    "totalBalIl": 214.0,                                # TOTAL_BAL_IL
    "totalBcLimit": 19100,                              # TOTAL_BANK_CARD_LIMIT
    "totalCuTl": 2,                                     # TOTAL_CU_TL
    "totalIlHighCreditLimit": 3330,                     # TOTAL_IL_HIGH_CREDIT_LIMIT
    "totalRevHiLim": 29800                              # TOTAL_REV_HI_LIM
}
'''

def fetch_loan_detail_from_html(html):
  soup = BeautifulSoup(html, 'html.parser')
  loan = {}
  # parse note id
  for div in soup.find_all('div'):
    class_values = div.attrs.get('class')
    if class_values is not None and 'memberHeader' in class_values:
      break
  loan['id'] = int(div.text.strip().split(':')[1].strip().split(' ')[0])

  # parse content
  if len(soup.find_all('table')) < 6:
    raise Exception('Bad HTML page')
  for table in soup.find_all('table'):
    s = str(table)
    if s.find('Amount Requested') > 0:
      loan = fetch_basic_loan_info(loan, table)
    elif s.find('Funding Received') > 0:
      loan = fetch_basic_loan_info(loan, table)
    elif s.find('Home Ownership') > 0:
      loan = fetch_basic_lender_profile(loan, table)
    elif s.find('Gross Income') > 0:
      loan = fetch_basic_lender_profile(loan, table)
    elif s.find('Credit Score') > 0:
      loan = fetch_basic_credit_history(loan, table)
    elif s.find('Delinquent Amount') > 0:
      loan = fetch_basic_credit_history(loan, table)

  return loan

'''
Parse

<table class="loan-details">
  <tr><th>Amount Requested</th><td><div class="amountRequested"><div class="status-review-text"> $34,000</div></div></td></tr>
  <tr><th>Loan Purpose</th><td>Credit card refinancing</td></tr>
  <tr><th>Loan Grade</th><td class="legend"><span class="gradeText A">A5</span></td></tr>
  <tr><th>Interest Rate</th><td>7.89%</td></tr>
  <tr><th>Loan Length</th><td>5 years (60 payments)</td></tr>
  <tr><th>Monthly Payment</th><td>$687.61 / month </td></tr>
</table>

<table class="loan-details">
  <tr><th>Funding Received</th><td class="fundingReceived">$34,000 (100.00% funded)</td></tr>
  <tr><th>Investors</th><td class="loanDetailsInvestors">896 people funded this loan</td></tr>
  <tr><th>Note issued on</th><td> 7/7/16 3:26 AM</td></tr>
  <tr><th>Note Status</th><td title="Loan has been fully repaid, either at the expiration of the 3- or 5-year year term or as a result of a prepayment.">Fully Paid</td></tr>
  <tr><th>Loan Submitted on</th><td>6/1/16 11:43 AM</td></tr>
</table>
'''
def fetch_basic_loan_info(loan, table):
  for tr in table.find_all('tr'):
    if tr.text.find('Amount Requested') > 0:
      loan['loanAmount'] = float(tr.td.text.strip().strip('$').replace(',', ''))
    elif tr.text.find('Loan Purpose') > 0:
      value = tr.td.text.strip().lower()
      loan['purpose'] = config.LoanStaticData.loan_value_to_key_map.get(value)
      if loan['purpose'] == None:
        raise Exception('Unrecoganized loan type: ' + value)
    elif tr.text.find('Loan Grade') > 0:
      loan['subGrade'] = tr.td.text.strip().upper()
      loan['grade'] = tr.td.text.strip().upper()[0]
    elif tr.text.find('Interest Rate') > 0:
      loan['intRate'] = float(tr.td.text.strip().strip('%'))
    elif tr.text.find('Investors') > 0:
      loan['numInvestors'] = int(tr.td.text.strip().split(' ')[0])
    elif tr.text.find('Note Status') > 0:
      loan['loanStatus'] = tr.td.text.strip()
    elif tr.text.find('Loan Length') > 0:
      loan['term'] = int(tr.td.text.strip().split(' ')[0]) * 12
    elif tr.text.find('Loan Submitted on') > 0:
      submit_date = tr.td.text.strip().split(' ')[0]
      parts = submit_date.split('/')
      year = int(parts[2])
      if year < 1000:
        year += 2000
      month = int(parts[0])
      day = int(parts[1])
      loan['acceptD'] = datetime.datetime(year, month, day).isoformat()
  return loan


'''
Parse
<table class="loan-details">
  <tr><th>Home Ownership</th><td>RENT</td></tr>
  <tr><th>Job Title</th><td>Analyst</td></tr>
  <tr><th>Length of Employment</th><td>6 years </td></tr>
</table>

<table class="loan-details">
  <tr><th>Gross Income</th><td>$7,292 / month<span id="verifiedIncomeAsterisk">*</span></td></tr>
  <tr><th>Debt-to-Income (DTI)</th><td>24.30%</td></tr>
  <tr><th>Location</th><td>221xx</td></tr>
</table>
'''
def fetch_basic_lender_profile(loan, table):
  for tr in table.find_all('tr'):
    if tr.text.find('Home Ownership') > 0:
      loan['homeOwnership'] = tr.td.text.upper()
    elif tr.text.find('Job Title') > 0:
      loan['empTitle'] = tr.td.text.strip()
    elif tr.text.find('Length of Employment') > 0:
      value = tr.td.text.replace('+', '').replace('<', '').strip().split(' ')[0]
      if value == 'n/a':
        num_years = 0
      else:
        num_years = int(value)
      loan['empLength'] = num_years * 12
    elif tr.text.find('Gross Income') > 0 and tr.text.find('Joint') < 0:
      raw_str = tr.td.text
      if not raw_str.startswith('n/a'):
        value = float(raw_str.split('/')[0].strip().strip('$').replace(',', ''))
      else:
        value = 0
      if raw_str.lower().find('month') > 0:
        value = value * 12
      loan['annualInc'] = value
      if raw_str.lower().find('*') > 0:
        loan['isIncV'] = 'VERIFIED'
      else:
        loan['isIncV'] = 'NOT_VERIFIED'
    elif tr.text.find('Gross Income') > 0 and tr.text.find('Joint') >= 0:
      raw_str = tr.td.text
      if raw_str != 'n/a':
        value = float(raw_str.split('/')[0].strip().strip('$').replace(',', ''))
      else:
        value = 0
      if raw_str.lower().find('month') > 0:
        value = value * 12
      loan['annualIncJoint'] = value
      if raw_str.lower().find('*') > 0:
        loan['isIncVJoint'] = 'VERIFIED'
      else:
        loan['isIncV'] = 'NOT_VERIFIED'
    elif tr.text.find('DTI') > 0 and tr.text.find('Joint') < 0:
      loan['dti'] = float(tr.td.text.strip().strip('%*'))
    elif tr.text.find('DTI') > 0 and tr.text.find('Joint') >= 0:
      loan['dtiJoint'] = float(tr.td.text.strip().strip('%*'))
    elif tr.text.find('Location') > 0:
      loan['addrZip'] = tr.td.text.strip()
  return loan

'''
Parse

<table class="loan-details">
  <tr><th>Credit Score Range:</th><td>770-774</td></tr>
  <tr><th>Earliest Credit Line</th><td>10/2002</td></tr>
  <tr><th>Open Credit Lines</th><td>26</td></tr>
  <tr><th>Total Credit Lines</th><td>53</td></tr>
  <tr><th>Revolving Credit Balance</th><td>$32,688.00</td></tr>
  <tr><th>Revolving Line Utilization</th><td>17.70%</td></tr>
  <tr><th>Inquiries in the Last 6 Months</th><td>0</td></tr>
  <tr><th>Accounts Now Delinquent</th><td>0</td></tr>
</table>

<table class="loan-details">
  <tr><th>Delinquent Amount</th><td>$0.00</td></tr>
  <tr><th>Delinquencies (Last 2 yrs)</th><td>0 </td></tr>
  <tr><th>Months Since Last Delinquency</th><td>34 </td></tr>
  <tr><th>Public Records On File</th><td>0</td></tr><tr>
  <th>Months Since Last Record</th><td>n/a </td></tr>
  <tr><th>Months Since Last Major Derogatory</th><td>n/a </td></tr>
  <tr><th>Collections Excluding Medical</th><td>0 </td></tr>
</table>
'''
def fetch_basic_credit_history(loan, table):
  for tr in table.find_all('tr'):
    if tr.text.find('Credit Score Range') > 0:
      value = tr.td.text
      scores = value.split('-')
      if len(scores) >= 2:
        loan['ficoRangeLow'] = int(scores[0])
        loan['ficoRangeHigh'] = int(scores[1])
    elif tr.text.find('Earliest Credit Line') > 0:
      # "earliestCrLine": "2007-07-17T17:00:00.000-07:00"
      value = tr.td.text
      parts = value.split('/')
      loan['earliestCrLine'] = datetime.datetime(int(parts[1]), int(parts[0]), 1).isoformat()
    elif tr.text.find('Open Credit Lines') > 0:
      loan['openAcc'] = int(tr.td.text.strip())
    elif tr.text.find('Total Credit Lines') > 0:
      loan['totalAcc'] = int(tr.td.text.strip())
    elif tr.text.find('Revolving Credit Balance') > 0:
      loan['revolBal'] = float(tr.td.text.strip().strip('$').replace(',', ''))
    elif tr.text.find('Revolving Line Utilization') > 0:
      value = tr.td.text.strip().strip('%')
      if value == 'n/a':
        loan['revolUtil'] = None
      else:
        loan['revolUtil'] = float(value)
    elif tr.text.find('Inquiries in the Last 6 Months') > 0:
      loan['inqLast6Mths'] = int(tr.td.text.strip())
    elif tr.text.find('Accounts Now Delinquent') > 0:
      loan['accNowDelinq'] = int(tr.td.text.strip())
    elif tr.text.find('Delinquent Amount') > 0:
      loan['delinqAmnt'] = float(tr.td.text.strip().strip('$').replace(',', ''))
    elif tr.text.find('Delinquencies (Last 2 yrs)') > 0:
      loan['delinq2Yrs'] = int(tr.td.text.strip())
    elif tr.text.find('Months Since Last Delinquency') > 0:
      if tr.td.text.strip().lower() != 'n/a':
        loan['mthsSinceLastDelinq'] = int(tr.td.text.strip())
      else:
        loan['mthsSinceLastDelinq'] = None
    elif tr.text.find('Public Records On File') > 0:
      loan['pubRec'] = int(tr.td.text.strip())
    elif tr.text.find('Months Since Last Record') > 0:
      if tr.td.text.strip().lower() != 'n/a':
        loan['mthsSinceLastRecord'] = int(tr.td.text.strip())
      else:
        loan['mthsSinceLastRecord'] = None
    elif tr.text.find('Months Since Last Major Derogatory') > 0:
      if tr.td.text.strip().lower() != 'n/a':
        loan['mthsSinceLastMajorDerog'] = int(tr.td.text.strip())
      else:
        loan['mthsSinceLastMajorDerog'] = None
    elif tr.text.find('Collections Excluding Medical') > 0:
      loan['collections12MthsExMed'] = int(tr.td.text.strip())
  return loan
