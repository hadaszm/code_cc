import unittest
from unittest.mock import patch, Mock
import os
import our_code.subscribe_reports_lambda as lam
from moto import mock_ssm, mock_sns
import boto3
import json


class TestSubscribeReportLambdaFunction(unittest.TestCase):
    def setUp(self):
        self.event = {'body': '{"emailAddress":"email@onet.pl"}'}
        self.table_name = "table_name"
        self.response_ok = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'accept,accept-encoding,accept-language,access-control-request-method,connection,host,origin,sec-fetch-dest,sec-fetch-mode,sec-fetch-site,user-agent,content-type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
            },
            'body': json.dumps('Successful subscription')
        }
        self.wrong_response = {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': 'accept,accept-encoding,accept-language,access-control-request-method,connection,host,origin,sec-fetch-dest,sec-fetch-mode,sec-fetch-site,user-agent,content-type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
            },
            'body': "Internal server error encountered"
        }

    @patch.dict(os.environ, {"awsRegion": "us-east-1"})
    @mock_ssm
    @mock_sns
    def test_OK(self):
        # mock boto3 ssm
        ssmClient = boto3.client('ssm', region_name="us-east-1")
        snsClient = boto3.client("sns", region_name="us-east-1")
        mock_topic = snsClient.create_topic(Name="mocktopic")
        topic_arn = mock_topic.get("TopicArn")
        ssmClient.put_parameter(Name='/params/reportTopicArn', Value=topic_arn)

        res = lam.handler(self.event, {})
        self.assertDictEqual(res, self.response_ok)

    @patch.dict(os.environ, {"awsRegion": "us-east-1"})
    @mock_ssm
    @mock_sns
    def test_exception(self):
        # mock boto3 ssm
        ssmClient = boto3.client('ssm', region_name="us-east-1")
        snsClient = boto3.client("sns", region_name="us-east-1")
        ssmClient.put_parameter(
            Name='/params/reportTopicArn', Value="wronng_topic")

        res = lam.handler(self.event, {})
        self.assertDictEqual(res, self.wrong_response)


if __name__ == '__main__':
    unittest.main()
