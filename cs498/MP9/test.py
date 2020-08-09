import csv
import requests
import json

url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp-9"

student = {
    "submitterEmail": "arthurl3@illinois.edu", #<Your coursera account email>
    "secret": "pdXe7aMeW0TveHDo"  # <Your secret token from coursera>
}

numFilteredEntries = 1274  # <The count of the filtered entries from 3.2>

viz1CsvPath = "mp9-viz1.csv"  # <Filepath for your tableau viz1 csv file>
viz2CsvPath = "mp9-viz2.csv" #<Filepath for your tableau viz2 csv file>

# The column ordering in the tsv file may not be preserved when you export the data.
# Therefore, please check and modify the respective column index below

viz1StopOverColumn = 0 #<0 if the first column is the airport title or else 1>
viz2ArrivalDelayColumn = 0 #<0 if the first column is the arrival delay or 1>

def readViz(filePath, keyColumn):
    viz1Data = {}
    valueColumn = int(not keyColumn)

    with  open(filePath, encoding="utf8", errors='ignore') as csvfile:
        reader = csv.reader((line.replace('\0','') for line in csvfile), delimiter='\t')
        header = reader.__next__()

        for row in reader:
            if len(row) == 2:
                viz1Data[row[keyColumn]] = int(row[valueColumn])

    return viz1Data


def sendToAutograder(payload):
    r = requests.post(url, data=json.dumps(payload))
    print(r.status_code, r.reason)
    print(r.text)

def main():
    viz1Data = readViz(viz1CsvPath, viz1StopOverColumn)
    viz2Data = readViz(viz2CsvPath, viz2ArrivalDelayColumn)

    payload = {}
    payload['student'] = student
    payload['numFilteredEntries'] = numFilteredEntries
    payload['viz1'] = viz1Data
    payload['viz2'] = viz2Data
    print(json.dumps(payload))
    sendToAutograder(payload)

if __name__== "__main__":
    main()
