import boto3
import os
from datetime import datetime
import io

def handler(event, context):

    report_minutes = 10

    # environment and ssm variables    
    FUNCTION_REGION = os.environ['awsRegion']

    ssmClient = boto3.client('ssm', region_name=FUNCTION_REGION)
    topic_arn = ssmClient.get_parameter(Name='/params/reportTopicArn')['Parameter']['Value']
    topic_region = topic_arn.split(':')[3]
    dynamoDB_tablename = ssmClient.get_parameter(Name='/params/dynamoDbTable')['Parameter']['Value']

    # DynamoDB properties
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamoDB_tablename)

    # creating the report
    response = table.scan()
    data = response['Items']
    now_time = datetime.now()
    found_celebs_counts = {}
    number_of_requests = 0

    for doc in data:
        requestTime = datetime.strptime(doc["RequestTime"], "%d-%m-%Y_%H-%M-%S")
        if (now_time - requestTime).total_seconds() / 60 <= report_minutes:
            number_of_requests +=1
            for celeb_name in doc['FoundCelebs']:
                found_celebs_counts[celeb_name] = found_celebs_counts.get(celeb_name, 0) + 1

    message = io.StringIO()
    message.write(f'Found celebrities from last {report_minutes} minutes report\n'.center(80))
    today = 'Date: ' + str(now_time.strftime('%Y-%m-%d %H:%M:%S'))
    message.write(today.center(80))
    message.write('\n\n')
   
    if len(found_celebs_counts) > 0:
        message.write(f'Found celebrities in {number_of_requests} requests\n')
        for celeb, count in found_celebs_counts.items():
            message.write(celeb + ": " + str(count) + " times")
            message.write('\n')
    else:
        message.write(f"No celebrities found in {number_of_requests} requests\n")
    
    # publishing message to the topic
    snsClient = boto3.client('sns', region_name=topic_region)

    response = snsClient.publish(
        TopicArn = topic_arn,
        Subject = 'Scheduled celebrities report',
        Message = message.getvalue() 
    )


    return {
        'statusCode': 200,
        'body': "Report sent"
    }
