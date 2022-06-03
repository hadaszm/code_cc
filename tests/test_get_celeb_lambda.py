import unittest
from unittest.mock import patch, Mock
import os
import our_code.get_celebs_lambda as lam
from moto import mock_dynamodb2, mock_ssm
import boto3


class TestGetLambdaFunction(unittest.TestCase):
    def setUp(self):
        self.table_name = "table_name"
        self.response_ok = {'statusCode': 200, 'headers': {'Access-Control-Allow-Headers': 'accept,accept-encoding,accept-language,access-control-request-method,connection,host,origin,sec-fetch-dest,sec-fetch-mode,sec-fetch-site,user-agent,content-type',
                                                           'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'}, 'body': '{"Krzysztof Krawczyk": 1, "Piotr Adamczyk": 1, "Maryla Rodowicz": 1}'}
        self.response_no_key = {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': 'accept,accept-encoding,accept-language,access-control-request-method,connection,host,origin,sec-fetch-dest,sec-fetch-mode,sec-fetch-site,user-agent,content-type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
            },
            'body': "Internal server error encountered"
        }

    @patch.dict(os.environ, {"awsRegion": "us-east-1"})
    @mock_dynamodb2
    @mock_ssm
    def test_get_OK(self):
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
        item = {}
        item['RequestId'] = '00'
        item['FoundCelebs'] = ['Krzysztof Krawczyk', "Piotr Adamczyk"]
        table.put_item(Item=item)

        item = {}
        item['RequestId'] = '01'
        item['FoundCelebs'] = ['Maryla Rodowicz']
        table.put_item(Item=item)

        res = lam.handler({}, {})
        self.assertDictEqual(res, self.response_ok)

    @patch.dict(os.environ, {"awsRegion": "us-east-1"})
    @mock_dynamodb2
    @mock_ssm
    def test_no_key(self):
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
        item = {}
        item['RequestId'] = '00'
        item['no_key'] = 'Krzysztof Krawczyk'

        table.put_item(Item=item)
        res = lam.handler({}, {})
        self.assertDictEqual(res, self.response_no_key)


if __name__ == '__main__':
    unittest.main()
