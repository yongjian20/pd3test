from flask import Flask
from flask_mysqldb import MySQL
import threading
"""
In your main program, create an instance of the SingletonDatabase class before assessing its functions
"""


class SingletonDatabase:
    __instance__ = None

    def __init__(self, app, hostip, user, password, dbname, port):
        app.config['MYSQL_HOST'] = hostip
        app.config['MYSQL_USER'] = user
        app.config['MYSQL_PASSWORD'] = password
        app.config['MYSQL_DB'] = dbname
        app.config['MYSQL_PORT'] = port
        self.mysql = MySQL(app)

        if SingletonDatabase.__instance__ is None:
            SingletonDatabase.__instance__ = self
        else:
            raise Exception("You cannot create another SingletonDatabase class")

    @staticmethod
    def get_instance():
        """ Static method to fetch the current instance. 
        """ 
        if SingletonDatabase.__instance__ == None:
            with threading.Lock():
                if SingletonDatabase.__instance__ == None:
                    SingletonDatabase()
        return SingletonDatabase.__instance__

    def getUserDetailsByEmail(self, email):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM User where email = %s", [email])
        myresult = cur.fetchone()
        return myresult

    def getUserDetailsWithoutPicByEmail(self, email):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT idUser, idUserType, Email, MobileNumber, DOB, FirstName, LastName, DisplayName, MailingAddress, DeliveryAddress, JoinDate, LastLoginDate, LoginAttempts, IPAddress, OtpStatus FROM User WHERE email = %s", [email])
        myresult = cur.fetchone()
        return myresult
    
    def getUserWalletBalance(self, UserID):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT SUM(Amount) FROM WalletTranscript WHERE idUser = %s", [str(UserID)])
        myresult = cur.fetchone()
        return myresult

    def executeSelectMultipleQuery(self, query):
        cur = self.mysql.connection.cursor()
        cur.execute(query)
        myresult = cur.fetchall()
        return myresult

    def executeSelectMultipleQueryWithParameters(self, query, values):
        cur = self.mysql.connection.cursor()
        cur.execute(query, values)
        myresult = cur.fetchall()
        return myresult

    def executeSelectOneQuery(self, query):
        cur = self.mysql.connection.cursor()
        cur.execute(query)
        myresult = cur.fetchone()
        return myresult

    def executeSelectOneQueryWithParameters(self, query, values):
        cur = self.mysql.connection.cursor()
        cur.execute(query, values)
        myresult = cur.fetchone()
        return myresult

    def executeInsertQueryWithParameters(self, query, values):
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(query, values)
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print("Problem inserting into database: " + str(e))
            return False

    def executeUpdateQueryWithParameters(self, query, values):
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(query, values)
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print("Problem Update into database: " + str(e))
            return False

    def executeDeleteQueryWithParameters(self, query, values):
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(query, values)
            self.mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print("Problem Delete into database: " + str(e))
            return False