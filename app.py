import sys
from flask_mail import Mail
from flask import Flask
from services.controllerService import controllerService
from services.appConfigService import appConfigService
from services.s3Service import s3Service
from services.secretsManagerService import secretsManagerService

###################################
# Main function where app is run. #
###################################
if __name__ == '__main__':
    public = '0.0.0.0'
    local = '127.0.0.1'

    environment = sys.argv[1]

    configService = appConfigService(Flask(__name__), secretsManagerService())
    app = configService.configureApp(environment)

    controllerService = controllerService(app,
    {
        'env': app.config['ENVIRONMENT'],
        's3Service': s3Service({
            'bucket': app.config['S3_BUCKET'],
            'env': app.config['ENVIRONMENT']
        }), 
        'postsPerPage': {
            '/home': app.config['HOME_POSTS_PER_PAGE'], 
            '/myPosts': app.config['MYPOSTS_POSTS_PER_PAGE'] 
        },
        'mailClient': Mail(app)
    })

    controllerService.registerControllers()
        
    app.run(debug=True, host=local)

