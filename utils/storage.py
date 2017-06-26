import csv
import json
import config

def save_to_file(object, filename):
  f = open(filename, "w")
  f.write(json.dumps(object))
  f.close()


def load_from_file(filename):
  s = open(filename, 'r').read()
  return json.loads(s)


def save_notes_to_csv(loans, note_statuses, filename):
  notes = {}
  for n in note_statuses:
    notes[n['loanId']] = n

  header_fields = []
  for key in config.StorageConfig.note_cvs_header_keys:
    header_fields.append(config.LoanStaticData.note_attribute_key_to_value_map[key])
  for key in config.StorageConfig.loan_cvs_header_keys:
    header_fields.append(config.LoanStaticData.loan_attribute_key_to_value_map[key])

  f = csv.writer(open(filename, "wb"))
  f.writerow(header_fields)

  for loan in loans:
    values = []
    loan_id = loan['id']
    note = notes[loan_id]
    for key in config.StorageConfig.note_cvs_header_keys:
      values.append(note[key])
    for key in config.StorageConfig.loan_cvs_header_keys:
      v = loan[key]
      if isinstance(v, basestring):
        v = v.encode('utf-8').strip()
      values.append(v)
    f.writerow(values)




