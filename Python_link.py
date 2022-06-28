import MySQLdb as mdb

DBNAME="investment_firm"  # database name
#DBPORT=3306      # database port
DBHOST="localhost"  # database host
DBUSER="root"  # database user
DBPASS="batmanpn"  # database password

try:
    db= mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME)
    print("Connected to database")
    cur = db.cursor()
    cur.execute("SELECT * FROM clients")
    print("Executed query")
    for row in cur.fetchall():
        print(row)
except mdb.Error as e:
    print("Error %d: %s" % (e.args[0],e.args[1]))
