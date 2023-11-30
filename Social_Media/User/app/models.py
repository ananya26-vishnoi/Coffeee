import psycopg2
from dotenv import load_dotenv
import os
import string
import random
load_dotenv()

class User:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('PASSWORD'),
            host=os.environ.get('HOST'),
            port=os.environ.get('PORT')
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        try:

            # Check if the 'users' table already exists in the database
            table_exists_query = """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_name = 'users'
                );
            """

            self.cursor.execute(table_exists_query)
            table_exists = self.cursor.fetchone()[0]
            
            # If 'users' table does not exist, create it in the database
            if not table_exists:
                self.cursor.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, first_name VARCHAR(255) NOT NULL,last_name VARCHAR(255) NOT NULL,email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, user_token VARCHAR(255) NOT NULL)")
                self.conn.commit()

        except Exception as e:
            # Print and handle any exceptions that occur during table creation
            print(e)
            self.cursor.rollback()

        finally:
            # Close the database connection and instance after operations are done
            # self.cursor.close()
            # self.conn.close()
            print("Tables created successfully")

    def create_user(self, email, password,first_name,last_name):
        self.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = self.cursor.fetchone()
        if user is not None:
            return None
        
        user_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        self.cursor.execute("INSERT INTO users (email, password, user_token,first_name,last_name) VALUES (%s, %s, %s, %s, %s)", (email, password, user_token,first_name,last_name))
        self.conn.commit()
        return user_token
        
    def verify_user(self, user_token):
        self.cursor.execute("SELECT * FROM users WHERE user_token = %s", (user_token,))
        user = self.cursor.fetchone()
        if user is None:
            return None
        return {
            "user_id": user[0],
            "user_token": user[5],
            "first_name": user[1],
            "last_name": user[2]
        }
    
    def login(self, email, password):
        self.cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = self.cursor.fetchone()
        if user is None:
            return None
        
        user_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        self.cursor.execute("UPDATE users SET user_token = %s WHERE id = %s", (user_token, user[0]))
        self.conn.commit()
        return {
            "user_id": user[0],
            "user_token": user_token,
            "first_name": user[1],
            "last_name": user[2]
        }
