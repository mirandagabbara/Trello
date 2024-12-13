import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['boards', 'boardmembers', 'cards', 'lists', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path='flask_app/database/'):
        if purge:
            drop_order = ['cards', 'lists', 'boardmembers', 'boards', 'users']
            for table in drop_order:
                self.query(f"DROP TABLE IF EXISTS `{table}`;")

        sql_file_order = ['users.sql', 'boards.sql', 'boardmembers.sql', 'lists.sql', 'cards.sql']
        for sql_file_name in sql_file_order:
            with open(f"{data_path}create_tables/{sql_file_name}", 'r') as file:
                sql_script = file.read()
                self.query(sql_script)

        """
        csv_file_order = ['institutions.csv', 'positions.csv', 'experiences.csv', 'skills.csv']
        for csv_file_name in csv_file_order:
            with open(f"{data_path}initial_data/{csv_file_name}", 'r', newline='', encoding='utf-8-sig') as file:
                csv_data = list(csv.reader(file))
                if not csv_data:
                    continue
                headers = csv_data[0]
                rows = csv_data[1:]
                rows = [row for row in rows if any(field.strip() for field in row)]
                if not rows:
                    continue
                self.insertRows(table=csv_file_name.split('.')[0], columns=headers, parameters=rows)
        """

    
    def insertRows(self, table='table', columns=['x', 'y'], parameters=[['v11', 'v12'], ['v21', 'v22']]):
        sql = f"INSERT INTO `{table}` ({', '.join([f'`{col}`' for col in columns])}) VALUES ({', '.join(['%s'] * len(columns))})"
        cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            charset='latin1'
        )
        cur = cnx.cursor()
        cleaned_parameters = [[None if val.strip().upper() == 'NULL' else val for val in row] for row in parameters if len(row) == len(columns)]
        cur.executemany(sql, cleaned_parameters)
        cnx.commit()
        cur.close()
        cnx.close()
        """

    def getResumeData(self):
        resume_data = {}
        institutions = self.query("SELECT * FROM institutions")
        for institution in institutions:
            inst_id = institution['inst_id']
            resume_data[inst_id] = institution
            resume_data[inst_id]['positions'] = {}
            positions = self.query("SELECT * FROM positions WHERE inst_id = %s", parameters=[inst_id])
            for position in positions:
                position_id = position['position_id']
                resume_data[inst_id]['positions'][position_id] = position
                resume_data[inst_id]['positions'][position_id]['experiences'] = {}
                experiences = self.query("SELECT * FROM experiences WHERE position_id = %s", parameters=[position_id])
                for experience in experiences:
                    experience_id = experience['experience_id']
                    resume_data[inst_id]['positions'][position_id]['experiences'][experience_id] = experience
                    resume_data[inst_id]['positions'][position_id]['experiences'][experience_id]['skills'] = {}
                    skills = self.query("SELECT * FROM skills WHERE experience_id = %s", parameters=[experience_id])
                    for skill in skills:
                        skill_id = skill['skill_id']
                        resume_data[inst_id]['positions'][position_id]['experiences'][experience_id]['skills'][skill_id] = skill
        return resume_data
    """
        
    def getBoardsByUser(self, user_id):
        query = """
            SELECT b.board_id, b.name, b.owner_id
            FROM boards b
            JOIN boardmembers bm ON b.board_id = bm.board_id
            WHERE bm.user_id = %s
             """
        return self.query(query, [user_id])
    
    def addBoard(self, project_name, owner_id, member_emails):
        try:
            # Insert the board
            board_result = self.query(
                "INSERT INTO boards (name, owner_id) VALUES (%s, %s)", 
                [project_name, owner_id]
            )
            board_id = board_result[0]['LAST_INSERT_ID()'] if board_result else None

            if not board_id:
                raise ValueError("Failed to create the board.")

            # Add the owner as a member of the board
            self.query(
                "INSERT INTO boardmembers (board_id, user_id) VALUES (%s, %s)", 
                [board_id, owner_id]
            )

            # Add other members if provided
            for email in member_emails:
                email = email.strip()
                if email:  # Skip empty entries
                    user = self.query("SELECT user_id FROM users WHERE email = %s", [email])
                    if user:
                        user_id = user[0]['user_id']
                        self.query(
                            "INSERT INTO boardmembers (board_id, user_id) VALUES (%s, %s)", 
                            [board_id, user_id]
                        )

            # Add default lists
            default_lists = ["To Do", "Doing", "Completed"]
            for list_name in default_lists:
                self.query(
                    "INSERT INTO lists (board_id, name) VALUES (%s, %s)", 
                    [board_id, list_name]
                )

            return board_id
        except Exception as e:
            print(f"Error in addBoard: {e}")
            raise


    #######################################################################################
    # AUTHENTICATION RELATED
    #######################################################################################
    
    def createUser(self, email, password, role='user'):
        try:
            # Check if the user already exists
            existing_user = self.query("SELECT * FROM users WHERE email = %s", [email])
            print(f"Existing user check result: {existing_user}")

            if existing_user:
                return {'success': 0, 'error': 'User already exists'}

            # Hash the password
            encrypted_password = self.onewayEncrypt(password)
            print(f"Encrypted password: {encrypted_password}")

            # Insert the new user into the database
            result = self.query(
                "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)", 
                [email, encrypted_password, role]
            )
            print(f"Insert result: {result}")

            return {'success': 1}
        except Exception as e:
            print(f"Error in createUser: {e}")
            return {'success': 0, 'error': str(e)}



    def authenticate(self, email='me@email.com', password='password'):
        # Encrypt the provided password for comparison
        encrypted_password = self.onewayEncrypt(password)
        # Check for matching email and password
        user = self.query(
            "SELECT * FROM users WHERE email = %s AND password = %s", 
            [email, encrypted_password]
        )
        if user:
            return {'success': 1, 'user': user[0]}
        else:
            return {'success': 0, 'error': 'Invalid email or password'}


    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message
    

