from flask import Blueprint, make_response, redirect, url_for, render_template, request, jsonify
from flask_classful import FlaskView, route

class aboutController(FlaskView):
    #
    # Constructor
    #
    def __init__(self, dict):
        self.s3Service = dict['s3Service']
        self.environment = dict['env']
        self.postsPerPage = dict['postsPerPage']

    ########################################################
    # '/about' - About page responsible for reading in     #
    #            'templates/aboutMe.json' file and passing #
    #            the data into 'about.html' file.          #
    #                                                      #
    # 'Referenced In' - 'index.html'                       #
    ########################################################
    @route('/about')
    def about(self):
        return make_response(render_template(
            'about.html',
            about=self.s3Service.getAbout(),
            env=self.environment
        ), 200)