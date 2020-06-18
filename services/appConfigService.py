import json
from flask import Flask

class appConfigService():
    def __init__(self, app, client):
        self.app = app
        self.client = client

    def configureApp(self):
        creds = json.loads(self.client.get_secret_value(
            SecretId='loisaWebsiteEmailCreds'
        )['SecretString'])

        self.app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        self.app.config['MAIL_PORT'] = 465
        self.app.config['MAIL_USERNAME'] = creds['username']
        self.app.config['MAIL_PASSWORD'] = creds['password']
        self.app.config['MAIL_USE_TLS'] = False
        self.app.config['MAIL_USE_SSL'] = True
        self.app.config['ENVIRONMENT'] = 'prod'
        self.app.config['HOME_POSTS_PER_PAGE'] = 3
        self.app.config['MYPOSTS_POSTS_PER_PAGE'] = 5
        self.app.secret_key = 'something'

        return self.app