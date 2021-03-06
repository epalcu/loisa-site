import requests
from flask import Blueprint, make_response, redirect, url_for, render_template, request, jsonify
from flask_classful import FlaskView, route

class socialController(FlaskView):
    #
    # Constructor
    #
    def __init__(self, dict):
        self.s3Service = dict['s3Service']
        self.environment = dict['env']
        self.postsPerPage = dict['postsPerPage']
        

    ###################################################################
    # '/youtubeFeed' - Route responsible for reaching out to youTube  #
    #                  and grabbing videos, and then setting the      #
    #                  width for displaying on page.                  #
    #                                                                 #
    # 'Referenced In' - 'home.js'                                    #
    ###################################################################
    @route('/youtubeFeed', methods=['POST'])
    def youtubeFeed(self):
        screenWidth = request.json['screenWidth']
        
        data = str(requests.get('https://www.youtube.com/user/palcu08/videos').content).split(' ')
        videos = list(set([line.replace('href="', 'https://www.youtube.com').replace('watch?v=', 'embed/').replace('"', '') for line in data if 'href="/watch?' in line]))
       
        # TODO: Make the displaying of videos on page way more mobile-friendly
        return make_response(jsonify(
            render_template('includeFiles/youtubeFeed.html', 
                videos=videos[0:4],
                screenWidth=int(screenWidth)
            )
        ), 200)


    ###################################################################
    # '/instagramFeed' - Route responsible for receiving posts from   #
    #                    client-side, and then setting the            #
    #                    width for displaying on page.                #
    #                                                                 #
    # 'Referenced In' - 'home.js'                                     #
    ###################################################################
    @route('/instagramFeed', methods=['POST'])
    def instagramFeed(self):
        posts = list(request.json['posts'])
        
        # TODO: Make the displaying of videos on page way more mobile-friendly
        return make_response(jsonify(
            render_template('includeFiles/instagramFeed.html', 
                posts=posts[0:4]
            )
        ), 200)