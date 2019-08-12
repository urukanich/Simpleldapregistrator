import sys
import time
import os
import ldap3
from ldap3 import Server, Connection, ALL, MODIFY_ADD
import random
import json
from random import randint
from string import ascii_letters
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import logging
def create(conf,login,password,base_dn,c):
                        import logger
                        logging.getLogger('tornado.access').disabled = True
                        logger = logger.get_logger()
                        try:
                            for i in conf["openldap_settings"]:
                                objectClass = i["objectClass"]
                                objectClass = objectClass.split(",")
                                attribute = i["attribute"]
                                attribute = attribute.split(",")
                                openldap_settings = True
                        except KeyError:
                            logger.error("Reading openldap_settings error! Verify that the openldap_settings block exist in config and contain objectClass and attribute!")
                            openldap_settings = False
                            ldapadd = False
                        if openldap_settings != False:
                            attribute_values = {}
                            gidnumber=randint(0, 99999)
                            try:
                                default_attributes = conf["openldap_attribute_values"]
                                attr = True
                            except:
                                attr = False
                            if attr != False:
                                for i in attribute:
                                    if i in default_attributes:
                                        if i == "homeDirectory":
                                            try: 
                                                login.decode('ascii')
                                            except:
                                                if default_attributes[i].endswith("/"):
                                                    attribute_values[i] = default_attributes[i] + str(gidnumber)
                                                else:
                                                    attribute_values[i] = default_attributes[i] + "/" + str(gidnumber)
                                            else:
                                                if default_attributes[i].endswith("/"):
                                                    attribute_values[i] = default_attributes[i] + login
                                                else:
                                                    attribute_values[i] = default_attributes[i] + "/" + login
                                        else:
                                            attribute_values[i] = default_attributes[i]
                                    else:
                                        if i == "gidNumber":
                                            attribute_values[i] = gidnumber
                                        elif i == "uid":
                                            attribute_values[i] = login
                                        elif i == "uidNumber":
                                            attribute_values[i] = gidnumber
                                        elif i == "userPassword":
                                            attribute_values[i] = password
                            try:
                                c.add('cn='+login+','+base_dn, objectClass, attribute_values)
                                c.entries
                                ldapadd = True
                            except:
                                logger.error("LDAPObjectClassError: invalid object class or attribute!")
                                ldapadd = False
                            if ldapadd != False:
                                if c.result["description"] != "success":
                                    logger.error(c.result)
                                    ldapadd = False
                                else:
                                    logger.info(c.result)
                                try:
                                    group_settings = conf["default_group_settings"]
                                    group = True
                                except:
                                    group= False
                                if group != False:
                                    for i in group_settings:
                                        try:
                                            group_object_class = i["group_object_class"]
                                            group_dn = i["group_dn"]
                                        except:
                                            logger.error("You must specify group_object_class and group_dn")
                                            group_object_class = ""
                                            group_dn = ""
                                    if group_object_class == "posixGroup":
                                        try:
                                            c.modify(group_dn, {'memberUid': (MODIFY_ADD, [login])})
                                            c.entries
                                            groupadd = True
                                        except:
                                            groupadd = False
                                        if groupadd != True:
                                            logger.error("Invalid group_dn")
                                        else:
                                            if c.result["description"] != "success":
                                                logger.error(c.result)
                                            else:
                                                logger.info(c.result)
                                    elif group_object_class == "groupOfNames":
                                        try:
                                            c.modify(group_dn, {'member': (MODIFY_ADD, ['cn='+login+','+base_dn])})
                                            c.entries
                                            groupadd = True
                                        except:
                                            groupadd = False
                                        if groupadd != True:
                                            logger.error("Invalid group_dn")
                                        else:
                                            if c.result["description"] != "success":
                                                logger.error(c.result)
                                            else:
                                                logger.info(c.result)
                                    elif group_object_class == "groupOfUniqueNames":
                                        try:
                                            c.modify(group_dn, {'uniqueMember': (MODIFY_ADD, ['cn='+login+','+base_dn])})
                                            c.entries
                                            groupadd = True
                                        except:
                                            groupadd = False
                                        if groupadd != True:
                                            logger.error("Invalid group_dn")
                                        else:
                                            if c.result["description"] != "success":
                                                logger.error(c.result)
                                            else:
                                                logger.info(c.result)
                        return ldapadd