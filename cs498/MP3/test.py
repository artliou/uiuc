import requests
import json
url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp3-test"
payload = {
        	"accountId": "389326344480",#<your aws account id used for accessing lex>,
		    "submitterEmail": "arthurl3@illinois.edu", # <insert your coursera account email>,
		    "secret": "rA47U0I4MgJBjJhQ",  # <insert your secret token from coursera>,
		    "ipaddress": "54.91.245.6:5000", #<Insert IP:Port of EKS Master>
    }
r = requests.post(url, data=json.dumps(payload))
print(r.status_code, r.reason)
print(r.text)
