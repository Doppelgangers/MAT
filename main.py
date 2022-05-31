import json
import multiprocessing
import time
import os.path
import pickle
import requests

# import logging
# logging.basicConfig(level=logging.DEBUG)

from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from configs import *
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
        print("ошбка прокси" )
        return False

class AccauntTwiter:
    def __init__(self, proxy_username, proxy_password, proxy_ip, proxy_port):
        self.worked = True
        # Отключаем отображение изображений для оптимизации и так медленых прокси
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        #В фоновый режим
        # chrome_options.headless = True

        # Настраиваем прокси
        seleniumwire_options = {
            "proxy": {"http": f"http://{proxy_username}:{proxy_password}@{proxy_ip}:{proxy_port}", "verify_ssl": False}}

        caps = DesiredCapabilities().CHROME
        # caps["pageLoadStrategy"] = "normal"  # complete (полная загрузка страницы)
        # caps["pageLoadStrategy"] = "eager"  #  interactive
        caps["pageLoadStrategy"] = "none"

        # Создаём браузер
        self.brower = webdriver.Chrome(executable_path=PATCH_DRIVER, seleniumwire_options=seleniumwire_options,
                                       chrome_options=chrome_options, desired_capabilities=caps)

    def cls_broser(self):
        # При вызове этой функции закрывается текущий браузер
        try:
            self.worked = False
            self.brower.close()
            self.brower.quit()
        except Exception as ex:
            print(ex)

    def enter_for_password(self, login, password , second_enter = False):
        self.brower.get('https://mobile.twitter.com/i/flow/login')
        try:
            element = WebDriverWait(self.brower, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
            )
            print('TARGER поле логина')
        except:
            if second_enter:
                print("Неудалось найти поле логина дважды ")
                raise
            else:
                print("Вторая попытка входа по поролю")
                self.enter_for_password(login=login, password=password, second_enter=True)
        # Ввод логина
        log = self.brower.find_element(By.CSS_SELECTOR, 'input[autocomplete="username"]')
        log.clear()
        log.send_keys(login)
        log.send_keys(Keys.ENTER)

        try:
            element = WebDriverWait(self.brower, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="current-password"]'))
            )
            print('TARGET поле ввода пороля')
        except:
            print('Неудалось найти поле ввода пороля')
            raise
        # Ввод пороля
        inputPas = self.brower.find_element(By.CSS_SELECTOR, 'input[autocomplete="current-password"]')
        inputPas.clear()
        inputPas.send_keys(password)
        inputPas.send_keys(Keys.ENTER)

        #Проверка успешности входа
        self.authorization_verification()

    def enter_for_cookies(self, login , second_enter = False):
        self.brower.get('https://mobile.twitter.com/')

        #Поскольку я зотключил проверку загрузки страницы вручную ждём минимальной загрузки страницы
        try:
            element = WebDriverWait(self.brower, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'input'))
            )
            print('Страница загрузилась')
        except:
            if second_enter:
                print('Страница не грузится снова')
                raise
            else:
                print('Попытка перезагрузить страницу')
                self.enter_for_cookies(login=login , second_enter=True)

        print('Начало загрузки куки на сайт')
        try:
            for coocie in pickle.load(open(f'{PATCH_COOKIES}{login}__cookies', 'rb')):
                self.brower.add_cookie(coocie)
            print('Загруженно')

            #Проверка входа
            self.authorization_verification()

        except:
            print("Не удалось авторизоваться по куки")
            raise

    def open_tweet(self, url , second_enter = False):
        self.brower.get(url)
        try:
            element = WebDriverWait(self.brower, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h2[role = "heading"]'))
            )
            print('TARGER твит')
        except:
            if second_enter:
                print("Неудалось найти твит дважды")
                raise
            else:
                print('Вторая попытка открыть твит ')
                self.open_tweet(url=url , second_enter=True)
        try:
            element = WebDriverWait(self.brower, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'article'))
            )
            print('TARGER содержимое твита')
        except:
            if second_enter:
                print("Неудалось загрусть сам твит дважды")
                raise
            else:
                print('Вторая попытка загрусть твит ')
                self.open_tweet(url=url, second_enter=True)

    def delete_cookie(self, login):
        if self.check_cookies(login=login):
            os.remove(PATCH_COOKIES + login + '__cookies')
            print('Старые куки удалены')

    def create_cookie(self, login , refresh = False):
        #Удаляем старык куки
        self.delete_cookie(login=login)
        #Создаём куки
        print('куки записываюстя')
        try:
            pickle.dump(self.brower.get_cookies(), open(f'{PATCH_COOKIES}{login}__cookies', 'wb'))
            print('куки записаны')
        #Если возникла ошибка при записи повторить попытку
        except:
            if refresh:
                print("Куки не ужалось записать уже дважды!")
            else:
                print('Во время созранения куки возникла ,ошибка вторая попытка')
                self.create_cookie(login=login , refresh=True)

    def check_cookies(self, login):
        if os.path.isfile(PATCH_COOKIES + login + '__cookies'):
            return True
        else:
            return False

    def retweet(self):
        try:
            tweet = self.brower.find_element(By.CSS_SELECTOR, 'article')
            tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="retweet"]').click()
            time.sleep(0.4)
            self.brower.find_element(By.CSS_SELECTOR, 'div[data-testid="retweetConfirm"]').click()
            print('Успешный ретвит')
        except:
            print('Ретвит неудался или уже был сделан')

    def unretweet(self):
        try:
            tweet = self.brower.find_element(By.TAG_NAME, 'article')
            tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="unretweet"]').click()
            time.sleep(0.4)
            self.brower.find_element(By.CSS_SELECTOR, 'div[data-testid="unretweetConfirm"]').click()
            print('Ретивит отменён')
        except:
            print('Ретвит неудалось отменить')

    def like(self):
        try:
            tweet = self.brower.find_element(By.CSS_SELECTOR, 'article')
            tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="like"]').click()
            print("Лайкнул")
        except:
            print("Лайк не удался")

    def unlike(self):
        try:
            tweet = self.brower.find_element(By.CSS_SELECTOR, 'article')
            tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="unlike"]').click()
            print("Убрал лайк")
        except:
            print("Лайк не удалось снять или уже был снят")

    def login_twiter(self, tw_login='', tw_password='', flag_used_cookies=True, second_enter=False):
        if (self.check_cookies(login=tw_login) and flag_used_cookies ):
            # Если есть куки пытаемя войти с их помощью
            try:
                self.enter_for_cookies(login=tw_login)
            except:
                print('Заблокирован вход по куки , попытка без них')
                self.login_twiter(tw_login=tw_login, tw_password=tw_password, flag_used_cookies=False)

        else:
            # Если куки в файлах нет авторизуемя и создаём куки
            try:
                # Авторизуемся по поролю
                self.enter_for_password(login=tw_login, password=tw_password)
                # Создаём куки
                self.create_cookie(tw_login)
            except:
                if second_enter:
                    print('Дважды не удалось войти, аккаунт добавлен в архив')
                    raise
                else:
                    print('Попытка второго входа')
                    self.login_twiter(tw_login=tw_login, tw_password=tw_password, flag_used_cookies=False,second_enter=True)

    def authorization_verification(self , second_enter = False):
        self.brower.get('https://twitter.com/home')
        try:
            element = WebDriverWait(self.brower, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="SideNav_AccountSwitcher_Button"]'))
            )
            print('Успешный вход')
        except:
            if second_enter:
                print('Не успешный вход , нет значка пользователя')
                raise
            else:
                print('Вторая попытка провеоки входа')
                self.authorization_verification(second_enter=True)





def task_parser(proxy_username="c0BRFK", proxy_password="QNNZN4Vp1m", proxy_ip="109.248.55.221",proxy_port=5500):
    tweeter = AccauntTwiter( proxy_username=proxy_username, proxy_password=proxy_password, proxy_ip=proxy_ip,proxy_port=proxy_port  )
    tweeter.brower.get('http://2ip.ru')



def main():

    # with Pool(processes=multiprocessing.cpu_count()) as pool_process:
    #     pool_process.starmap( task_parser , [ (),() ] )
    # iterable_list  = ['109.248.55.221:5500:c0BRFK:QNNZN4Vp1m:akkayntmager@gmail.com:passwordtwinkoFarmer:ot#https://twitter.com/elonmusk/status/1519377424437243904:#like#retweet']
    #
    # p = Pool(2)
    # p.starmap(task_parser , [ ('kSJLd7' , '01r375' , '196.19.158.205' ,8000), ('c0BRFK' , 'QNNZN4Vp1m' , '109.248.55.221' ,5500)] )
    # p.close()

    tw = AccauntTwiter(proxy_username="c0BRFK", proxy_password="QNNZN4Vp1m", proxy_ip="109.248.55.221",proxy_port=5500)
    if check_proxy(tw.brower.proxy['http']):
        tw.login_twiter(tw_login='akkayntmager@gmail.com', tw_password='passwordtwinkoFarmer')
        tw.open_tweet('https://twitter.com/elonmusk/status/1530291267652898816')
        time.sleep(3)
        tw.like()
        tw.retweet()
        time.sleep(20000)
        tw.cls_broser()


if __name__ == '__main__':
    main()
