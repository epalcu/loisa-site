from controllers.homeController import homeController
from controllers.contactController import contactController
from controllers.postsController import postsController
from controllers.socialController import socialController
from controllers.aboutController import aboutController

class controllerService():
    def __init__(self, app, dict):
        self.app = app
        self.init_argument = dict
        
    def registerControllers(self):
        homeController.register(self.app, init_argument=self.init_argument, route_base='/')
        contactController.register(self.app, init_argument=self.init_argument, route_base='/')
        postsController.register(self.app, init_argument=self.init_argument, route_base='/')
        socialController.register(self.app, init_argument=self.init_argument, route_base='/')
        aboutController.register(self.app, init_argument=self.init_argument, route_base='/')