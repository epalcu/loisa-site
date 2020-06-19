import json
from flask import Flask

class appConfigService():
    #
    # Constructor
    #
    def __init__(self, app, service):
        self.app = app
        self.secretsManagerService = service

    #
    # Public Methods
    #
    def configureApp(self, env):
        with open('./configs/{0}.json'.format(env)) as json_file: 
            config = json.load(json_file) 
        
        creds = self.secretsManagerService.getSecretValue(config['SECRETS_MANAGER_SECRET_ID'])

        self.app.config['MAIL_SERVER'] = config['MAIL_SERVER']
        self.app.config['MAIL_PORT'] = config['MAIL_PORT']
        self.app.config['MAIL_USERNAME'] = creds['username']
        self.app.config['MAIL_PASSWORD'] = creds['password']
        self.app.config['MAIL_USE_TLS'] = config['MAIL_USE_TLS']
        self.app.config['MAIL_USE_SSL'] = config['MAIL_USE_SSL']
        self.app.config['ENVIRONMENT'] = config['ENVIRONMENT']
        self.app.config['HOME_POSTS_PER_PAGE'] = config['HOME_POSTS_PER_PAGE']
        self.app.config['MYPOSTS_POSTS_PER_PAGE'] = config['MYPOSTS_POSTS_PER_PAGE']
        self.app.config['S3_BUCKET'] = config['S3_BUCKET']
        self.app.secret_key = config['APP_SECRET_KEY']

        return self.app