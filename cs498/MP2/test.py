import requests
import json
import uuid

url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp2"

payload = {
	# <post api for storing the graph>,
	"graphApi": "https://lakgkhfeeh.execute-api.us-east-1.amazonaws.com/prod/getdistance",
	"botName": "GetDistanceBot",  # <name of your Amazon Lex Bot>,
	"botAlias": "DistanceBotAlias", # <alias name given when publishing the bot>,
	# <cognito identity pool id for lex>,
	"identityPoolId": "us-east-1:5c67c013-15a4-4b1c-9b69-5b93c90454d2",
	"accountId": "530466304726", #<your aws account id used for accessing lex>,
	"submitterEmail": "arthurl3@illinois.edu", # <insert your coursera account email>,
	"secret": "FjkSzOpjz8UNMA9R",  # <insert your secret token from coursera>,
	"region": "us-east-1" #<Region where your lex is deployed (Ex: us-east-1)>
}
# cs498-mp2-arthur
# http://cs498-mp2-arthur.s3-website-us-east-1.amazonaws.com
# poolid: us-east-1_T9Zr29euN
# appclientid: 5krcdq32qdbgb8rru7o29jsgv0
# Role ARN: arn:aws:iam::530466304726:role/CityLambda
# arn:aws:dynamodb:us-east-1:530466304726:table/distances

# AWS.config.region = 'us-east-1'
# // Region
# AWS.config.credentials = new AWS.CognitoIdentityCredentials({
#     IdentityPoolId: 'us-east-1:5c67c013-15a4-4b1c-9b69-5b93c90454d2',
# })
# Invoke URL: https://lakgkhfeeh.execute-api.us-east-1.amazonaws.com/prod
# "body": "{\"graph\": \"New York->New Jersey,New Jersey->Boston,Boston->Philadelphia,New York->Washington,New York->Miami,New Jersey->Houston,Boston->Houston,Miami->Austin,Los Angeles->New Jersey,Los Angeles->Philadelphia,San Francisco->Las Vegas,Las Vegas->Washington,Houston->Las Vegas,Chicago->New Jersey,Los Angeles->Chicago\"}",
# {
# 	"graph": "Chicago->Urbana, Urbana->Springfield, Chicago->Lafayette"
# }

r = requests.post(url, data=json.dumps(payload))
# print(payload)
print(r.status_code, r.reason)
print(r.text)
