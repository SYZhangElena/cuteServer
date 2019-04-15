import logging
import json

import utils.db as db
from base import BaseHandler

class LoginHandler(BaseHandler):
    def prepare(self):
        super(LoginHandler, self).prepare()

    def post(self):
        res = {
            'retcode': 1
        }

        logging.info(self.request.body)
        try:
            params = json.loads(self.request.body)
        except Exception as why:
            logging.info('Invalid post params')
            self.write(res)
            return

        if ('username' not in params) or ('passwd' not in params):
            self.write(res)
            return

        valid_passwd = db.get_passwd_by_username(params['username'])
        if valid_passwd == params['passwd']:
            res['retcode'] = 0
            self.write(res)
        else:
            self.write(res)

