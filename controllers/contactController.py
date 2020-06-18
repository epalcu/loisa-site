from flask import Blueprint, make_response, redirect, url_for, render_template
from flask_classful import FlaskView, route

class contactController(FlaskView):
    def __init__(self, dict):
        self.s3 = dict['s3Client']
        self.environment = dict['env']
        self.postsPerPage = dict['postsPerPage']
        self.mail = dict['mailClient']

    ######################################################
    # '/contact' - Contact page responsible for allowing # 
    #            users to send personal messages.        #
    #                                                    #
    # 'Referenced In' - 'index.html'                     #
    ######################################################
    @route('/contact')
    def contact(self):
        return make_response(render_template(
            'contact.html',
            contact=self.s3.getContact(),
            env=self.environment
        ), 200)

    #########################################################
    # '/contact/message' - contactMessage route responsible # 
    #                      for receiving user message and   #
    #                      responding to his/her e-mail.    #
    #                                                       #
    # 'Referenced In' - 'contact.js'                        #
    #########################################################
    @route('/contact/message', methods=['POST'])
    def contactMessage(self):
        name = request.json['name']
        email = request.json['email']
        message = request.json['message']
        emailSubscription = request.json['emailSubscription']

        # E-mail the user
        msg = Message(
            "It's Loisa :) Thanks for messaging me!",
            sender="elliaspalcu@gmail.com",
            recipients=[email]
        )

        msg.body = "Hey, I received your message! Just give me a few days to respond :)"

        try :
            self.mail.send(msg)
            message = "Message successfully sent!"
            code = 200
        except:
            message = "Message could not send!"
            code = 201
        
        # Add the user's e-mail to subscription list
        if emailSubscription:
            print "Adding {0} to e-mail list!".format(email)

        return make_response(jsonify(
            response={
                'message':  message,
                'statusCode': code
            }
        ), code)