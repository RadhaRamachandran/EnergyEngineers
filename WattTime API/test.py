import requests

ba = 'PJM'
url = 'https://api.watttime.org:443/api/v1/datapoints/?ba=PJM&start_at=2015-11-19T11%3A30%3A00&end_at=2015-11-19T12%3A00%3A00'

r = requests.get(url)
data = r.json()

print (data[u'results'])

