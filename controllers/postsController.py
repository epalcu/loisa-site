import ast
import json
from flask import Blueprint, make_response, redirect, url_for, render_template, request, jsonify
from flask_classful import FlaskView, route

class postsController(FlaskView):
    def __init__(self, dict):
        self.s3 = dict['s3Client']
        self.environment = dict['env']
        self.postsPerPage = dict['postsPerPage']

    ###########################################################
    # '/post' - Page responsible for displaying user-selected # 
    #           post.                                         #
    #                                                         #
    # 'Referenced In' - 'index.html'                          #
    ###########################################################
    @route('/post', methods=['GET'])
    def post(self):
        return make_response(render_template(
            'post.html'
        ), 200)


    #####################################################
    # '/myPosts' - Page responsible for displaying all  #
    #              existing posts.                      #
    #                                                   #
    # 'Referenced In' - 'index.html'                    #
    #####################################################
    @route('/myPosts', methods=['GET'])
    def myPosts(self):
        posts, length = self.s3.getPosts(self.postsPerPage['/myPosts'], 0)

        return make_response(render_template(
            'myPosts.html', 
            posts=posts, 
            nextIndex=self.postsPerPage['/myPosts'],
            prevIndex=0,
            numPosts=length
        ), 200)

    ###########################################################
    # '/post/next' - Route responsible for reading in and     #
    #                updating index of next posts to display. #
    #                                                         #
    # 'Referenced In' - 'index.js'                            #
    ###########################################################
    @route('/post/next', methods=["POST"])
    def postNext(self):
        nextIndex = int(request.json['nextIndex'])
        source = request.json['source']
        
        posts, length = self.s3.getPosts(nextIndex+self.postsPerPage[source], nextIndex)
        
        posts = render_template('includeFiles/posts.html', posts=posts)
        
        return make_response(jsonify({
            'nextIndex' : str(nextIndex+self.postsPerPage[source]),
            'prevIndex' : str(nextIndex),
            'numPosts' : length,
            'posts' : posts
        }), 200)


    ################################################################
    # '/post/prev' - Route responsible for reading in and updating #
    #                index of previous posts to display.           #
    #                                                              #
    # 'Referenced In' - 'index.js'                                 #
    ################################################################
    @route('/post/prev', methods=["POST"])
    def postPrevious(self):
        prevIndex = int(request.json['prevIndex'])
        source = request.json['source']
        
        posts, length = self.s3.getPosts(prevIndex, prevIndex-self.postsPerPage[source])
        
        posts = render_template('includeFiles/posts.html', posts=posts)
        
        return make_response(jsonify({
            'nextIndex' : str(prevIndex),
            'prevIndex' : str(prevIndex-self.postsPerPage[source]),
            'posts' : posts
        }), 200)


    ##################################################################
    # '/post/get' - Route responsible for passing selected post into #
    #               'postGetTemplate' file and writing it to         #
    #               'templates/includeFiles/postGet.html' file.      #
    #                                                                #
    # 'Referenced In' - 'index.js'                                   #
    ##################################################################
    @route('/post/get', methods=['POST'])
    def postGet(self):
        if 'post' in request.json:
            post = ast.literal_eval(request.json['post'])
        elif 'carouselPost' in request.json:
            post = json.load(open('posts/' + str(request.json['carouselPost']), 'r'))

        postGet = render_template(
            'postGetTemplate.html', 
            post=post
        )
        
        with open('templates/includeFiles/postGet.html', 'w+') as htmlFile:
            htmlFile.write(postGet)
        
        htmlFile.close()

        return make_response(jsonify('Success!'), 200)