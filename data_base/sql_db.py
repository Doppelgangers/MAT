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

async def link_proxy_for_twitters ():
    free_twitter = cur.execute('SELECT twitters.id FROM twitters LEFT JOIN proxys_twitters ON proxys_twitters.twitter = twitters.id WHERE proxys_twitters.id IS NULL').fetchall()
    free_proxy = cur.execute('SELECT proxys.id FROM proxys LEFT JOIN proxys_twitters ON proxys_twitters.proxy = proxys.id WHERE proxys_twitters.id IS NULL').fetchall()
    command = []
    count_pars = 5
    i_may = len(free_twitter) // count_pars
    real = len(free_proxy) - i_may
    if real > 0:
        use = i_may
    else:
        use = len(free_proxy)

    for pr in range(use):
        for tw in range(count_pars):
            print(free_proxy[pr][0], free_twitter[pr * count_pars + tw][0])
            command.append( [free_proxy[pr][0], free_twitter[pr * count_pars + tw][0]] )


    # offset = free_twitter[do:]
    # print( command )

    cur.executemany("INSERT INTO proxys_twitters (proxy, twitter) VALUES ( ? , ? )" , (command))
    base.commit()

    return len(command)






