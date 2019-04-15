#coding: utf-8

import sys
import os
import time
import logging
import configparser as ConfigParser
import yaml
import tornado
from tornado.options import define, options

ROOT = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(ROOT, 'utils/'))
sys.path.append(os.path.join(ROOT, 'handler/'))

cfg = "{0}/config/MATRIX_ENV_CONF".format(ROOT)
config = ConfigParser.ConfigParser()
config.readfp(open(cfg))


define("port", default=int(config.get("base", "PORT")), help="listen port", type=int)
define("address", default=config.get("base", "IPADDR"), help="listen address")
options.logging = None
tornado.options.parse_command_line()

settings = {}

settings["app_root"] = ROOT
settings["config"] = config

settings["log_path"] = config.get("base", "MATRIX_APPLOGS_DIR").strip('"')
settings["log_format"] = logging.Formatter(fmt="%(asctime)s|%(levelname)s|%(process)d|%(message)s", datefmt="%Y/%m/%d %H:%M:%S")

logfile = "{0}/app.log.{1}".format(settings["log_path"], time.strftime("%Y%m%d"))
fh = logging.FileHandler(filename=logfile)
fh.setFormatter(settings["log_format"])
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(fh)
