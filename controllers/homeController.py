from flask import Blueprint, make_response, redirect, url_for, render_template
from flask_classful import FlaskView, route

class homeController(FlaskView):
    #
    # Constructor
    #
    def __init__(self, dict):
        self.s3Service = dict['s3Service']
        self.environment = dict['env']
        self.postsPerPage = dict['postsPerPage']

    ####################################
    # '/' - Redirects to '/home' page. #
    ####################################
    @route('/')
    def index(self):
        return make_response(redirect('/home'), 302)

    #########################################################
    # '/home' - Home page responsible for displaying posts. #
    #                                                       #
    # 'Referenced In' - 'index.html'                        #
    #########################################################
    @route('/home')
    def home(self):
        posts, length = self.s3Service.getPosts(self.postsPerPage['/home'], 0)

        carouselSlides = self.s3Service.getCarousel()
        
        return make_response(render_template(
            'home.html', 
            posts=posts, 
            nextIndex=self.postsPerPage['/home'],
            prevIndex=0,
            numPosts=length,
            slides=carouselSlides,
            env=self.environment
        ), 200)