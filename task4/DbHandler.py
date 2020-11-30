import mysql.connector
from functools import wraps
from typing import List
from logging_config import log
from db_config import db_config


def exceptions_logging(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            # log.DEBUG(f.__name__, *args, **kwargs)
            return f(*args, **kwargs)
        except Exception as e:
            log.error(e)
            raise

    return wrapper


class DbHandler:
    """Class to handle all possible interactions with database within the scope of a given task (Task4)."""

    def __init__(self, from_scratch: bool = False):
        self.cnx = mysql.connector.connect(**db_config)
        self.db_name = db_config["database"]
        if from_scratch:
            self.__drop_database()
        self.create_database()

    def __drop_database(self):
        query = f"""DROP DATABASE IF EXISTS {self.db_name}"""
        with self.cnx.cursor() as cursor:
            cursor.execute(query, )

    def create_database(self, ):
        query = f"CREATE DATABASE IF NOT EXISTS {self.db_name}"
        with self.cnx.cursor() as cursor:
            cursor.execute(query, )
        query = f"USE {self.db_name}"
        with self.cnx.cursor() as cursor:
            cursor.execute(query, )

    def create_table_rooms(self):
        query = f"""CREATE TABLE IF NOT EXISTS rooms (
                    id INT NOT NULL ,
                    name VARCHAR(12) NOT NULL
                    )
                """
        with self.cnx.cursor() as cursor:
            cursor.execute(query, )

    def create_table_students(self):
        query = f"""CREATE TABLE IF NOT EXISTS students (
                    birthday DATETIME NOT NULL,
                    id INT NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    room INT NOT NULL,
                    sex enum('M', 'F') NOT NULL
                    )
                """
        with self.cnx.cursor() as cursor:
            cursor.execute(query, )

    def insert_room(self, dic: dict):
        query = """INSERT INTO rooms
                   (id, name)
                   VALUES (%(id)s, %(name)s)
                """
        with self.cnx.cursor() as cursor:
            cursor.execute(query, dic)
            self.cnx.commit()

    def insert_rooms(self, list_of_rooms: List[dict]):
        query = """INSERT INTO rooms
                   (id, name)
                   VALUES (%(id)s, %(name)s)
                """
        with self.cnx.cursor() as cursor:
            cursor.executemany(query, list_of_rooms)
            self.cnx.commit()

    def insert_student(self, dic: dict):
        query = """INSERT INTO students
                   (birthday, id, name, room, sex)
                   VALUES (%(birthday)s, %(id)s, %(name)s, %(room)s, %(sex)s)
                """
        with self.cnx.cursor() as cursor:
            cursor.execute(query, dic)
            self.cnx.commit()

    def insert_students(self, list_of_students: List[dict]):
        query = """INSERT INTO students
                   (birthday, id, name, room, sex)
                   VALUES (%(birthday)s, %(id)s, %(name)s, %(room)s, %(sex)s)
                """
        with self.cnx.cursor() as cursor:
            cursor.executemany(query, list_of_students)
            self.cnx.commit()

    def room_population(self):
        """список комнат и количество студентов в каждой из них"""
        query = """
                SELECT r.id, COUNT(s.id) as population
                FROM rooms AS r
                    LEFT JOIN students AS s
                        ON r.id = s.room
                GROUP BY r.id
                ORDER BY population DESC
                """
        with self.cnx.cursor(dictionary=True) as cursor:
            cursor.execute(query, )
            return cursor.fetchall()

    def top5_least_average_age(self):
        """top 5 комнат, где самые маленький средний возраст студентов"""
        query = """
                SELECT room,
                       AVG(DATEDIFF(NOW(), birthday)) AS avg_age
                FROM students
                GROUP BY room
                ORDER BY avg_age ASC
                LIMIT 5
                """
        with self.cnx.cursor(dictionary=True) as cursor:
            cursor.execute(query, )
            return cursor.fetchall()
    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.close()