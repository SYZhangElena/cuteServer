import logging
import json

from base import BaseHandler
from utils.db import get_event_list, insert_event, change_event, get_event_by_receiver, get_event_by_user

class CreateEventHandler(BaseHandler):
    def prepare(self):
        super().prepare()

    def post(self):
        # 创建订单业务逻辑
        res = {
            'retcode': 1
        }

        logging.info(self.request.body)
        try:
            # 获取前端传来的数据
            params = json.loads(self.request.body)
            # 插入数据库
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
        # 接收订单
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
        # 获取所有未完成订单
        res = {
            'events': [],
            'retcode': 1
        }
        # 获取数据库中所有未完成订单
        events = get_event_list()
        if not events:
            return res
        # 将订单数据赋值并写到套接字中返回给前端
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