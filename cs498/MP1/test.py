from flask import Flask, request
import requests
import json

url = 'https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp1'

payload = {
		'ip_address1': '34.229.160.134:80', # <insert ip address:port of first EC2 instance>, 
		'ip_address2': '54.85.1.216:80', # <insert ip address:port of second EC2 instance>,
		'load_balancer' : 'MP1LB-942015379.us-east-1.elb.amazonaws.com', # <insert address of load balancer>,
		'submitterEmail':  'arthurl3@illinois.edu', # <insert your coursera account email>,
		'secret':  'r8rjPktUwK3xXygF'  # <insert your secret token from coursera>
		}

r = requests.post(url, data=json.dumps(payload))

print(r.status_code, r.reason)
print(r.text)

# Flask Server Implementation
application = Flask(__name__)
seedNumber = 0
		
@application.route("/", methods=['GET'])
def get():
	if request.method == "GET":
		return str(seedNumber)
	return ''

@application.route("/", methods=['POST'])
def post():
	global seedNumber
	if request.method == "POST":
		seedNumber = request.json["num"]
	return ''

# Main Application Run
if __name__ == "__main__":
	application.debug = True
	application.run('0.0.0.0', port='80')

# Usage
# sudo python test.py
# http://flask.palletsprojects.com/en/1.1.x/quickstart/
# export FLASK_APP=server.py
# flask run --host=0.0.0.0
# python -m flask

# curl -H "Content-Type: application/json"  --data '{"num":10}' 127.0.0.1:5000
#  http://XXXXXXXXXXXXXXXXXXX.amazonaws.com/
