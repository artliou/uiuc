const randomBytes = require('crypto').randomBytes;

const AWS = require('aws-sdk');

const ddb = new AWS.DynamoDB.DocumentClient();

exports.handler = (event, context, callback) => {
    var distanceId;
    console.log('Received event (', distanceId, '): ', event);
    // function getDistanceId() {
    //     var distanceId = toUrlString(randomBytes(16));
    //     return distanceId
    // }
    // Because we're using a Cognito User Pools authorizer, all of the claims
    // included in the authentication token are provided in the request context.

    // The body field of the event in a proxy integration is a raw string.
    // In order to extract meaningful values, we need to first parse this string
    // into an object. A more robust implementation might inspect the Content-Type
    // header first and use a different parsing strategy based on that value.
    //parsing
    const requestBody = JSON.parse(event.body);
    // console.log("Body: ", requestBody)
    const graph = requestBody.graph;
    // console.log("Graph: ", graph)
    var edges = graph.split(",")
    console.log("Edges: ", edges)
    var edgeObjects = {}
    var parsedGraph = new Graph()
    for (var i = 0; i < edges.length; i++) {
        // distanceId = getDistanceId();
        let temp = edges[i].split("->")
        console.log("temps: ", temp)
        let obj = {
            distanceId: distanceId,
            source: temp[0],
            destination: temp[1],
            distance: 1
        }
        edgeObjects[i] = obj
        console.log("Object", obj, obj.source, obj.destination, obj.distance)
        parsedGraph.addVertex(obj.source)
        // console.log("Source Vertex Added")
        parsedGraph.addVertex(obj.destination)
        // console.log("Vertex Added - Destination")
        parsedGraph.addEdge(obj.source, obj.destination)
        // console.log("Edge Added")
        // putDistance(distanceId, obj.source, obj.destination, obj.distance)
        // console.log("Edge Done")
    }
    // console.log("Object: ", edgeObjects)
    // console.log("parsedGraph: ", parsedGraph)
    let allDistancesObject = []
    parsedGraph.calculateDistances(allDistancesObject)
    console.log("Object", allDistancesObject)
    allDistancesObject.forEach((edge) => {
        let //distanceId = edge[0], 
            source = edge[1], destination = edge[2], distance = edge[3];
        let distanceId = source.concat(destination)
        putDistance(distanceId, source, destination, distance).then(() => {
            // You can use the callback function to provide a return value from your Node.js
            // Lambda functions. The first parameter is used for failed invocations. The
            // second parameter specifies the result data of the invocation.

            // Because this Lambda function is called by an API Gateway proxy integration
            // the result object must use the following structure.
            callback(null, {
                statusCode: 200,
                body: JSON.stringify({
                    distanceId: distanceId,
                    source: source,
                    destination: destination,
                    distance: distance,
                    // User: username
                }),
                headers: {
                    'Access-Control-Allow-Origin': '*',
                },
            });
        }).catch((err) => {
            console.error(err);

            // If there is an error during processing, catch it and return
            // from the Lambda function successfully. Specify a 500 HTTP status
            // code and provide an error message in the body. This will provide a
            // more meaningful error response to the end client.
            errorResponse(err.message, context.awsRequestId, callback)
        });
    });
    // putDistance(distanceId, source, destination, distance, username).then(() => {
    //     // You can use the callback function to provide a return value from your Node.js
    //     // Lambda functions. The first parameter is used for failed invocations. The
    //     // second parameter specifies the result data of the invocation.

    //     // Because this Lambda function is called by an API Gateway proxy integration
    //     // the result object must use the following structure.
    //     callback(null, {
    //         statusCode: 200,
    //         body: JSON.stringify({
    //             distanceId: distanceId,
    //             source: source,
    //             destination: destination,
    //             distance: distance,
    //             // User: username
    //         }),
    //         headers: {
    //             'Access-Control-Allow-Origin': '*',
    //         },
    //     });
    // }).catch((err) => {
    //     console.error(err);

    //     // If there is an error during processing, catch it and return
    //     // from the Lambda function successfully. Specify a 500 HTTP status
    //     // code and provide an error message in the body. This will provide a
    //     // more meaningful error response to the end client.
    //     errorResponse(err.message, context.awsRequestId, callback)
    // });
};

function getDistanceId() {
    var distanceId = toUrlString(randomBytes(16));
    return distanceId;
}

function putDistance(distanceId, source, destination, distance, username) {
    return ddb.put({
        TableName: 'distances',
        Item: {
            distanceId: distanceId,
            source: source,
            destination: destination,
            distance: distance,
            // User: username
        },
    }).promise();
}

function toUrlString(buffer) {
    return buffer.toString('base64')
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=/g, '');
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
    });
}

class Graph {
    constructor() {
        this.AdjList = new Map();
        this.sources = []
    }

    addVertex(vertex) {
        if (!this.AdjList.has(vertex)) {
            this.AdjList.set(vertex, [])
            this.sources.push(vertex);
        } else {
            // console.log(`Vertex exists '${vertex}'`);
        }
    }

    addEdge(vertex, node) {
        if (this.AdjList.has(vertex)) {
            if (this.AdjList.has(node)) {
                let arr = this.AdjList.get(vertex);
                if (!arr.includes(node)) {
                    arr.push(node);
                }
            } else {
                throw `Can't add non-existing vertex ->'${node}'`;
            }
        } else {
            throw `You should add '${vertex}' first`;
        }
    }

    calculateDistances(allDistancesObject) {
        // console.log("Keys", typeof(keys), this.AdjList.keys(), keys)
        // console.log("Sources", this.sources)

        // keys.forEach(key => {
        //     console.log("Checking")
        //     if (this.AdjList[key].length == 0) {
        //         console.log("0 Key", this.AdjList[key])
        //     } else {
        //         sources.push(this.AdjList[key])
        //     }
        // })
        this.sources.forEach((source) => {
            // console.log("Source Check", source)
            BFS(this.AdjList, source)
        })
        // BFS(this.AdjList, this.sources[0])
        // console.log("Done First Source")
        function BFS(graph, node) {
            var level = new Map(); //To determine the level of each node
            var visited = []; //Mark the node if visited 
            // Create a Queue and add our initial node in it
            let q = []
            let explored = new Set();
            q.push(node)

            // Mark the first node as explored explored.
            explored.add(node);
            level[node] = 0;
            visited[node] = true;

            while (Array.isArray(q) && q.length) {
                //get first element
                let source = q.shift();
                let endValues = graph.get(source)
                // console.log("Vertex", source, endValues, graph)
                endValues.forEach((neighbor) => {
                    q.push(neighbor)
                    
                    let distance = level[source] + 1
                    level[neighbor] = distance
                    visited[neighbor] = true
                    // console.log("Distance from", source, "to", neighbor, level[neighbor])
                });
                // console.log("End Vertex Neighbor Check")
            }
            let keys = Object.keys(level)
            // console.log("Keys", keys)
            for (const destination of keys) {
                let distance = level[destination]
                // console.log(destination, distance)
                if (distance == 0) {
                    continue;
                }
                console.log("Added", node, "to", destination, distance)
                // let distanceId = getDistanceId();
                // console.log("DistanceId Generated", distanceId)

                // putDistance(distanceId, node, destination, distance)
                allDistancesObject.push([distanceId, node, destination, distance])
            }
            // console.log("Level", level)
            console.log("Finish BFS for:", node)
        }
    }
}
