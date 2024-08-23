import json
import boto3
from botocore.exceptions import ClientError
from utils.utils import *

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TODOTABLE')

def get(event, context):
    print("get id funciton...")

    #get user_id 
    user_id = event['requestContext']['authorizer']['claims']['sub']

    body = {}
    status_code = 200
    result = {}
    try:
        result = table.get_item(Key={'user_id': user_id, 'id': event['pathParameters']['id']})
        body = buildDefaultResponseBody(result['Item'], None, None)
    except ClientError as ce:
        status_code, body = buildClientErrorResponseBody(ce.response)
    except Exception as e:
        status_code = 404
        if (not 'Item' in result):
            body = buildDefaultResponseBody(None, "No Item Found ", "No Item Found in database")
        else:
            status_code = 500
            body = buildDefaultResponseBody(None, "Unexpected Error",str(e) )

    print("query result : ", result)

    response = buildResponse(status_code, "GET")
    response["body"] = json.dumps(body)
    return response

