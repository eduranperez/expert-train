const dynamoDb = require('aws-sdk/clients/dynamodb');
exports.lambdaHandler = async (event, context) => {
    try {
        const itemId = event.pathParameters.itemId;

        const params = {
            TableName: 'items',
            Key: {
              'pk': itemId
            }
        };

        const docClient = exports.getDynamoDbDocumentClient();
        
        console.log(JSON.stringify(params));
        const response = await docClient.get(params).promise();

        return {
            'statusCode': 200,
            'body': JSON.stringify({
                item: response
            })
        };
    } catch (err) {
        console.log(err);
        return {
            'statusCode': 500
        }
    }
};

exports.getDynamoDbDocumentClient = () => {
    console.log("Connecting to DB....");
    console.log(process.env.USE_LOCAL_DYNAMODB);
    if (process.env.USE_LOCAL_DYNAMODB == "true") {
        console.log('connecting to local instance');
        return new dynamoDb.DocumentClient({'endpoint': 'http://dynamo-local:8000'});
    } else {
        console.log('Connecting to cloud instance');
        return new dynamoDb.DocumentClient();
    }
}
