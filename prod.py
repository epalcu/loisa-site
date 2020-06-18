import ast
import json
import boto3
import requests
from s3Utils import s3Utils
from flask_mail import Mail, Message
from flask import Flask, render_template, redirect, request, flash, jsonify, make_response, url_for
from flask_classful import FlaskView, route
from services.controllerService import controllerService
from services.appConfigService import appConfigService

###################################
# Main function where app is run. #
###################################
if __name__ == '__main__':
    public = '0.0.0.0'
    local = '127.0.0.1'

    client = boto3.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )

    configService = appConfigService(Flask(__name__), client)
    app = configService.configureApp()
    
    controllerService = controllerService(app,
    {
        'env': app.config['ENVIRONMENT'],
        's3Client': s3Utils({
            's3': boto3.client('s3'),
            'bucket': 'loisa-website',
            'env': app.config['ENVIRONMENT']
        }), 
        'postsPerPage': {
            '/home': app.config['HOME_POSTS_PER_PAGE'], 
            '/myPosts': app.config['MYPOSTS_POSTS_PER_PAGE'] 
        },
        'mailClient': Mail(app)
    })

    controllerService.registerControllers()

    # UNIX command to end processes
    # ps -fA | grep python
        
    app.run(debug=True, host=local)

