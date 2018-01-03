import requests
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
import sys
import time

class SecStaticData:
  url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001409970&type=424B3&dateb=&owner=include&count=100'
  website = 'https://www.sec.gov'
  raw_data_file = '/Users/gary_wu/lending_club/data/loan_sec_stats.csv'
  quarter_postsup_stats = '/Users/gary_wu/lending_club/data/quarter_postsup_stats.csv'
  quarter_salessup_stats = '/Users/gary_wu/lending_club/data/quarter_salessup_stats.csv'
  quarter_raw_sec_fold = '/Users/gary_wu/lending_club/data/sec/'

def fetch_all_sec_424B3_filing_pages(start_date = '2017-09-01'):
  loan_aggr_data = load_raw_data_from_csv_file()
  session = requests.session()

  start = 0
  while True:
    url = SecStaticData.url + "&start=%d" % start
    keep_read = fetch_one_sec_424B3_filing_page(url, session, loan_aggr_data, start_date)
    if not keep_read:
      break
    start += 100

  return loan_aggr_data


def fetch_one_sec_424B3_filing_page(url, session, loan_aggr_data, start_date = '2017-01-01'):
  response = session.get(url)
  if response.status_code != 200:
    raise Exception('Access Denied!')

  soup = BeautifulSoup(response.text, 'html.parser')
  tables = soup.find_all('table')
  rows = tables[2].find_all('tr')
  rows.pop(0) # Remove the header row

  keep_read = False
  for row in rows:
    tds = row.find_all('td')

    doc_date = tds[3].text
    doc_id = tds[4].text.strip()

    keep_read = doc_date >= start_date

    if loan_aggr_data.get(doc_id) is not None:
      continue

    if doc_date >= start_date:
      doc_url = get_loan_url(SecStaticData.website + tds[1].a.attrs.get('href'), session)
      loan_aggr_data[doc_id] = {
          'url': doc_url,
          'date': doc_date,
          'id': doc_id,
          'loan_amount': -1
        }
      print "%s: %s" % (doc_date, doc_url)

  return keep_read


def populate_loan_amount(loan_aggr_data, save_intermediate_result = False):
  session = requests.session()
  for doc_id, doc_item in loan_aggr_data.iteritems():
    if doc_item.get('loan_amount') is None or doc_item['loan_amount'] < 0:
      print "Pulling loan amount for %s with id %s" % (doc_item['date'], doc_id)
      loan_amount = get_total_loan_amount_from_one_sec_filing_page(doc_item['url'], session)
      print "%s: " % doc_item['date'] + "{:,}".format(loan_amount)
      doc_item['loan_amount'] = loan_amount

      if save_intermediate_result:
        save_raw_data_to_csv_file(loan_aggr_data)


def get_loan_url(url, session):
  response = session.get(url)
  if response.status_code != 200:
    raise Exception('Access Denied!')
  soup = BeautifulSoup(response.text, 'html.parser')
  rows = soup.find_all('table')[0].find_all('tr')
  return SecStaticData.website + rows[1].find_all('td')[2].a.attrs.get('href')


def get_total_loan_amount_from_one_sec_filing_page(url, session):
  response = session.get(url)
  if response.status_code != 200:
    raise Exception('Access Denied!')
  soup = BeautifulSoup(response.text, 'html.parser')
  tables = soup.find_all('table')
  total_amount = 0

  if url.find('salessup_') > 0:
    pattern_string = 'series of member payment dependent notes'
  else:
    pattern_string = 'member loan id'

  for table in tables:
    if str(table).lower().find(pattern_string) <= 0:
      continue
    row = table.find_all('tr')[1]
    loan_amount = int(row.find_all('td')[1].text.strip().replace('$', '').replace(',', ''))
    total_amount += loan_amount

  return total_amount


def save_raw_data_to_csv_file(loan_aggr_data):
  f = csv.writer(open(SecStaticData.raw_data_file, "wb"))
  f.writerow(['date', 'id', 'amount', 'url'])
  for key, item in loan_aggr_data.iteritems():
    f.writerow([item['date'], item['id'], item['loan_amount'], item['url']])
  print 'Save the stats to ' + SecStaticData.raw_data_file


def load_raw_data_from_csv_file():
  print 'Load raw data from: ' + SecStaticData.raw_data_file
  loan_aggr_data = {}
  f = csv.reader(open(SecStaticData.raw_data_file))
  next(f)
  for row in f:
    item = {}
    item['date'] = row[0]
    item['id'] = row[1]
    item['loan_amount'] = int(row[2])
    item['url'] = row[3]
    loan_aggr_data[item['id']] = item
  return loan_aggr_data


def generate_aggregated_stats():
  loan_aggr_data = load_raw_data_from_csv_file()
  quarter_postsup_stats = defaultdict(int)
  quarter_salessup_stats = defaultdict(int)
  for key, item in loan_aggr_data.iteritems():
    date_values = item['date'].split('-')
    year_quarter = date_values[0] + '-Q' + str((int(date_values[1]) - 1) / 3 + 1)
    if item['url'].find('salessup_') > 0:
      quarter_salessup_stats[year_quarter] += item['loan_amount']
    elif item['url'].find('postsup_') > 0:
      quarter_postsup_stats[year_quarter] += item['loan_amount']
    else:
      raise Exception('Unexpected URL: ' + item['url'])

  f = csv.writer(open(SecStaticData.quarter_postsup_stats, "wb"))
  f.writerow(['quarter', 'loan amount'])
  for key, value in quarter_postsup_stats.iteritems():
    f.writerow([key, value])
  print 'Save the quarterly stats to ' + SecStaticData.quarter_postsup_stats
  f = csv.writer(open(SecStaticData.quarter_salessup_stats, "wb"))
  f.writerow(['quarter', 'loan amount'])
  for key, value in quarter_salessup_stats.iteritems():
    f.writerow([key, value])
  print 'Save the quarterly stats to ' + SecStaticData.quarter_salessup_stats


'''
def temp_merge_lists(doc_list, salessup_list):
  loan_aggr_data = {}
  for l in salessup_list:
    id = l['id']
    loan_aggr_data[id] = l

  for l in doc_list:
    id = l['id']
    if loan_aggr_data.get(id) is None:
      loan_aggr_data[id] = l
  return loan_aggr_data


def validate_lists(doc_list = [], salessup_list = []):
  ll = doc_list + salessup_list
  loan_aggr_data = {}
  for l in ll:
    id = l['id']
    if loan_aggr_data.get(id) is None:
       loan_aggr_data[id]= l
    elif loan_aggr_data[id]['url'] != l['url']:
      print 'bad data'
      print l
      print loan_aggr_data[id]
'''


def main():
  start_date = '2017-06-01'
  loan_aggr_data = fetch_all_sec_424B3_filing_pages(start_date)
  while True:
    try:
      print 'Start processing ...'
      populate_loan_amount(loan_aggr_data, True)
      generate_aggregated_stats()
    except requests.exceptions.ConnectionError as err:
      print err
      print 'Retrying ... after 60 seconds ...'
      time.sleep(60)
      continue
    except:
      print("Unexpected error:", sys.exc_info()[0])
    break


if __name__ == "__main__":
  main()
