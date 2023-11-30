import psycopg2
from dotenv import load_dotenv
import os
import string
import random
load_dotenv()

class Post:
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
                    WHERE table_name = 'posts'
                );
            """

            self.cursor.execute(table_exists_query)
            table_exists = self.cursor.fetchone()[0]
            
            # If 'users' table does not exist, create it in the database
            if not table_exists:
                self.cursor.execute("CREATE TABLE posts (id SERIAL PRIMARY KEY, title VARCHAR(255) NOT NULL, content VARCHAR(255) NOT NULL, user_id VARCHAR(255) NOT NULL, url VARCHAR(255) NOT NULL, created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
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

    def create_post(self, title, content, user_id):
        url = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        self.cursor.execute("INSERT INTO posts (title, content, user_id, url) VALUES (%s, %s, %s, %s)", (title, content, user_id, url))
        self.conn.commit()
        return url

    def get_post(self, url):
        self.cursor.execute("SELECT * FROM posts WHERE url = %s", (url,))
        post = self.cursor.fetchone()
        if post:
            return {
                "id": post[0],
                "title": post[1],
                "content": post[2],
                "user_id": post[3],
                "url": post[4],
                "created_date": post[5],
                "updated_date": post[6]
            }
        else:
            return None

    
    def get_all_posts(self,user_id):
        self.cursor.execute("SELECT * FROM posts WHERE user_id = %s", (str(user_id),))
        posts = self.cursor.fetchall()
        if posts:
            return [{
                "id": post[0],
                "title": post[1],
                "content": post[2],
                "user_id": post[3],
                "url": post[4],
                "created_date": post[5],
                "updated_date": post[6]
            } for post in posts]
        else:
            return None
