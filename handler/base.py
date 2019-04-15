import sys
import os
import json
import time
import logging
import netaddr
import re
import requests
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        remote_ip = netaddr.IPAddress(self.request.remote_ip)
        logging.info('remote ip: {0}'.format(remote_ip))
#        if not remote_ip.is_private() and not remote_ip.is_loopback():
#            raise tornado.web.HTTPError(403)

    def set_default_headers(self):
        self.set_header("Server", "PiggyWeather")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def get(self):
        raise tornado.web.HTTPError(404)

    def options(self):
        self.set_status(204)
        self.finish()

