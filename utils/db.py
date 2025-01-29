import mysql.connector

import config


def createConnection():
    mydb = mysql.connector.connect(
        host=config.database_host,
        port=config.database_port,
        user=config.database_username,
        password=config.database_password,
        database=config.database_name
    )

    return mydb
