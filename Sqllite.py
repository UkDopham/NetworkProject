# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 17:39:37 2020

@author: Antoine Delay
"""

import sqlite3
from sqlite3 import Error
class Sqllite:

    def create_connection(self,db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn
                
    def createDataUser(self,conn):
        conn = self.create_connection(r"usertest.db")
        cur = conn.cursor()
        sql =  "DROP TABLE IF EXISTS EmailUser;"
        cur.execute(sql)
        sql = ''' CREATE TABLE EmailUser (Username TEXT, Password TEXT, Server TEXT); '''
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid

    def createEmailData(self,conn):
        conn = self.create_connection(r"usertest.db")
        cur = conn.cursor()
        sql =  "DROP TABLE IF EXISTS EmailData;"
        cur.execute(sql)
        sql = ''' CREATE TABLE EmailData (Sender TEXT , Recever TEXT, Subject TEXT, DateP TEXT, Content TEXT); '''
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid

    def insertUser(self, user, conn):    
        params = (user.get_username(), user.get_password(), user.get_server())
        cur = conn.cursor()
        cur.execute("INSERT INTO EmailUser VALUES (?, ?, ?)", params)
        conn.commit()

    def insertData(self, email, conn):
        params = (email.get_sender(), email.get_recever(), email.get_subject(), email.get_date(), email.get_content())
        cur = conn.cursor()
        cur.execute("INSERT INTO EmailData VALUES (?, ?, ?, ?, ?)", params)
        conn.commit()

    def selectUser(self,conn):
        a = []
        cur = conn.cursor()
        cur.execute("SELECT * FROM EmailUser")
        rows = cur.fetchall()
        for row in rows:
            a.append(row)
            #print(row)
        return a

    def selectData(self, conn, user):
        a = []
        cur = conn.cursor()
        cur.execute("SELECT * FROM EmailData WHERE Recever = " + "'" + user.get_username()+ "'" )
        rows = cur.fetchall()
        for row in rows:
            a.append(row)
            #print(row)
        return a

    def selectDataOrderByDate(self, conn, user):        
        cur = conn.cursor()
        cur.execute("SELECT * FROM EmailData WHERE Recever = " + "'" + user.get_username() + "'" + " order by DateP")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    def selectDataOrderBySender(self, conn, user):        
        cur = conn.cursor()
        cur.execute("SELECT * FROM EmailData WHERE Recever = " +  "'" +user.get_username() + "'" + " order by upper(Sender)")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    def selectDataOrderBySubject(self, conn, user):        
        cur = conn.cursor()
        cur.execute("SELECT * FROM EmailData WHERE Recever = " +  "'" +user.get_username() + "'" + " order by upper(Subject)")
        rows = cur.fetchall()
        for row in rows:
            print(row)



    def close(self, conn):
        conn.close()
            
    #def __init__(self):
        #self.conn = self.create_connection(r"usertest.db")
        #with self.conn:
            #print(self.create_project(self.conn))
            #self.selectUser(self.conn)
            #select_project_by(conn, 1)
        #conn.close()