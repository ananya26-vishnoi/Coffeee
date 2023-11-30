import psycopg2
from dotenv import load_dotenv
import os
import string
import random
load_dotenv()

class Social:
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
                    WHERE table_name = 'social'
                );
            """

            self.cursor.execute(table_exists_query)
            table_exists = self.cursor.fetchone()[0]
            
            # If 'users' table does not exist, create it in the database
            if not table_exists:
                self.cursor.execute("CREATE TABLE social (id SERIAL PRIMARY KEY, user_1 INT  NOT NULL ,user_2 INT  NOT NULL,interaction_type VARCHAR(255) NOT NULL,text TEXT, post_id INT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
                self.conn.commit()

        except Exception as e:
            # Print and handle any exceptions that occur during table creation
            print(e)
        finally:
            print("Tables created successfully")
    
    def create_interaction(self,user_1,user_2,interaction_type,text=None, post_id=None):
        # check if both user exists
        self.cursor.execute("SELECT * FROM users WHERE id = %s OR id = %s",(user_1,user_2))
        result = self.cursor.fetchall()
        if len(result) != 2:
            return "not_exists"
        
        # check if interaction is already present
        if post_id is None:
            self.cursor.execute("SELECT * FROM social WHERE user_1 = %s AND user_2 = %s AND interaction_type = %s",(user_1,user_2,interaction_type))
        else:
            self.cursor.execute("SELECT * FROM social WHERE user_1 = %s AND user_2 = %s AND interaction_type = %s AND post_id = %s",(user_1,user_2,interaction_type,post_id))
        result = self.cursor.fetchone()
        if result is not None:
            return "already_exists"

        # Check if post exists
        if post_id is not None:
            self.cursor.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
            result = self.cursor.fetchone()
            if result is None:
                return "post_not_exists"
        
        # create interaction
        self.cursor.execute("INSERT INTO social (user_1,user_2,interaction_type,text,post_id) VALUES (%s,%s,%s,%s,%s)",(user_1,user_2,interaction_type,text,post_id))
        self.conn.commit()

        return "done"
    
    def check_follow(self,user_1,user_2):
        self.cursor.execute("SELECT * FROM social WHERE user_1 = %s AND user_2 = %s AND interaction_type = 'Following'",(user_1,user_2))
        result = self.cursor.fetchone()
        if result is None:
            return False
        return True