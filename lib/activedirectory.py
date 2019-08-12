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
                            for i in conf["active_directory_settings"]:
                                objectClass = i["objectClass"]
                                objectClass = objectClass.split(",")
                                attribute = i["attribute"]
                                attribute = attribute.split(",")
                                activedirectory_settings = True
                        except KeyError:
                            logger.error("Reading active_directory_settings error! Verify that the active_directory_settings block exist in config and contain objectClass and attribute!")
                            openldap_settings = False
                            ldapadd = False
                        if activedirectory_settings != False:
                            attribute_values = {}
                            try:
                                default_attributes = conf["active_directory_attribute_values"]
                                attr = True
                            except:
                                attr = False
                            if attr != False:
                                for i in attribute:
                                    if i in default_attributes:
                                        attribute_values[i] = default_attributes[i]      
                                        if i == "userPassword":
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
                                            group_dn = i["group_dn"]
                                        except:
                                            logger.error("You must specify group_dn")
                                            group_dn = ""
                                    
                                    
                                    if group_dn != "":
                                        try:
                                            c.extend.microsoft.add_members_to_groups('cn='+login+','+base_dn, group_dn)
                                            c.entries
                                            groupadd = True
                                        except:
                                            groupadd = False
                                        if groupadd != True:
                                            logger.error("Invalid group_dn")
                                            logger.error(c.result)                                            
                                        else:
                                            if c.result["description"] != "success":
                                                logger.error(c.result)
                                            else:
                                                logger.info(c.result)
                        return ldapadd
