from handler.base import BaseHandler
from handler.login import LoginHandler
from handler.signup import SignupHandler
from handler.test import TestHandler
from handler.event import QueryEventHandler, CreateEventHandler, ReceiveEventHandler, PublishByHandler, HelpByHandler
from settings import settings

url_patterns = [
    (r"/login", LoginHandler),
    (r"/signup", SignupHandler),
    (r"/events/query", QueryEventHandler),
    (r"/events/create", CreateEventHandler),
    (r"/events/receive", ReceiveEventHandler),
    (r"/events/publishby", PublishByHandler),
    (r"/events/helpby", HelpByHandler),
    (r"/test", TestHandler),
    (r"/.*", BaseHandler)
]
