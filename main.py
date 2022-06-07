import json
import multiprocessing
import time

from lib.titter_bot import AccauntTwiter

import requests

from data_base import sql_db


from multiprocessing import Pool

def check_proxy(proxy):
    try:
        prox ={'http': proxy,
               'https': proxy
               }
        ht = requests.get(url='https://www.bing.com', proxies=prox)
        print('Прокси верны' ,ht.status_code )
        return True
    except:
        print("ошибка прокси" )
        return False


def make_a_gift( array_task , proxy_login ,proxy_password , proxy_ip , proxy_port , twitter_login , twitter_password , twitter_tag):
    proxy = f'http://{proxy_login}:{proxy_password}@{proxy_ip}:{proxy_port}'
    link , tags , mes = array_task
    try:
        if True:
            tw = AccauntTwiter()
            # tw.create_proxy_browser(proxy_username=proxy_login, proxy_password=proxy_password, proxy_ip=proxy_ip,proxy_port=proxy_port)
            tw.create_browser()
            tw.login_twiter(tw_login=twitter_login, tw_password=twitter_password)
            tw.open_tweet(link)
            tw.like()
            tw.retweet()
            time.sleep(100000)
    except Exception as e :
        print("Возникла ошибка " , e)

    print("Авторизуюсь " ,twitter_login ,twitter_password ,twitter_tag )



def retweet_post ( array_task , proxy_login ,proxy_password , proxy_ip , proxy_port , twitter_login , twitter_password , twitter_tag):
    pass

def like_post ( array_task , proxy_login ,proxy_password , proxy_ip , proxy_port , twitter_login , twitter_password , twitter_tag):
    pass

def mark_friends ( array_task , proxy_login ,proxy_password , proxy_ip , proxy_port , twitter_login , twitter_password , twitter_tag):
    pass

def subscribe ( array_task , proxy_login ,proxy_password , proxy_ip , proxy_port , twitter_login , twitter_password , twitter_tag):
    pass




def main():
    sql_db.sql_start()

    #Вечный цикл
    while True:
        #Ищем задания
        while True:
            task = sql_db.get_task()
            print("Поиск заданий")
            if task:
                array_task = json.loads(task[0][1])
                task_id = task[0][0]
                sql_db.set_task_status(task_id , 2)
                # print('Обрабатываю запрос ' , array_task['function'] )
                break
            #Спим секуду и повторяем поиск
            time.sleep(1)

        #Получаем из бд список активных связанныйх прокси + твитеров
        iter_data = sql_db.get_all_active_akkaunt_data()

        #Добавляем к списку аккаунтов задания для итерации в мультипроцессинге
        for i in range(len(iter_data)):
            iter_data[i] =   ( array_task['arguments'] ,) + iter_data[i]


        print(iter_data)

        match array_task['function'] :
            case 'gift':
                with Pool(processes=multiprocessing.cpu_count()) as pool_process:
                    dat = pool_process.starmap( make_a_gift , iter_data )
                print(dat)
            case _:
                print("Такой функции в боте нет")
                raise




    # with Pool(processes=multiprocessing.cpu_count()) as pool_process:
    #     pool_process.starmap( task_parser , [ (),() ] )
   #
    # p = Pool(2)
    # p.starmap(task_parser , [ ('kSJLd7' , '01r375' , '196.19.158.205' ,8000), ('c0BRFK' , 'QNNZN4Vp1m' , '109.248.55.221' ,5500)] )
    # p.close()

    # tw = AccauntTwiter(proxy_username="c0BRFK", proxy_password="QNNZN4Vp1m", proxy_ip="109.248.55.221",proxy_port=5500)
    # if check_proxy(tw.brower.proxy['http']):
    #     tw.login_twiter(tw_login='akkayntmager@gmail.com', tw_password='passwordtwinkoFarmer')
    #     tw.open_tweet('https://twitter.com/elonmusk/status/1530291267652898816')
    #     time.sleep(3)
    #     tw.like()
    #     tw.retweet()
    #     time.sleep(20000)
    #     tw.cls_broser()


if __name__ == '__main__':

    main()
