import ast
import json
import boto3
import requests
from os import path
from s3Utils import s3Utils
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask import Flask, render_template, redirect, request, flash, jsonify, make_response, url_for

'''
##################################################################################################
#################################### Begin Application Globals ###################################
##################################################################################################
{'''

app = Flask(__name__)

mail = Mail(app)

client = boto3.client(
    service_name='secretsmanager',
    region_name='us-east-1'
)

env = 'dev'

creds = json.loads(client.get_secret_value(
    SecretId='loisaWebsiteEmailCreds'
)['SecretString'])

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = creds['username']
app.config['MAIL_PASSWORD'] = creds['password']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

postsPerPage = {
    '/home': 3,
    '/myPosts': 5
}

s3 = s3Utils({
    's3': boto3.client('s3'),
    'bucket': 'loisa-website',
    'env': 'dev'
})


'''}
##################################################################################################
##################################### End Application Globals ####################################
##################################################################################################
'''

'''
##################################################################################################
##################################### Begin Application Pages ####################################
##################################################################################################
{'''


####################################
# '/' - Redirects to '/home' page. #
####################################
@app.route('/')
def index():
    return make_response(redirect('/home'), 302)
 

#########################################################
# '/home' - Home page responsible for displaying posts. #
#                                                       #
# 'Referenced In' - 'index.html'                        #
#########################################################
@app.route('/home')
def home():
    posts, titles, length = s3.getPosts(postsPerPage['/home'], 0)

    carouselSlides = s3.getCarousel()
    
    return make_response(render_template(
        'home.html', 
        posts=posts, 
        nextIndex=postsPerPage['/home'],
        prevIndex=0,
        numPosts=length,
        slides=carouselSlides,
        titles=titles,
        env=env
    ), 200)


########################################################
# '/about' - About page responsible for reading in     #
#            'templates/aboutMe.json' file and passing #
#            the data into 'about.html' file.          #
#                                                      #
# 'Referenced In' - 'index.html'                       #
########################################################
@app.route('/about')
def about():
    return make_response(render_template(
        'about.html',
        about=s3.getAbout(),
        env=env
    ), 200)


######################################################
# '/contact' - Contact page responsible for allowing # 
#            users to send personal messages.        #
#                                                    #
# 'Referenced In' - 'index.html'                     #
######################################################
@app.route('/contact')
def contact():
    return make_response(render_template(
        'contact.html',
        contact=s3.getContact(),
        env=env
    ), 200)


###########################################################
# '/post' - Page responsible for displaying user-selected # 
#           post.                                         #
#                                                         #
# 'Referenced In' - 'index.html'                          #
###########################################################
@app.route('/post', methods=['GET'])
def post():
    return make_response(render_template(
        'post.html'
    ), 200)


#####################################################
# '/myPosts' - Page responsible for displaying all  #
#              existing posts.                      #
#                                                   #
# 'Referenced In' - 'index.html'                    #
#####################################################
@app.route('/myPosts', methods=['GET'])
def myPosts():
    posts, titles, length = s3.getPosts(postsPerPage['/myPosts'], 0)
    
    return make_response(render_template(
        'myPosts.html', 
        posts=posts, 
        nextIndex=postsPerPage['/myPosts'],
        prevIndex=0,
        numPosts=length,
        titles=titles,
        env=env
    ), 200)


'''}
##################################################################################################
###################################### End Application Pages #####################################
##################################################################################################
'''

'''
##################################################################################################
##################################### Begin Application Routes ###################################
##################################################################################################
{'''


#########################################################
# '/contact/message' - contactMessage route responsible # 
#                      for receiving user message and   #
#                      responding to his/her e-mail.    #
#                                                       #
# 'Referenced In' - 'contact.js'                        #
#########################################################
@app.route('/contact/message', methods=['POST'])
def contactMessage():
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
        mail.send(msg)
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


##########################################################
# '/carousel' - Route responsible for taking in carousel #
#               file and then saving it either the dev   #
#               site or the prod site.                   #
#                                                        #
# 'Referenced In' - 'home.js'                            #
##########################################################
@app.route('/carousel', methods=['POST'])
def carousel():
    inputFile = request.files["inputFile"]
    
    if request.form['button'] == 'addToDevBtn':
        print "Adding carousel to dev!"
        filePath = s3.uploadCarousel('dev/pages/carousel.json', inputFile)
    elif request.form['button'] == 'addToProdBtn':
        print "Adding carousel to prod!"
        filePath = s3.uploadCarousel('prod/pages/carousel.json', inputFile)

    return make_response(jsonify(
        "Success!"
    ), 200)


#############################################################
# '/about/update' - Route responsible for taking in about   #
#                   file and then saving it either the dev  #
#                   site or the prod site.                  #
#                                                           #
# 'Referenced In' - 'about.js'                              #
#############################################################
@app.route('/about/update', methods=['POST'])
def aboutUpdate():
    inputFile = request.files["inputFile"]
    
    filename = 'about.json'
    
    if request.form['button'] == 'addToDevBtn':
        print "Updating about page in dev!"
        filePath = path.join(app.config['DEV_FOLDER'], filename)
    elif request.form['button'] == 'addToProdBtn':
        print "Updating about page in prod!"
        filePath = path.join(app.config['PROD_FOLDER'], filename)

    inputFile.save(filePath)

    return make_response(jsonify(
        "Success!"
    ), 200)


###############################################################
# '/contact/update' - Route responsible for taking in contact #
#                     file and then saving it either the dev  #
#                     site or the prod site.                  #
#                                                             #
# 'Referenced In' - 'contact.js'                              #
###############################################################
@app.route('/contact/update', methods=['POST'])
def contactUpdate():
    inputFile = request.files["inputFile"]
    
    filename = 'contact.json'
    
    if request.form['button'] == 'addToDevBtn':
        print "Updating contact page in dev!"
        filePath = path.join(app.config['DEV_FOLDER'], filename)
    elif request.form['button'] == 'addToProdBtn':
        print "Updating contact page in prod!"
        filePath = path.join(app.config['PROD_FOLDER'], filename)

    inputFile.save(filePath)

    return make_response(jsonify(
        "Success!"
    ), 200)


###############################################################
# '/myPosts/update' - Route responsible for taking in myPosts #
#                     file and then saving it either the dev  #
#                     site or the prod site.                  #
#                                                             #
# 'Referenced In' - 'myPosts.js'                              #
###############################################################
@app.route('/myPosts/update', methods=['POST'])
def myPostsUpdate():
    inputFile = request.files["inputFile"]
    
    filename = secure_filename(inputFile.filename)
    
    if request.form['button'] == 'addToDevBtn':
        print "Adding blog post in dev!"
        filePath = path.join(app.config['DEV_POSTS_FOLDER'], filename)
    elif request.form['button'] == 'addToProdBtn':
        print "Adding blog post in prod!"
        filePath = path.join(app.config['PROD_POSTS_FOLDER'], filename)

    inputFile.save(filePath)

    return make_response(jsonify(
        "Success!"
    ), 200)


###########################################################
# '/post/next' - Route responsible for reading in and     #
#                updating index of next posts to display. #
#                                                         #
# 'Referenced In' - 'index.js'                            #
###########################################################
@app.route('/post/next', methods=["POST"])
def postNext():
    nextIndex = int(request.json['nextIndex'])
    source = request.json['source']
    
    posts, titles, length = s3.getPosts(nextIndex+postsPerPage[source], nextIndex)
    
    posts = render_template('includeFiles/posts.html', posts=posts, titles=titles)
    
    return make_response(jsonify({
        'nextIndex' : str(nextIndex+postsPerPage[source]),
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
@app.route('/post/prev', methods=["POST"])
def postPrevious():
    prevIndex = int(request.json['prevIndex'])
    source = request.json['source']
    
    posts, titles, length = s3.getPosts(prevIndex, prevIndex-postsPerPage[source])
    
    posts = render_template('includeFiles/posts.html', posts=posts, titles=titles)
    
    return make_response(jsonify({
        'nextIndex' : str(prevIndex),
        'prevIndex' : str(prevIndex-postsPerPage[source]),
        'posts' : posts
    }), 200)


##################################################################
# '/post/get' - Route responsible for passing selected post into #
#               'postGetTemplate' file and writing it to         #
#               'templates/includeFiles/postGet.html' file.      #
#                                                                #
# 'Referenced In' - 'index.js'                                   #
##################################################################
@app.route('/post/get', methods=['POST'])
def postGet():
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


###################################################################
# '/youtubeFeed' - Route responsible for reaching out to youTube  #
#                  and grabbing videos, and then setting the      #
#                  width for displaying on page.                  #
#                                                                 #
# 'Referenced In' - 'home.js'                                    #
###################################################################
@app.route('/youtubeFeed', methods=['POST'])
def youtubeFeed():
    screenWidth = request.json['screenWidth']
    
    # data = str(requests.get('https://www.youtube.com/user/palcu08/videos').content).split(' ')
    # videos = list(set([line.replace('href="', 'https://www.youtube.com').replace('watch?v=', 'embed/').replace('"', '') for line in data if 'href="/watch?' in line]))
    videos = ['https://www.youtube.com/embed/3q7mgIm6m0Y', 'https://www.youtube.com/embed/VeoZxlY1-W0', 'https://www.youtube.com/embed/CDVijTt8iNg', 'https://www.youtube.com/embed/ga9KThfMmiY', 'https://www.youtube.com/embed/92OioRIX9Go', 'https://www.youtube.com/embed/qYxpoZ1ebtQ', 'https://www.youtube.com/embed/3TBOxLJtWrM']
    # print videos
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
@app.route('/instagramFeed', methods=['POST'])
def instagramFeed():
    posts = list(request.json['posts'])
    
    # TODO: Make the displaying of videos on page way more mobile-friendly
    return make_response(jsonify(
        render_template('includeFiles/instagramFeed.html', 
            posts=posts[0:4]
        )
    ), 200)


'''}
##################################################################################################
###################################### End Application Routes ####################################
##################################################################################################
'''

###################################
# Main function where app is run. #
###################################
if __name__ == '__main__':
    public = '0.0.0.0'
    local = '127.0.0.1'
    app.secret_key = 'something'

    # UNIX command to end processes
    # ps -fA | grep python
        
    app.run(debug=True, host=public)

