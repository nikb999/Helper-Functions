#!/usr/bin/python
# -*- coding: utf-8 -*-

#Library of common functions
import json, urllib2, re, time, datetime, sys, cgi, os, string, random, math
import locale
import base64
import hashlib
import sqlite3
from tempfile import TemporaryFile

from email.mime.text import MIMEText

from werkzeug.security import generate_password_hash, \
                              check_password_hash

#to enable debugging
import cgitb
# cgitb.enable()


    
# ###############################################################################
# ###############################################################################
#
#                SQL FUNCTIONS
#
# ###############################################################################
# ###############################################################################

# Open database connection
def sql_open_db(in_db=''):
    # # Fatcow DB
    # db_host="......fatcowmysql.com"
    # db_username="...."
    # db_password="..."
    # db_database="....."

    # AWS DB
    db_host="/home/ubuntu/..../"
    db_username=""
    db_password=""
    db_database=in_db
    db_host_db = db_host+db_database

    try:
        # FATCOW
        # db = MySQLdb.connect(db_host,db_username,db_password,db_database)

        # AWS - sqlite3 -- outside of Flask app framework.
        db = sqlite3.connect(db_host_db)
        
        cur = db.cursor()
        #cur.execute("SELECT VERSION()")
        cur.execute("SELECT SQLITE_VERSION()")

        ver = cur.fetchone()
        
        ptest( ( "Database version : %s " % ver ))
        return db            
    except:          
        # ptest(( "Error %d: %s" % (e.args[0],e.args[1]) ))
        return False

def sql_create_table():
    
    try:
        db = sql_open_db()
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
    except:
        return False

    # Drop table if it already exist using execute() method.
    try:
        cursor.execute("DROP TABLE IF EXISTS FM_MODEL")
    except:
        ptest("1. Issue with drop table")
        return False

    sql = """CREATE TABLE FM_MODELS (
             USERNAME  CHAR(50) NOT NULL,
             MODELNAME CHAR(112),
             MODELDATA TEXT,
             LASTSAVED TEXT,
             MODELTYPE CHAR(50)
             )"""
             
    try:
        cursor.execute(sql)
        # disconnect from server
        db.close()
        return True
    except:
        # ptest("2. Issue with table creation")
        # ptest(sql)
        return False
    
def sql_add_user(u_info):
    #module to add a user - get the data as a list 
    #open the database
    try:
        db = sql_open_db()
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
    except:
        # ptest('problem opening DB')
        # ptest(u_info)
        return False
 
    # Prepare SQL query to INSERT a record into the database.
    sql_1 = 'INSERT INTO FM_USERS(USERNAME, PASSWORD, EMAIL, REGTYPE) VALUES ( '
    #print '<p>',sql_1
    sql_2 = sql_1 + "'" + u_info[0] + "','" + u_info[1] + "','" + u_info[2] + "','" + u_info[3] + "'"
    #print '<p>',sql_2
    sql_3 = sql_2 + ' )'
    #print '<p>',sql_3

    sql = sql_3
    ptest(sql)
    
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
        ptest('1 Done with sql')
        # disconnect from server
        db.close()
        return True
    except:
        # Rollback in case there is any error
        db.rollback()
        ptest('2 Problem with sql')
        return False

def sql_get_userinfo(u_name):
    #module to get all users info
    #open the database
    try:
        db = sql_open_db()
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
    except:
        return False

    # Prepare SQL query to INSERT a record into the database.
    sql = "SELECT * FROM FM_USERS WHERE USERNAME = '"+u_name+"'"
    ptest( sql )
    
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        results = cursor.fetchall()
        # disconnect from server
        db.close()
        return results
    except:
        return False

def sql_update_password(u_info):
    #module to update password - data comes in as a list - name and new pswd
    #open the database
    try:
        db = sql_open_db()
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
    except:
        return False

    # Prepare SQL query to INSERT a record into the database.
    sql = "UPDATE FM_USERS SET PASSWORD = '"+u_info[1]+"' WHERE USERNAME = '"+u_info[0]+"'"
    #print '<p>',sql
    
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
        # disconnect from server
        db.close()
        ptest( ("1 Done with "+sql ))
        return True
    except:
        return False
 
def sql_update_registration(u_info):
    #module to get all users info
    #open the database
    try:
        db = sql_open_db()
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
    except:
        return False

    # Prepare SQL query to INSERT a record into the database.
    sql = "UPDATE FM_USERS SET REGTYPE = '"+u_info[1]+"' WHERE USERNAME = '"+u_info[0]+"'"
    #print '<p>',sql
    
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
        #print <p>1 Done with ",sql
        # disconnect from server
        db.close()
        return True
    except:
        return False
      
def sql_get_modelinfo_all(u_name):
    #module to get info for the models saved for a given user
    #open the database
    try:
        db = sql_open_db('fm_model.db')
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
    except:
        return False

    # Prepare SQL query to INSERT a record into the database.
    sql = "SELECT * FROM FM_MODELS WHERE USERNAME = '"+u_name+"'"
    sql3 = "SELECT * FROM FM_MODEL WHERE USERNAME = ?"
    args = [u_name]
    #ptest(sql)
    
    try:
        # Execute the SQL command
        #cursor.execute(sql)
        cursor.execute(sql3,args)
        # Commit your changes in the database
        results = cursor.fetchall()
        # disconnect from server
        db.close()
        return results
    except:
        return False

def sql_get_modelinfo(u_name,m_type):
    #module to get info for the models saved for a given user and model type
    #open the database
    try:
        db = sql_open_db('fm_model.db')
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
    except:
        return False

    # Prepare SQL query to INSERT a record into the database.
    # sql = "SELECT * FROM FM_MODELS WHERE USERNAME = '"+u_name+"' AND MODELTYPE = '"+m_type+"'"
    sql3 = "SELECT * FROM FM_MODEL WHERE USERNAME = ? AND MODELTYPE = ?"
    args = [u_name,m_type]
    
    try:
        # Execute the SQL command
        # cursor.execute(sql)
        cursor.execute(sql3,args)
        # Commit your changes in the database
        results = cursor.fetchall()
        # disconnect from server
        db.close()
        return results
    except:
        return False

def sql_process_model(m_info):
    #module to add or update a model - 
    #get the data as a list -- ADD/UPDATE/DELETE, USERNAME, MODELNAME, MODELDATA and MODELTYPE
    # time stamp placed automatically
    #open the database
    try:
        db = sql_open_db('fm_model')
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
    except:
        return False

    #replace all the ' with \' in the sql input
    #model_data = m_info[3].replace("'","''")
    # use the msqld.escape_string function to do this.
    #model_data = MySQLdb.escape_string(str(m_info[3]))
    model_data = m_info[3]

    # Prepare SQL query to INSERT a record into the database.
    if m_info[0].upper()=="ADD":
        sql_1 = 'INSERT INTO FM_MODEL (USERNAME, MODELNAME, MODELDATA, LASTSAVED, MODELTYPE) VALUES ( '
        ptest(sql_1)
        sql_2 = sql_1 + "'" + m_info[1] + "','" + m_info[2] + "','" + model_data + "',now()" + ",'" + m_info[4] + "'"
        sql3 = 'INSERT INTO FM_MODEL (USERNAME, MODELNAME, MODELDATA, LASTSAVED, MODELTYPE) VALUES (?,?,?,?,?)'
        args = [m_info[1],m_info[2],model_data,now(),m_info[4]]
    elif m_info[0].upper()=="UPDATE":
        sql3 = "UPDATE FM_MODEL SET MODELDATA = ? LASTSAVED = ? WHERE ( USERNAME = ? AND MODELNAME = ?)"
        args = [model_data,now(),m_info[1],m_info[2]]
    elif m_info[0].upper()=="DELETE":
        sql3 = "DELETE FROM FM_MODEL WHERE (USERNAME = ? AND MODELNAME = ?)"
        args = [m_info[1],m_info[2]]
    else:
        # sql = "DESCRIBE FM_MODELS"
        sql3 = "SELECT SQLITE_VERSION()"
        args = []
        
    try:
        # Execute the SQL command
        cursor.execute(sql3,args)
        # Commit your changes in the database
        db.commit()
        # disconnect from server
        db.close()
        return True
    except:
        # Rollback in case there is any error
        db.rollback()
        ptest(("2 Problem with ",sql))
        return False

def sql_get_maxmodels(utype=''):
    #module to define the max number of models that a user can store
    return 10
        
   
