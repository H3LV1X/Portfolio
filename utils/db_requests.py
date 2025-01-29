from utils.db import createConnection


def getSQLFetchone(sql, params=None):
    db = createConnection()
    cursor = db.cursor()
    if params:
        cursor.execute(sql, params=params)
    else:
        cursor.execute(sql)
    result = cursor.fetchone()
    db.close()

    return result


def getSQLFetchall(sql, params=None):
    db = createConnection()
    cursor = db.cursor()
    if params:
        cursor.execute(sql, params=params)
    else:
        cursor.execute(sql)
    results = cursor.fetchall()
    db.close()

    return results


def addSQL(sql, params=None):
    db = createConnection()
    cursor = db.cursor()
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    db.commit()
    db.close()

    return True


def updateSQL(sql, params=None):
    db = createConnection()
    cursor = db.cursor()
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    db.commit()
    db.close()

    return True


def removeSQL(sql, params=None):
    db = createConnection()
    cursor = db.cursor()
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    db.commit()
    db.close()

    return True
