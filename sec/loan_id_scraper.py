import requests
import os
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
import sys
import time
from web_scraper import *

def get_all_sec_files():
  csv_file = open(SecStaticData.raw_data_file)
  reader = csv.DictReader(csv_file)
  rows = []
  for row in reader:
    if row['url'].find('postsup_') > 0:
      rows.append(row)
  return rows

# Creat the fold if not exists
def get_sec_fold(sec_date):
  year_month = sec_date.split('-')[0] + '-' + sec_date.split('-')[1]
  fold_dir = SecStaticData.quarter_raw_sec_fold + year_month + '/'
  if os.path.isdir(fold_dir):
    return fold_dir
  os.makedirs(fold_dir)
  print 'created a fold: ' + fold_dir
  return fold_dir


def pull_sec_data(url):
  pattern_string = 'member loan id'
  session = requests.session()
  response = session.get(url)
  if response.status_code != 200:
    raise Exception('Access Denied!')

  soup = BeautifulSoup(response.text, 'html.parser')
  tables = soup.find_all('table')
  stats = []
  for table in tables:
    if str(table).lower().find(pattern_string) <= 0:
      continue
    all_trs = table.find_all('tr')
    row = all_trs[1]
    loan_id = row.find_all('td')[0].text.strip()
    row = all_trs[1]
    loan_amount = int(
      row.find_all('td')[1].text.strip().replace('$', '').replace(',', ''))
    stats.append({'loan_id': loan_id, 'loan_amount': loan_amount})
  return stats

def dump_to_raw_stats_to_file(filename, stats):
  csvfile = open(filename, 'w')
  fieldnames = ['loan_id', 'loan_amount']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
  for row in stats:
    writer.writerow({'loan_id': row['loan_id'], 'loan_amount': row['loan_amount']})



start_date = '2017-01-01'

rows = get_all_sec_files()
for row in rows:
  if row['date'] < start_date:
    continue
  fold = get_sec_fold(row['date'])
  sec_file_name = fold + row['id'] + '.csv'
  if os.path.isfile(sec_file_name):
    continue
  print "pulling {}".format(row['url'])
  stats = pull_sec_data(row['url'])
  dump_to_raw_stats_to_file(sec_file_name, stats)
  print "Saved {} records to {}".format(len(stats), sec_file_name)
