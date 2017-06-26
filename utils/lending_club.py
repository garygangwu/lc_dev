import requests
import scraper
import config
import json

def get_web_login_session(
      email = config.get_login_email(),
      password = config.get_login_password()):

  session_requests = requests.session()

  web_url = "https://www.lendingclub.com"
  login_url = "https://www.lendingclub.com/account/login.action"
  response = session_requests.get(web_url)
  if response.status_code != 200:
    raise Exception('access denied')

  payload = {
    "login_password": password,
    "login_email": email,
    "login_url": ""
  }

  response = session_requests.post(
    login_url,
    data = payload,
    headers = dict(referer=web_url)
  )

  if response.status_code != 200:
    raise Exception('login failed')

  return session_requests


def get_purchased_notes_detail_statuses():
  url = "https://api.lendingclub.com/api/investor/v1/accounts/%d/detailednotes" % config.get_account_id()
  headers = {
    "Content-type" : "application/json",
    "Accept" : "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
    "Authorization": config.get_api_token()
  }

  response = requests.get(url, headers=headers)
  if response.status_code != 200:
    raise Exception('API request failed')

  return response.json()['myNotes']


def get_purchased_loan_listings_in_html(loan_ids, session):
  url = 'https://www.lendingclub.com/browse/loanDetail.action?loan_id='
  htmls = []

  for loan_id in loan_ids:
    response = session.get(url + str(loan_id))
    print "fetching loan html with id = %d" % loan_id
    if response.status_code != 200:
      raise Exception('access denied')
    htmls.append(response.text)

  return htmls


def get_loans_from_htmls(htmls):
  loans = []
  for html in htmls:
    loans.append(scraper.fetch_loan_detail_from_html(html))
  return loans


def get_available_loan_listings():
  url = "https://api.lendingclub.com/api/investor/v1/loans/listing"
  headers = {
    "Content-type" : "application/json",
    "Accept" : "application/json",
    "X-LC-LISTING-VERSION" : "1.2",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
    "Authorization": config.get_api_token()
  }
  payload = {
    "showAll" : "true"
  }

  response = requests.get(url, headers=headers, params=payload)
  if response.status_code != 200:
    raise Exception('API request failed')

  return response.json()['loans']


def dump_available_loan_listings_to_cvs(filename):
  url = "https://api.lendingclub.com/api/investor/v1/loans/listing"
  headers = {
    "Content-type" : "application/json",
    "Accept" : "text/csv",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
    "X-LC-LISTING-VERSION" : "1.2",
    "Authorization": config.get_api_token()
  }
  payload = {
    "showAll" : "true"
  }

  response = requests.get(url, headers=headers, params=payload)
  if response.status_code != 200:
    raise Exception('access denied')

  if not filename.endswith('.csv'):
    filename = filename + '.csv'
  with open(filename, "w") as csv_file:
    csv_file.write(response.text)


def dump_purchased_notes_detail_statuses_to_cvs(filename):
  url = "https://api.lendingclub.com/api/investor/v1/accounts/%d/detailednotes" % config.get_account_id()
  headers = {
    "Content-type" : "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
    "Accept" : "text/csv",
    "Authorization": config.get_api_token()
  }

  response = requests.get(url, headers=headers)
  if response.status_code != 200:
    raise Exception('access denied')

  if not filename.endswith('.csv'):
    filename = filename + '.csv'
  with open(filename, "w") as csv_file:
    csv_file.write(response.text)


def get_owned_portfolios():
  url = "https://api.lendingclub.com/api/investor/v1/accounts/%d/portfolios" % config.get_account_id()
  headers = {
    "Content-type" : "application/json",
    "Accept" : "application/json",
    "X-LC-LISTING-VERSION" : "1.2",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
    "Authorization": config.get_api_token()
  }
  payload = {
    "showAll" : "true"
  }

  response = requests.get(url, headers=headers, params=payload)
  if response.status_code != 200:
    raise Exception('API request failed')

  return response.json()['myPortfolios']


def get_account_summary():
  url = "https://api.lendingclub.com/api/investor/v1/accounts/%d/summary" % config.get_account_id()
  headers = {
    "Content-type" : "application/json",
    "Accept" : "application/json",
    "X-LC-LISTING-VERSION" : "1.2",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
    "Authorization": config.get_api_token()
  }
  response = requests.get(url, headers=headers)
  if response.status_code != 200:
    raise Exception('API request failed')
  return response.json()


def get_available_cash():
  account  = get_account_summary()
  return account['availableCash']

def submit_order(loans, purchase_unit):
  url = "https://api.lendingclub.com/api/investor/v1/accounts/%d/orders" % config.get_account_id()
  headers = {
    "Content-type" : "application/json",
    "Accept" : "application/json",
    "X-LC-LISTING-VERSION" : "1.2",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
    "Authorization": config.get_api_token()
  }
  portfolio_id = config.get_portfolio_id()
  payload = {
    "aid": config.get_account_id(),
    "orders": []
  }
  for loan in loans:
    payload["orders"].append(
      {
         "loanId": loan['id'],
         "requestedAmount": purchase_unit,
         "portfolioId": portfolio_id
      }
    )
  print url
  print payload
  response = requests.post(url, data=json.dumps(payload), headers=headers)
  if response.status_code != 200:
    raise Exception('API request failed')
  return response.json()
