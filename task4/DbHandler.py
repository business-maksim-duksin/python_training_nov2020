import mysql.connector
from functools import wraps
from typing import List
from logging_config import log
from db_config import db_config


def exceptions_logging(f):
    """ I don't know if i really have to log everything, but i cat if i do. """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            # log.debug(f.__name__, )
            return f(*args, **kwargs)
        except Exception as e:
            log.error(e)
            raise

    return wrapper


class DbHandler:
    """
    Class to handle all possible interactions with database within the scope of a given task (Task4)..


    __init__
    ----------
    :Bool from_scratch: If True then DROP DATATABLE IF EXISTS, False -> use existing

    """
    def __init__(self, from_scratch: bool = False):
        """
        :Bool from_scratch: If True then DROP DATATABLE IF EXISTS, False -> use existing
        """
        self.cnx = mysql.connector.connect(host=db_config["host"],
                                           password=db_config["password"],
                                           user=db_config["user"],
                                           )
        self.db_name = db_config["database"]
        if from_scratch:
            self.__drop_database()
        self.create_database()

    def __drop_database(self):
        query = f"""DROP DATABASE IF EXISTS {self.db_name}"""
        with self.cnx.cursor() as cursor:
            cursor.execute(query, )
            log.warning(f"DROPPED {self.db_name} IF EXISTS")

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

    def top5_max_diff_age(self):
        """top 5 комнат с самой большой разницей в возрасте студентов"""
        query = """
                WITH min_max AS
                (
                    SELECT room,
                           MAX(birthday) AS max_age,
                           MIN(birthday) AS min_age
                    FROM students
                    GROUP BY room
                )
                SELECT room,
                       MAX(DATEDIFF(max_age, min_age)) AS max_diff
                FROM min_max
                GROUP BY room
                ORDER BY max_diff DESC
                LIMIT 5
                """
        with self.cnx.cursor(dictionary=True) as cursor:
            cursor.execute(query, )
            return cursor.fetchall()

    def mixed_sex(self):
        """список комнат где живут разнополые студенты"""
        query = """
                SELECT room,
                       COUNT(DISTINCT(sex)) AS sex_dst
                FROM students
                GROUP BY room
                HAVING sex_dst > 1
                """
        with self.cnx.cursor(dictionary=True) as cursor:
            cursor.execute(query, )
            return cursor.fetchall()

    def add_indexes(self):
        """добавить использование PRIMERY KEY и FOREIGN KEY в таблицы"""
        query = """
                ALTER TABLE rooms ADD PRIMARY KEY (id)
                """
        with self.cnx.cursor() as cursor:
            cursor.execute(query, )
            self.cnx.commit()
        query = """
                ALTER TABLE students ADD PRIMARY KEY (id), 
                ADD FOREIGN KEY (room)  REFERENCES rooms (id)
                """
        with self.cnx.cursor() as cursor:
            cursor.execute(query, )
            self.cnx.commit()

    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.close()
