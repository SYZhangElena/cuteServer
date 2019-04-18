import logging
import json

import utils.db as db
from base import BaseHandler
from utils.db import get_event_list, insert_event, change_event, get_event_by_receiver, get_event_by_user

class CreateEventHandler(BaseHandler):
    def prepare(self):
        super().prepare()

    def post(self):
        res = {
            'retcode': 1
        }

        logging.info(self.request.body)
        try:
            params = json.loads(self.request.body)
            insert_event(params)
        except Exception as why:
            logging.info('Invalid post params')
            self.write(res)
            return
        else:
            res['retcode'] = 0
        self.write(res)



class ReceiveEventHandler(BaseHandler):
    def prepare(self):
        super().prepare()

    def post(self):
        res = {
            'retcode': 1
        }

        logging.info(self.request.body)
        try:
            params = json.loads(self.request.body)
            change_event(params)
        except Exception as why:
            logging.info('Invalid post params')
            self.write(res)
            return
        else:
            res['retcode'] = 0
        self.write(res)


class QueryEventHandler(BaseHandler):
    def prepare(self):
        super().prepare()

    async def get(self):
        res = {
            'events': [],
            'retcode': 1
        }
        events = get_event_list()
        if not events:
            return res
        res['events'] = events
        res['retcode'] = 0
        self.write(res)


class PublishByHandler(BaseHandler):
    def prepare(self):
        super().prepare()

    def post(self):
        res = {
            'events': [],
            'retcode': 1
        }

        logging.info(self.request.body)
        try:
            params = json.loads(self.request.body)
            res['events'] = get_event_by_user(params)
        except Exception as why:
            logging.info('Invalid post params')
            self.write(res)
            return
        else:
            res['retcode'] = 0
        self.write(res)


class HelpByHandler(BaseHandler):
    def prepare(self):
        super().prepare()

    def post(self):
        res = {
            'events': [],
            'retcode': 1
        }

        logging.info(self.request.body)
        try:
            params = json.loads(self.request.body)
            res['events'] = get_event_by_receiver(params)
        except Exception as why:
            logging.info('Invalid post params')
            self.write(res)
            return
        else:
            res['retcode'] = 0
        self.write(res)