import json
import boto3
from botocore.exceptions import ClientError
import os
from utils.utils import *

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TODOTABLE')
# table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def list(event, context):
    print("List function")
    body = {}
    status_code = 200
    try:
        print("Scanning DynamoDB ...")
        result = table.scan()
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
    response["body"] = json.dumps(body)

    return response