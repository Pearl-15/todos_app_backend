import json
import boto3
import os
from botocore.exceptions import ClientError
from utils.utils import *
from todos.get import get

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TODOTABLE')
# table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def delete(event, context):
    status_code = 200
    body = {}

    # check if the item is exist in the database
    get_response = get(event, context)
    get_body = json.loads(get_response["body"])
    print("get_response ", get_response)
    if not get_body["data"]:
        response = buildResponse(404, "DELETE")
        response["body"] = json.dumps(get_body)
        return response
        
    try:
        result = table.delete_item(
            Key={'id': event['pathParameters']['id']}, 
            ReturnValues = "ALL_OLD",
            ReturnValuesOnConditionCheckFailure="ALL_OLD",
            ConditionExpression="attribute_exists(id)")
        print("result", result)
        body = buildDefaultResponseBody(None, None, "Item deleted successfully." )
    except ClientError as e:
        print("error response", e.response)
        status_code, body = buildClientErrorResponseBody(e.response)

    response = buildResponse(status_code, "DELETE")
    response["body"] = json.dumps(body)

    return response
    

