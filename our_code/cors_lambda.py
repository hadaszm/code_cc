import json

def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'accept,accept-encoding,accept-language,access-control-request-method,connection,host,origin,sec-fetch-dest,sec-fetch-mode,sec-fetch-site,user-agent,content-type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
        },
        'body': json.dumps('')
    }