import json
import glob
import ast
import boto3

class secretsManagerService():
    #
    # Constructor
    #
    def __init__(self):
        self.client = boto3.client(
            service_name='secretsmanager',
            region_name='us-east-1'
        )


    #
    # Public Methods
    #
    def getSecretValue(self, secretId):
        return json.loads(self.client.get_secret_value(
            SecretId=secretId
        )['SecretString'])