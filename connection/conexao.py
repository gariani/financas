import psycopg2


class Conexao:
    def __init__(self):
        self.__pool = None

    @property
    def conn(self):
        if not self.__pool:
            self.__pool = psycopg2.connect(database="d73u6atflfqjbf",
                                           user="oivwavjrjjhwnx",
                                           password="c42a72b35ed8c8f96008da2be25f5f3f4d32f6bbe4fbec4e1555bcd3237b5da4",
                                           host="ec2-23-21-96-159.compute-1.amazonaws.com",
                                           port="5432")
            return self.__pool
        else:
            return self.__pool
