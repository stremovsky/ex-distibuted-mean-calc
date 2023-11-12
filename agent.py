import sys
import csv
from flask import Flask, abort, jsonify, request

if len(sys.argv) < 3:
  print("specify port and url")
  sys.exit()

port = sys.argv[1]
#file_path = 'mock_patient_data_0.csv'
file_path = sys.argv[2]

sensetive = {'ID_CASE', 'ID_XR_SUID'}
records = []
app = Flask(__name__)

with open(file_path, 'r') as csv_file:
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    #print(row)
    records.append(row)

def calc_histogram(column_name):
  record_count = {}
  for row in records:
    if row[column_name].isnumeric():
      continue
    if row[column_name] in record_count:
      record_count[row[column_name]] += 1
    else:
      record_count[row[column_name]] = 1
  print(record_count)
  return record_count

def calc_mean(column_name):
  total = float(0)
  sigma = float(0)
  num_records = 0
  for row in records:
    if row[column_name].isnumeric():
      #print(row[column_name])
      total += float(row[column_name])
      num_records += 1
  mean = total / num_records
  for row in records:
    if row[column_name].isnumeric():
      sigma += (float(row[column_name]) - mean)**2
  result = {}
  result['mean'] = mean
  result['count'] = num_records
  result['standard_deviation'] = (sigma / num_records) ** 0.5
  return result

def calc_sigma(column_name, mean):
  sigma = float(0)
  num_records = 0
  for row in records:
    if row[column_name].isnumeric():
      sigma += (float(row[column_name]) - mean)**2
      num_records += 1
  result = {}
  result['sigma'] = sigma
  result['count'] = num_records
  return result

@app.route('/api/histogram')
def api_histogram():
  column = request.args.get('column')
  if column is None:
    # Generates an "Access Denied" error
    abort(403)
  if column in sensetive:
    abort(403)
  histogram = calc_histogram(column)
  return jsonify(histogram)

@app.route('/api/count')
def api_count():
  data = {}
  data['count'] = len(records)
  return jsonify(data)

@app.route('/api/mean')
def api_mean():
  column = request.args.get('column')
  if column is None:
    # Generates an "Access Denied" error
    abort(403)
  if column in sensetive:
    abort(403)
  mean = calc_mean(column)
  return jsonify(mean)

@app.route('/api/sigma')
def api_sigma():
  column = request.args.get('column')
  mean = float(request.args.get('mean'))
  if column is None:
    # Generates an "Access Denied" error
    abort(403)
  if column in sensetive:
    abort(403)
  sigma = calc_sigma(column, mean)
  return jsonify(sigma)

if __name__ == '__main__':
  app.run(debug=True, port=port)
