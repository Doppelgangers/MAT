import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('database.db')
    cur = base.cursor()
    if base:
        print("Data base connekted")

def get_proxy ():
    proxys = cur.execute('SELECT * FROM proxys').fetchall()
    return proxys

async def get_count_twitters():
    tab = cur.execute('SELECT count(*) FROM twitters').fetchall()
    return str(tab[0][0])

async def get_count_proxys():
    tab = cur.execute('SELECT count(*)  FROM proxys').fetchall()

    return str(tab[0][0])

async def set_proxy ( login, password,ip,port ):
    table = cur.execute(f"SELECT * FROM proxys WHERE proxys.proxy = '{ip}' " ).fetchall()
    if table == []:
        cur.execute("INSERT INTO proxys (login,password, proxy,port )VALUES (? , ? , ? , ?)" , ( login, password,ip,port))
        base.commit()
        return True
    else:
        return False

async def set_twitter ( username ,password , mail ):
    table = cur.execute(f"SELECT * FROM twitters WHERE twitters.email_or_phone = '{mail}' " ).fetchall()
    if table == []:
        cur.execute("INSERT INTO twitters (login,password,email_or_phone) VALUES (? , ? , ? )" , ( username ,password , mail ) )
        base.commit()
        return True
    else:
        return False


