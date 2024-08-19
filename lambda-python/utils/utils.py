def buildResponse(status_code, method):

    response = {
            "statusCode": status_code,
            "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": method
            }
        }

    return response


def buildDefaultResponseBody(data, error, message):
    body = {
        "data": data,
        "error": error,
        "message": message
    }
    return body


def buildClientErrorResponseBody(error_response):

    status_code = error_response["ResponseMetadata"]["HTTPStatusCode"]
    body = buildDefaultResponseBody(None,error_response["Error"]["Code"],error_response["Error"]["Message"])

    return {"status_code": status_code, "body": body}
