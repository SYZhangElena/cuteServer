from handler.base import BaseHandler
from handler.login import LoginHandler
from handler.signup import SignupHandler
from handler.test import TestHandler
from settings import settings

url_patterns = [
    (r"/login", LoginHandler),
    (r"/signup", SignupHandler),
    (r"/test", TestHandler),
    (r"/.*", BaseHandler)
]
