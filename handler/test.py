import logging
import json

import utils.db as db
from base import BaseHandler

class TestHandler(BaseHandler):
    def prepare(self):
        super().prepare()

    def get(self):
        res = {
            'content': 'Hello sabi~!',
            'retcode': 0
        }
        self.write(res)
