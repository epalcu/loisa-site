import json
import glob
import ast

class s3Utils():
    #
    # Constructor
    #
    def __init__(self, dict):
        self.client = dict['s3']
        self.bucket = dict['bucket']
        self.env = dict['env']

        self.posts = None
        self.carouselSlides = None
        self.contact = None
        self.about = None


    #
    # Private Methods
    #
    def _getPost(self, bucket, key):
        keyContents = ast.literal_eval(self.client.get_object(Bucket=bucket, Key=key)['Body'].read())

        return keyContents

    
    def _uploadFile(self, fileName, file):
        return self.client.upload_fileobj(file, self.bucket, fileName)


    #
    # Public Methods
    #
    def getPosts(self, high, low):
        if not self.posts:
            self.posts = self.client.list_objects_v2(
                Bucket=self.bucket,
                Prefix='{0}/posts'.format(self.env)
            )['Contents'][1:]
            
        posts = [ast.literal_eval(self.client.get_object(Bucket=self.bucket, Key=post['Key'])['Body'].read()) for post in self.posts if post['Key'] != '{0}/posts/'.format(self.env)]
        
        l = len(self.posts)
        
        if self.env == 'prod':
            return posts[low:high], l

        titles = [post['Key'].replace('{0}/posts'.format(self.env), '') for post in self.posts if post['Key'] != '{0}/posts/'.format(self.env)]

        return posts[low:high], titles[low:high], l


    def getCarousel(self):
        if not self.carouselSlides:
            self.carouselSlides = self._getPost(self.bucket, '{0}/pages/carousel.json'.format(self.env))

        return self.carouselSlides


    def getContact(self):
        if not self.contact:
            self.contact = self._getPost(self.bucket, '{0}/pages/contact.json'.format(self.env))

        return self.contact


    def getAbout(self):
        if not self.about:
            self.about = self._getPost(self.bucket, '{0}/pages/about.json'.format(self.env))

        return self.about


    def uploadCarousel(self, fileName, file):
        self.carouselSlides = None

        return self._uploadFile(fileName, file)
    