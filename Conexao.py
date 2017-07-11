from PoolConection import PostgresConnectionPool


class Conexao:
    def __init__(self):
        self.__pool: PostgresConnectionPool = None

    @property
    def conn(self):
        if not self.__pool:
            self.__pool = PostgresConnectionPool(
                "dbname='d73u6atflfqjbf' user='oivwavjrjjhwnx' "
                "host='ec2-23-21-96-159.compute-1.amazonaws.com' "
                "password='c42a72b35ed8c8f96008da2be25f5f3f4d32f6bbe4fbec4e1555bcd3237b5da4'", maxsize=3)
            return self.__pool
        else:
            return self.__pool
