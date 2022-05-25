import json
import boto3
import os

def handler(event, context):

    try:
        protocol = 'email'

        # enivioroment ans ssm variables
        FUNCTION_REGION = os.environ['awsRegion']

        ssmClient = boto3.client('ssm', region_name=FUNCTION_REGION)
        topic_arn = ssmClient.get_parameter(Name='/params/reportTopicArn')['Parameter']['Value'] 

        # create topic from arn
        sns = boto3.resource('sns')    
        topic = sns.Topic(topic_arn)

        # get emailaddress from body
        email_address =  json.loads(event['body'])['emailAddress']
        
        # adding subscribtion
        try:
            subscription = topic.subscribe(
                Protocol=protocol, Endpoint=email_address, ReturnSubscriptionArn=True)
            print(f"Subscribed {protocol} {email_address}, to topic {topic.arn}.")
        except Exception as e:
            print(f"Couldn't subscribe {protocol} {email_address} to topic {topic.arn}.")
            raise            
                
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'accept,accept-encoding,accept-language,access-control-request-method,connection,host,origin,sec-fetch-dest,sec-fetch-mode,sec-fetch-site,user-agent,content-type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
            },
            'body': json.dumps('Successful subscription')
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