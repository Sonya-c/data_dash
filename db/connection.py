import pyodbc 

def conn():
    server = 'SONYA-LAPTOP'
    database = 'covid_db'
    username = 'sa'
    password = '123'

    conn_str = 'DRIVER={SQL Server};' + 'SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password

    try: 
        db = pyodbc.connect(conn_str)
        cursor = db.cursor()
        return db, cursor

    except Exception as e: 
        print("Connection ERROR = ", e)
        return e