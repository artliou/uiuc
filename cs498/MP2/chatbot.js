// # import json

// # def lambda_handler(event, context):
// #     # TODO implement
// #     return {
// #         'statusCode': 200,
// #         'body': json.dumps('Hello from Lambda!')
// #     }

const AWS = require('aws-sdk')
const ddb = new AWS.DynamoDB.DocumentClient()

exports.handler = (event, context, callback) => {
    // if (!event.requestContext.authorizer) {
    //     errorResponse('Authorization not configured', context.awsRequestId, callback)
    //     return
    // }
    console.log(event)
    // console.log('received request: ' + event)
    // console.log('received request2: ' + event['currentIntent']['slots'])
    
    let slotSource = event['currentIntent']['slots']['slotSource']
    let slotDestination = event['currentIntent']['slots']['slotDestination']
    getDistance(slotSource, slotDestination).then((result) => {
        // console.log("Result", result)
        // console.log("Result's Distance", result.Item.distance)
        let distance = result.Item.distance
        callback(null, {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "SSML",
                    "content": distance
                },
            },
        })
    }).catch((err) => {
        console.error(err)
        errorResponse(err.message, context.awsRequestId, callback)
    })
}

function getDistance(sourceIn, destinationIn) {
    let key = sourceIn.concat(destinationIn)
    console.log("Key:", key)
    return ddb.get({
        "TableName": 'distances',
        "Key": {
            "distanceId": key
            // "source": sourceIn,
            // "destination": destinationIn,
        },
    }).promise()
}

function errorResponse(errorMessage, awsRequestId, callback) {
    callback(null, {
        statusCode: 500,
        body: JSON.stringify({
            Error: errorMessage,
            Reference: awsRequestId,
        }),
        headers: {
            'Access-Control-Allow-Origin': '*',
        },
    })
}
