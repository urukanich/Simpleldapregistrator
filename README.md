# Simpleldapregistrator
Hello! It is a simple user registrator for your Active Directory or OpenLDAP server.
![alt text](https://github.com/urukanich/Simpleldapregistrator/blob/master/img/logo.png)
## Install

Install the following Python libraries:

  **pip install tornado ldap3**

Edit the conf/config.json file as shown in the examples.

Then run:

  **python Simpleldapregistrator.py**
  
Application works on TCP port 9999:

For example:

 **http://192.168.1.1:9999**

## Current Features

* Creating LDAP/AD account by users 
* Simple logging and error catch
* You can setup attributes of creating user in config file(like userAccountControl and homeDirectory)
* Automated adding user to specified group
