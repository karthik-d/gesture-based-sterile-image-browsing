import ibm_db

dsn_hostname = "2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud"
dsn_uid = "jlr06722"
dsn_password = "VlN0yoUMB4fzESl4"
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"
dsn_port = "30756"
dsn_protocol = "TCPIP"

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY=SSL"
).format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_password)

def connect_db():
    conn = ibm_db.connect(dsn, "", "")
    return conn

def users_insert(name, username, email, password):
    conn = connect_db()
    sql = "INSERT INTO USERS(\"name\", \"username\", \"email\", \"password\") VALUES(?, ?, ?, ?)"
    stmt = ibm_db.prepare(conn, sql)
    params = (name, username, email, password)
    res = ibm_db.execute(stmt, params)
    return res

def users_fetch_by_email(email):
    conn = connect_db()
    sql = "SELECT \"name\", \"password\", \"username\" FROM USERS WHERE \"email\" = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, email)
    ibm_db.execute(stmt)
    result_set =ibm_db.fetch_assoc(stmt)
    return result_set   