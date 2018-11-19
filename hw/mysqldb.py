#!/usr/bin/python3
import pymysql
from hw import configuration


def get_connection(configProps):
    try:
        conn = pymysql.connect(host=configProps['DB.host'], port=int(configProps['DB.port']),
                               user=configProps['DB.user'], passwd=configProps['DB.passwd'], db=configProps['DB.db'],
                               charset='utf8', autocommit=True)
        return conn
    finally:
        pass
if __name__ == "__main__":
    config = configuration.get_db_configuration('config.props')
    print(config)
    c = get_connection(config)
    c.close()