"""
this module contain the db manipulation interface
"""

try:
    import MySQLdb
except ImportError:
    print "please install the mysqldb module"

def get_db_connection():
    """
    this function used to get db connection
    """
    conn = None
    try:
        conn = MySQLdb.connect(
                host='localhost',
                user='root',
                passwd='123456',
                port=1306
                )
        cur = conn.cursor()
        cur.execute('CREATE DATABASE IF NOT EXISTS yagra')
        cur.close()
        conn.select_db('yagra')
    except MySQLdb.OperationalError as e:
        print e

    return conn

def init_db():
    """
    init yagra db, create the user table.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS user')
    sql = """
        CREATE TABLE user(
            id INT NOT NULL AUTO_INCREMENT,
            email VARCHAR(30) NOT NULL UNIQUE,
            password VARCHAR(64) NOT NULL,
            default_image VARCHAR(128),
            PRIMARY KEY (id)
        )
    """
    cur.execute(sql)
    cur.close()
    conn.close()

def get_user_by_id(id_):
    """
    get user data according user id.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    sql = 'SELECT * FROM user WHERE id = %s'
    count = cur.execute(sql, id_)
    result = None
    if count != 0:
        result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def get_user_by_email(email):
    """
    get user data according user email.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    sql = 'SELECT * FROM user WHERE email = %s'
    count = cur.execute(sql, email)
    result = None
    if count != 0:
        result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def add_user(email, password):
    """
    add one user into table.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    sql = 'INSERT INTO user(email, password) values(%s, %s)'
    cur.execute(sql, (email, password))
    conn.commit()
    cur.close()
    conn.close()

def change_default_image(id_, default_image):
    """
    change the default image of user
    """
    conn = get_db_connection()
    cur = conn.cursor()
    sql = 'UPDATE user set default_image = %s WHERE id = %s'
    cur.execute(sql, (default_image, id_))
    conn.commit()
    cur.close()
    conn.close()

def change_password(id_, password):
    """
    change the password of user
    """
    conn = get_db_connection()
    cur = conn.cursor()
    sql = 'UPDATE user SET password = %s WHERE id = %s'
    cur.execute(sql, (password, id_))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    #c = get_db_connection()
    #init_db()
    #add_user('wangxiang1124@gmail.com', '123456')
    #change_default_image(1, '00000000000.img')
    print get_user_by_email("wangxiang1124@gmail.com")
