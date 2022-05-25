import boto3
import os 

def handler(event, context):
    
    # event properties
    request_id = event["request_id"]
    request_time = event["request_time"]
    celebs = event["celeb_names"]
    print("requestId: " + request_id)
    print("requestIdTime: " + request_time)
    print(f"FoundCelebs: {celebs}")

    # environment and ssm variables    
    FUNCTION_REGION = os.environ['awsRegion']

    ssmClient = boto3.client('ssm', region_name=FUNCTION_REGION)
    dynamoDB_tablename = ssmClient.get_parameter(Name='/params/dynamoDbTable')['Parameter']['Value']

    # DynamoDB properties
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamoDB_tablename)

    # saving data in DynamoDB
    try:
        table.put_item(
          Item={
            'RequestId': request_id,
            "RequestTime": request_time,
            "FoundCelebs": celebs})
    except Exception as e:
        print("Unable to insert data into DynamoDB table: {e}")
        raise

    # return results
    return {
        'statusCode': 200,
        'body': "Successfully saved."
    }

