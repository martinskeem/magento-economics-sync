import mysql.connector
import secrets


def read_state(process):
    cn = mysql.connector.connect(user=secrets.mysql_magentosync_user,
                                 host=secrets.mysql_magentosync_host,
                                 database=secrets.mysql_magentosync_database,
                                 password=secrets.mysql_magentosync_password)
    state_cursor = cn.cursor()
    state_query = ("SELECT state " 
                   "FROM state " 
                   "WHERE process = '{}'").format(process)
    state_cursor.execute(state_query)
    row = state_cursor.fetchone()
    state_cursor.close()
    cn.close()

    if row is None:
        return 0
    else:
        return row[0]


def set_state(process, value):
    cn = mysql.connector.connect(user=secrets.mysql_magentosync_user,
                                 host=secrets.mysql_magentosync_host,
                                 database=secrets.mysql_magentosync_database,
                                 password=secrets.mysql_magentosync_password)
    state_cursor = cn.cursor()
    state_query = ("INSERT INTO state (process, state) " 
                   "VALUES ('{}', {}) " 
                   "ON DUPLICATE KEY UPDATE "
                   "state = VALUES(state)").format(process, value)

    state_cursor.execute(state_query)
    cn.commit()
    state_cursor.close()
    cn.close()
