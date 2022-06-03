import unittest
import json
import our_code.cors_lambda as lam


class TestCorsLambdaFunction(unittest.TestCase):
    def setUp(self) :
        self.expected_res = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'accept,accept-encoding,accept-language,access-control-request-method,connection,host,origin,sec-fetch-dest,sec-fetch-mode,sec-fetch-site,user-agent,content-type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
        },
        'body': json.dumps('')
    }
    def test_return_status(self):
        res = lam.handler({},{})
        self.assertDictEqual(res, self.expected_res)


