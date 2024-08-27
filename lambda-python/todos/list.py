import json
import boto3
from botocore.exceptions import ClientError
import os
from utils.utils import *
from todos import decimalencoder

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TODOTABLE')

def list(event, context):
    print("List function event", event)

    #get user_id
    user_id = event['requestContext']['authorizer']['claims']['sub']


    body = {}
    status_code = 200
    try:
        print("Query DynamoDB ...")
        result = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id))
        body = buildDefaultResponseBody(result["Items"], None, None)
    except ClientError as e:
    # ClientError => error response provided by an AWS Service to Boto3 client's request
        print("client error ...")
        status_code, body = buildClientErrorResponseBody(e.response)
    except Exception as e:
        print("default exception error ...")
        status_code = 500
        body = buildDefaultResponseBody(None,"Unexpected Error",str(e))

    response = buildResponse(status_code, "GET")
    response["body"] = json.dumps(body,cls=decimalencoder.DecimalEncoder)

    return response