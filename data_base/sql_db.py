import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('database.db')
    cur = base.cursor()
    if base:
        print("Data base connekted")


async def get_count_twitters():
    tab = cur.execute('SELECT count(*) FROM twitters').fetchall()
    return str(tab[0][0])

async def get_count_proxys():
    tab = cur.execute('SELECT count(*)  FROM proxys').fetchall()
    return str(tab[0][0])


async def set_proxy ( query ):
    cur.executemany("INSERT INTO proxys (login,password, proxy,port)VALUES (? , ? , ? , ?)" , (query))
    base.commit()

async def set_twitter ( query ):
    cur.executemany("INSERT INTO twitters (login,password,email_or_phone) VALUES (? , ? , ? )" , ( query) )
    base.commit()






