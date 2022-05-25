import boto3
import os
from datetime import datetime
import json

def handler(event, context):

    try:
        # environment and ssm variables    
        FUNCTION_REGION = os.environ['awsRegion']

        ssmClient = boto3.client('ssm', region_name=FUNCTION_REGION)
        dynamoDB_tablename = ssmClient.get_parameter(Name='/params/dynamoDbTable')['Parameter']['Value']

        # DynamoDB properties
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(dynamoDB_tablename)

        # creating the report
        response = table.scan()
        data = response['Items']
        found_celebs_counts = {}

        for doc in data:
            for celeb_name in doc['FoundCelebs']:
                found_celebs_counts[celeb_name] = found_celebs_counts.get(celeb_name, 0) + 1

        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Headers': 'accept,accept-encoding,accept-language,access-control-request-method,connection,host,origin,sec-fetch-dest,sec-fetch-mode,sec-fetch-site,user-agent,content-type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
                },
            'body': json.dumps(found_celebs_counts)
        }
    
    except  Exception as err:
        
        print(err)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': 'accept,accept-encoding,accept-language,access-control-request-method,connection,host,origin,sec-fetch-dest,sec-fetch-mode,sec-fetch-site,user-agent,content-type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
            },
            'body': "Internal server error encountered"
        }