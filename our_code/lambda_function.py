import os
import boto3
import logging
def lambda_handler(event, context):

    FUNCTION_REGION = os.environ['awsRegion']
    job_id = event['CodePipeline.job']['id']
    s3Client = boto3.client('s3', region_name=FUNCTION_REGION)
    
    code_pipeline = boto3.client('codepipeline')
    bucket_name = 'bucketsstack-codebucket-19hb395eaolra'
    objects = list(list_bucket_objects(bucket_name,s3Client))
    if objects is None:
        code_pipeline.put_job_failure_result(jobId=job_id)
        return 'Complete.'
    cnt = 0
    try:
        for obj in objects:
            if obj["Key"][:-3] != 'zip':
                res = s3Client.delete_object(Bucket=bucket_name, Key= obj["Key"])
                cnt+=1
        print(f"deleted {cnt} files")
        code_pipeline.put_job_success_result(jobId = job_id) 
        return 'Complete.'
    except Exception as e:
       code_pipeline.put_job_failure_result(jobId=job_id)
       return 'Complete.'
        
    
def list_bucket_objects(bucket_name,s3Client):
    try:
        response = s3Client.list_objects_v2(Bucket=bucket_name)
    except Exception as e:
        logging.error(e)
        return None
    return response['Contents']