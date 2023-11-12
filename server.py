import requests
from flask import Flask, abort, jsonify, request

agents = ['http://localhost:6000', 'http://localhost:6001']
sensetive = {'ID_CASE', 'ID_XR_SUID'}
app = Flask(__name__)
port = 5000

def fetch_json(url):
  response = requests.get(url)
  json_data = response.json()  # Parse the JSON response
  return json_data

def calc_histogram(column):
  record_count = {}
  for agent in agents:
    url = agent + '/api/histogram?column=' + column
    print(url)
    agent_records = fetch_json(url)
    print(agent_records)
    for key in agent_records:
      if key in record_count:
        record_count[key] += agent_records[key]
      else:
        record_count[key] = agent_records[key]
  print(record_count)
  return record_count

def calc_count():
  num = 0
  record_count = {}
  for agent in agents:
    url = agent + '/api/count'
    print(url)
    agent_records = fetch_json(url)
    num += agent_records['count']
  print(num)
  return num

def calc_mean(column):
  num = float(0)
  count = 0
  for agent in agents:
    url = agent + '/api/mean?column=' + column
    print(url)
    agent_records = fetch_json(url)
    print(agent_records)
    count += agent_records['count']
    num += agent_records['mean'] * agent_records['count']
  print('mean', num / count)
  print('count', count)
  return num / count

def calc_mean_and_standard_deviation(column):
  mean = calc_mean(column)
  sigma = float(0)
  count = 0
  for agent in agents:
    url = agent + '/api/sigma?column=' + column + '&mean=' + str(mean)
    print(url)
    agent_records = fetch_json(url)
    print(agent_records)
    sigma += agent_records['sigma']
    count += agent_records['count']
  standard_deviation = (sigma / count) ** 0.5
  print(standard_deviation)
  result = {}
  result['mean'] = mean
  result['count'] = count
  result['standard_deviation'] = standard_deviation
  return result

#calc_histogram('FEAT_ED_OD')
#calc_count()
#calc_mean('FEAT_VITAL_DBP_FIRST')
#calc_standard_deviation('FEAT_VITAL_DBP_FIRST')

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
  data['count'] = calc_count()
  return jsonify(data)

@app.route('/api/mean')
def api_mean():
  column = request.args.get('column')
  if column is None:
    # Generates an "Access Denied" error
    abort(403)
  if column in sensetive:
    abort(403)
  result = calc_mean_and_standard_deviation(column)
  return jsonify(result)

if __name__ == '__main__':
  app.run(debug=True, port=port)
