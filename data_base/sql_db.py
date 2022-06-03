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

async def add_task (json_task):
    cur.execute("""
    INSERT INTO tasks (
                      id,
                      json
                  )
                  VALUES (
                      ? , 
                      ? 
                  );
    """ , (None , json_task ) )
    base.commit()

def get_tasks ():
    feedback = cur.execute('SELECT * FROM tasks where tasks.status = 1 LIMIT 1').fetchall()
    return feedback

def del_task_for_id (id):
    cur.execute(f'DELETE FROM tasks WHERE id = ( {id} ) ')
    base.commit()

def disable_task (id):
    cur.execute(f"UPDATE tasks SET  status = '0' WHERE id = {id} ")
    base.commit()

def get_all_active_akkaunt_data ():
    data = cur.execute("""
    SELECT proxys.login as 'proxy_login' ,
    proxys.password as 'proxy_pasword' ,
    proxys.proxy as 'proxy_ip',
    proxys.port as 'proxy_port' ,
    twitters.email_or_phone as 'twitter_login' ,
    twitters.password as 'twitter_password' ,
    twitters.login as 'twitter_tag'
    FROM proxys
    JOIN
    proxys_twitters ON proxys_twitters.proxy = proxys.id and proxys.is_active = 1
    JOIN
    twitters ON proxys_twitters.twitter = twitters.id and twitters.status = 1
    ORDER BY proxys.id ASC;
    """).fetchall()
    return data



