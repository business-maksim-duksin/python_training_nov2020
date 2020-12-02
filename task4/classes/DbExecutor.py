from classes.ConnectorBase import ConnectorBase


class DbExecutor:
    """ Class for enabling connection context managing and maybe executing queries through connection to database. """

    def __init__(self, conncector: ConnectorBase, config: dict):
        self.cnx = conncector.connect(config)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.close()

    # def exec(self, query, *args,  **kwargs):
    #     with self.cnx.cursor(**kwargs) as cursor:
    #         cursor.execute(query, *args)
    #
    # def exec_commit(self, query, *args, **kwargs):
    #     with self.cnx.cursor(**kwargs) as cursor:
    #         cursor.execute(query, *args)
    #         self.cnx.commit()
    #
    # def execmany(self, query, *args,  **kwargs):
    #     with self.cnx.cursor(**kwargs) as cursor:
    #         cursor.executemany(query, *args)
    #
    # def execmany_commit(self, query, *args, **kwargs):
    #     with self.cnx.cursor(**kwargs) as cursor:
    #         cursor.executemany(query, *args)
    #         self.cnx.commit()
