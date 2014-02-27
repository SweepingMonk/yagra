"""
this module contain the db manipulation interface
"""
import md5
import ConfigParser
try:
    import MySQLdb
except ImportError:
    print "please install the mysqldb module"

CONFIG = ConfigParser.RawConfigParser()
CONFIG.read("../models/config.ini")
def get_install_status():
    """
    check install status
    """
    return CONFIG.getboolean("install", "first_install")

def set_install_status(status):
    """
    setting install status
    """
    CONFIG.set("install", "first_install", status)

def config_database(host, port, user, passwd, database):
    """
    change the config content
    """
    CONFIG.set("database", "host", host)
    CONFIG.set("database", "port", port)
    CONFIG.set("database", "user", user)
    CONFIG.set("database", "passwd", passwd)
    CONFIG.set("database", "db", database)

def save_config():
    """
    save the config to file
    """
    with open("../models/config.ini", "w") as configfile:
        CONFIG.write(configfile)

def get_db_connection():
    """
    this function used to get db connection
    """
    conn = None
    try:
        conn = MySQLdb.connect(
                host=CONFIG.get("database", "host"),
                user=CONFIG.get("database", "user"),
                passwd=CONFIG.get("database", "passwd"),
                port=CONFIG.getint("database", "port")
                )
        cur = conn.cursor()
        cur.execute('CREATE DATABASE IF NOT EXISTS {0}'
                .format(CONFIG.get("database", "db")))
        cur.close()
        conn.select_db(CONFIG.get("database", "db"))
        cur.close()
    except MySQLdb.OperationalError:
        print "error!"

    return conn

def init_db():
    """
    init yagra db, create the user table.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS user")
    sql = """
        CREATE TABLE user(
            id INT NOT NULL AUTO_INCREMENT,
            email VARCHAR(30) NOT NULL UNIQUE,
            password VARCHAR(64) NOT NULL,
            default_image VARCHAR(64),
            email_digest VARCHAR(64),
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
    sql = "SELECT * FROM user WHERE id = %s"
    return execute_sql(sql, id_)
def get_user_by_email(email):
    """
    get user data according user email.
    """
    sql = "SELECT * FROM user WHERE email = %s"
    return execute_sql(sql, email)

def get_user_by_email_digest(email_digest):
    """
    get user data according user email digest
    """
    sql = "SELECT * FROM user WHERE email_digest = %s"
    return execute_sql(sql, email_digest)

def add_user(email, password):
    """
    add one user into table.
    """
    sql = 'INSERT INTO user(email, password, email_digest) values(%s, %s, %s)'
    execute_sql(sql, email, password, md5.new(email).hexdigest())

def change_default_image(id_, default_image):
    """
    change the default image of user
    """
    sql = 'UPDATE user set default_image = %s WHERE id = %s'
    execute_sql(sql, default_image, id_)

def change_password(id_, password):
    """
    change the password of user
    """
    sql = "UPDATE user SET password = %s WHERE id = %s"
    execute_sql(sql, password, id_)

def execute_sql(sql, *args):
    """
    procedure of execute sql statement
    """
    conn = get_db_connection()
    cur = conn.cursor()
    result = None
    if cur.execute(sql, args) != 0:
        result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result

#if __name__ == '__main__':
    #c = get_db_connection()
    #init_db()
    #add_user('wangxiang1124@gmail.com', '123456')
    #change_default_image(1, '00000000000.img')
    #print get_user_by_email("wangxiang1124@gmail.com")
