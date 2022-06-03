import unittest
from unittest.mock import patch, Mock
import os
import our_code.save_results_lambda as lam
from moto import mock_dynamodb2, mock_ssm
import boto3
import datetime


class TestSaveLambdaFunction(unittest.TestCase):
    def setUp(self):
        self.event = {
            'request_id': '00',
            'request_time': str(datetime.datetime.now()),
            'celeb_names': 'Krzysztof Krawczyk'
        }
        self.table_name = "table_name"
        self.response_ok = {
            'statusCode': 200,
            'body': "Successfully saved."
        }

    @patch.dict(os.environ, {"awsRegion": "us-east-1"})
    @mock_dynamodb2
    @mock_ssm
    def test_OK(self):
        # mock boto3 ssm
        ssmClient = boto3.client('ssm', region_name="us-east-1")
        ssmClient.put_parameter(
            Name='/params/dynamoDbTable', Value=self.table_name)

        # dynamoDB
        dynamodb = boto3.resource('dynamodb', 'us-east-1')
        table = dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': 'RequestId',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'RequestId',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        res = lam.handler(self.event, {})
        self.assertDictEqual(res, self.response_ok)



if __name__ == '__main__':
    unittest.main()
