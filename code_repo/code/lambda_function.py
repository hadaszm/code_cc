import os
import boto3
import logging
import code

def lambda_handler(event, context):

    FUNCTION_REGION = os.environ['awsRegion']

    s3Client = boto3.client('s3', region_name=FUNCTION_REGION)
    code_pipeline = boto3.client('codepipeline')
    bucket_name = 'bucketsstack-codebucket-19hb395eaolra'
    objects = list(list_bucket_objects(bucket_name,s3Client))
    if objects is None:
        code_pipeline.put_job_failure_result(jobId=event)
        return 'Complete.'
    try:
        for obj in objects:
            if obj["Key"][:-3] != 'zip':
                print(obj["Key"])
                res = s3Client.delete_object(Bucket=bucket_name, Key= obj["Key"])
                print(res)

        code_pipeline.put_job_success_result(jobId = event) 
        return 'Complete.'
    except Exception as e:
       code_pipeline.put_job_failure_result(jobId=event)
       return 'Complete.'
        
    
def list_bucket_objects(bucket_name,s3Client):
    try:
        response = s3Client.list_objects_v2(Bucket=bucket_name)
    except Exception as e:
        logging.error(e)
        return None
    return response['Contents']