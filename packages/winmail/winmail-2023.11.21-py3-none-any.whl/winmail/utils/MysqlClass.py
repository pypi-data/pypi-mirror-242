# -*- coding: utf-8 -*-

import pymysql


class MySqlDb:
    debug = False

    def __init__(self, host=None, port=None, user=None, pwd=None, db=None, charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db
        self.charset = charset
        self.conn = None
        self.c = None
        if host and port and user and db:
            self.open(host=self.host, port=self.port, user=self.user, pwd=self.pwd, db=self.db,
                      charset=self.charset)

    def open(self, host, port, user, pwd, db, charset):
        try:
            if self.debug:
                print(host, port, user, pwd, db, charset)
            self.conn = pymysql.connect(host=host, port=port, user=user, password=pwd, db=db,
                                        charset=charset)
        except Exception as e:
            print(host, port, user, pwd, db)
            raise Exception(e)

        if self.conn:
            self.c = self.conn.cursor()
            return True
        else:
            return False

    def execute(self, sql):
        # 执行Sql语言。
        if self.debug:
            print("""class MysqlDb self.DEBUG:\t execute: %s""" % str(sql))
        try:
            self.c.execute(sql)
            return True
        except Exception as e:
            if self.debug:
                print("""class MysqlDb self.DEBUG:\t ERROR: %s""" % str(e))
            return False

    def fetchall(self):

        result = self.c.fetchall()
        if self.debug:
            print(f"fetchall {result}")
        return result

    def fetchone(self):

        result = self.c.fetchone()
        if self.debug:
            print(f"fetchone {result}")
        return result

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
