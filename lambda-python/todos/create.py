import json
import boto3
import uuid
import os
from botocore.exceptions import ClientError
from utils.utils import *

dynamodb = boto3.resource('dynamodb')

def create(event, context):

    print(event)

    data = json.loads(event['body'])

    # validation "title" field
    # if data["title"] is empty string or None , return error response
    if(not data["title"]):
        response = buildResponse(400, "POST")
        response["body"] = json.dumps(buildDefaultResponseBody(None,"Title is empty!", "Title cannot be empty, please provide title." ))
        return response

    table = dynamodb.Table('TODOTABLE')

    #get user_id 
    user_id = event['requestContext']['authorizer']['claims']['sub']

    item = {
        'user_id': user_id,
        'id': str(uuid.uuid1()),
        'created_at': data['created_at'],
        'title': data['title'],
        'content': data['content'],
        'is_done': data['is_done']
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
