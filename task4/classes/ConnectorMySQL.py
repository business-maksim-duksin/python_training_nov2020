import mysql.connector
from classes.ConnectorBase import ConnectorBase


class ConnectorMySQL(ConnectorBase):
    """Class used to establish connection database"""
    @staticmethod
    def connect(config: dict):
        return mysql.connector.connect(**config)
