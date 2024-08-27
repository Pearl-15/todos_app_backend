import json
import boto3
from botocore.exceptions import ClientError
import os
from utils.utils import * 
from todos.get import get
from todos import decimalencoder

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TODOTABLE')
# table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def update(event, context):
    data = json.loads(event['body'])

    # check if the item is exist in the database
    get_response = get(event, context)
    get_body = json.loads(get_response["body"])
    print("get_response ", get_response)
    if not get_body["data"]:
        response = buildResponse(404, "PUT")
        response["body"] = json.dumps(get_body, cls=decimalencoder.DecimalEncoder)
        return response

    update_expression = []
    expression_attribute_values = {}
    expression_attribute_names = {}
        
    # for key in ['title', 'content', 'status', 'date']:
    #     if key in data:

    #         # Use placeholder for reserved keywords
    #         if key == 'status':
    #             key_placeholder = '#status'
    #         elif key == 'date':
    #             key_placeholder = '#date'
    #         else:
    #             key_placeholder = key

    #         update_expression.append(f"{key_placeholder} = :{key}")
    #         expression_attribute_values[f":{key}"] = data[key]

    #         if key == 'status':
    #             expression_attribute_names['#status'] = key
    #         elif key == 'date':
    #             expression_attribute_names['#date'] = key

    for key in ['title', 'content', 'created_at', 'is_done', 'updated_at']:
        if key in data:
            key_placeholder = key
            update_expression.append(f"{key_placeholder} = :{key}")
            expression_attribute_values[f":{key}"] = data[key]
    
    if not update_expression:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "No valid attributes provided for update"})
        }

    update_expression_str = "SET " + ", ".join(update_expression)

    status_code = 200
    body = {}

    #get user_id 
    user_id = event['requestContext']['authorizer']['claims']['sub']

    try:
        result = table.update_item(
        Key={'user_id': user_id,'id': event['pathParameters']['id']},
        ExpressionAttributeValues=expression_attribute_values,
        # ExpressionAttributeNames=expression_attribute_names,
        UpdateExpression=update_expression_str,
        ReturnValues='ALL_NEW'
        )
        body = buildDefaultResponseBody(result['Attributes'], None, None)

    except ClientError as e:
        print("Client Error response ...", e.response)
        status_code, body = buildClientErrorResponseBody(e.response)
    
    response = buildResponse(status_code, "PUT")
    response["body"] = json.dumps(body, cls=decimalencoder.DecimalEncoder)

    return response



