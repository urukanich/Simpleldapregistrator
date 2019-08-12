# -*- coding: utf-8 -*-
import tornado.web
from tornado.ioloop import IOLoop
from tornado import gen 
import time
import os
import ldap3
from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_REPLACE
from ldap3 import Server, Connection, ALL, NTLM
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups as addUsersInGroups
import random
import json
from random import randint
from string import ascii_letters
import logging
import sys
sys.path.append("lib/")
import logger
import openldap
import activedirectory
@gen.coroutine
def async_sleep(seconds):
    yield gen.Task(IOLoop.instance().add_timeout, time.time() + seconds)

class DSHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        login = self.get_argument("login")
        password = self.get_argument("password")
        f = open("conf/config.json", "r")
        conf = f.read()
        try:
            conf = json.loads(conf)
        except ValueError:
            logger.error("Decoding config.json has failed! Invalid config!")
            conf = False
            ldapadd = False
        if conf != False:
            try:
                for i in conf["credentials"]:
                    host = i["host"]
                    bind_pass = i["password"]
                    bind_dn = i["bind_dn"]
                    base_dn = i["base_dn"]
                    ds_type = i["ds_type"]
                    try:
                        ssl = i["ssl"]
                        if ssl == "True":
                            ssl = True
                        else:
                            ssl = False
                    except:
                        ssl = False
                    try:
                        port = i["port"]
                        port = int(port)
                    except:
                        port = None
                    credentials = True
            except KeyError:
                logger.error("Reading credentials error! Verify that the credentials block exist in config and contain host, password, bind_dn, base_dn, ds_type!")
                credentials = False
                ldapadd = False
            if credentials != False:
                # define the server
                try:
                    if ssl == True:
                        s = Server(host, port=port, use_ssl = True, get_info=ALL)
                    elif ssl == False:
                        s = Server(host, port=port, get_info=ALL)  # define an unsecure LDAP server, requesting info on DSE and schema
                    # define the connection
                    c = Connection(s, user=bind_dn, password=bind_pass)
                    c.bind()
                    connect = True
                except:
                    logger.error("Unable connect to server!")
                    connect = False
                    ldapadd = False
                if connect != False:
                    if ds_type == "openldap":
                        ldapadd = openldap.create(conf,login,password,base_dn,c)
                        c.unbind()
                    elif ds_type == "activedirectory":
                        ldapadd = activedirectory.create(conf,login,password,base_dn,c)
                        c.unbind()
        if ldapadd == True:
            self.write("Success")
            self.finish()
        else:
            self.write("Failed")
            self.finish()

root = os.path.dirname(__file__)
application = tornado.web.Application([
    (r"/registrator", DSHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": root, "default_filename": "index.html"}),  
    ])


logging.getLogger('tornado.access').disabled = True
logger = logger.get_logger()
logger.info('Started')
application.listen(9999)
IOLoop.instance().start()