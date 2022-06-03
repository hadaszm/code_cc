import unittest
from unittest.mock import patch, Mock
import os
import our_code.send_report_lambda as lam
from moto import mock_dynamodb2, mock_ssm, mock_sns
import boto3
from datetime import datetime


class TestSendReportLambdaFunction(unittest.TestCase):
    def setUp(self):
        self.table_name = "table_name"
        self.response_ok = {
            'statusCode': 200,
            'body': "Report sent"
        }

    @patch.dict(os.environ, {"awsRegion": "us-east-1"})
    @mock_dynamodb2
    @mock_ssm
    @mock_sns
    def test_OK(self):
        # mock boto3 ssm
        ssmClient = boto3.client('ssm', region_name="us-east-1")
        snsClient = boto3.client("sns", region_name="us-east-1")
        mock_topic = snsClient.create_topic(Name="mocktopic")
        topic_arn = mock_topic.get("TopicArn")
        ssmClient.put_parameter(Name='/params/reportTopicArn', Value=topic_arn)
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
        item['FoundCelebs'] = ['Krzysztof Krawczyk']
        item["RequestTime"] = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        table.put_item(Item=item)
        res = lam.handler({}, {})
        self.assertDictEqual(res, self.response_ok)


if __name__ == '__main__':
    unittest.main()
