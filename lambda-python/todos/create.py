import json
import boto3
import uuid
import os
from botocore.exceptions import ClientError
from utils.utils import *

dynamodb = boto3.resource('dynamodb')

def create(event, context):

    data = json.loads(event['body'])

    # validation "title" field
    # if data["title"] is empty string or None , return error response
    if(not data["title"]):
        response = buildResponse(400, "POST")
        response["body"] = json.dumps(buildDefaultResponseBody(None,"Title is empty!", "Title cannot be empty, please provide title." ))
        return response

    # table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    table = dynamodb.Table('TODOTABLE')

    item = {
        'id': str(uuid.uuid1()),
        'date': data['date'],
        'title': data['title'],
        'content': data['content'],
        'status': data['status']
    }

    status_code = 200
    body = {}
    try:
        result = table.put_item(
            Item=item
        )
        print("result", result)
        body = buildDefaultResponseBody(item, None, None)
    except ClientError as e:
        print("Client Error response ...", e.response)
        status_code, body = buildClientErrorResponseBody(e.response)
        
    response = buildResponse(status_code, "POST")
    response["body"] = json.dumps(body)

    return response
