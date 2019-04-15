#!/usr/bin/env python
#coding: utf-8
import sys
import os
import signal
import logging
import time
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, options

from settings import settings, logger
from urls import url_patterns

def handler(signum, frame):
    logging.warning("Caught signal {0}".format(signum))
    tornado.ioloop.IOLoop.instance().add_callback_from_signal(shutdown)

def shutdown():
    logging.info("Stopping http server")
    tornado.ioloop.IOLoop.instance().stop()

def changelog(signum, frame):
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    logfile = "{0}/app.log.{1}".format(settings["log_path"], time.strftime("%Y%m%d"))
    fh = logging.FileHandler(filename=logfile)
    fh.setFormatter(settings["log_format"])
    logger.setLevel(logging.INFO)
    logger.addHandler(fh)

def main():
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGUSR2, changelog)
    application = tornado.web.Application(url_patterns, **settings)
    global server

    server = tornado.httpserver.HTTPServer(application, xheaders=True)
    logging.info(options.port)
    logging.info(options.address)
    server.bind(options.port, options.address)
    server.start(0)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

