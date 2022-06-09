import os.path
import pickle
import time

from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from configs import *

class AccauntTwiter:

    def __init__(self):
        pass

    def create_browser(self):
        self.worked = True
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        # В фоновый режим
        # chrome_options.headless = True

        caps = DesiredCapabilities().CHROME
        # caps["pageLoadStrategy"] = "normal"  # complete (полная загрузка страницы)
        # caps["pageLoadStrategy"] = "eager"  #  interactive
        caps["pageLoadStrategy"] = "none"

        # Создаём браузер
        self.brower = webdriver.Chrome(executable_path=PATCH_DRIVER, chrome_options=chrome_options, desired_capabilities=caps)


    def create_proxy_browser(self, proxy_username, proxy_password, proxy_ip, proxy_port):
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

    def enter_for_password(self, login, password , second_enter = False , refrash = True):
        if refrash:
            self.brower.get('https://twitter.com/i/flow/login')
        try:
            log = WebDriverWait(self.brower, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
            )
            print('TARGER поле логина')
        except:
            if second_enter:
                print("Неудалось найти поле логина дважды ")
                return False
            else:
                print("Вторая попытка входа по поролю")
                self.enter_for_password(login=login, password=password, second_enter=True)
        # Ввод логина
        log.clear()
        login_array = list(login)
        for i in login_array:
            log.send_keys(i)
            time.sleep(0.05)
        time.sleep(0.4)
        log.send_keys(Keys.ENTER)
        time.sleep(0.4)

        try:
            inputPas = WebDriverWait(self.brower, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="current-password"]'))
            )
            print('TARGET поле ввода пороля')
        except:
            print('Неудалось найти поле ввода пороля')
            return False
        # Ввод пороля
        # inputPas = self.brower.find_element(By.CSS_SELECTOR, 'input[autocomplete="current-password"]')
        inputPas.clear()
        password_array = list(password)
        for i in password_array:
            inputPas.send_keys(i)
            time.sleep(0.05)
        time.sleep(0.4)
        inputPas.send_keys(Keys.ENTER)
        time.sleep(0.4)

        #Проверка успешности входа
        if self.authorization_verification():
            return True
        else:

            if second_enter:
                return False

            try:
                WebDriverWait(self.brower, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
                )
                print("Вход неудолся ")
                self.enter_for_password(login=login, password=password, second_enter=True , refrash=False)
            except:
                return False



    def enter_for_cookies(self, login , second_enter = False):

        #Входим на сайт авторизации
        self.brower.get('https://twitter.com/i/flow/login')

        #Ждём появления поля ввода пороля (20 секунд ищем любой инпут)
        try:
            WebDriverWait(self.brower, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'input'))
            )
            print('Страница загрузилась')
        except:
            #Даём второй шанс войти на страницу , еcли за 2 попытки не смогли авторизоваться тогда выводим False
            if second_enter:
                print('Страница входа не загрузилась за 2 попытки')
                return False
            else:
                print('Попытка перезагрузить страницу')
                self.enter_for_cookies(login=login , second_enter=True)

        #Загружаем куки из файла , если загрузка не удалась выводим Falese
        print('Начало загрузки куки на сайт')
        try:
            for coocie in pickle.load(open(f'{PATCH_COOKIES}{login}__cookies', 'rb')):
                self.brower.add_cookie(coocie)
            print('Загруженно')
        except Exception as e :
            print('Во время загрузки куки возникала ошибка' , e)
            return False

        #Проверка входа (если появилась аватарка на главной странице)

        if self.authorization_verification():
            return True
        else:
            print("Не удалось авторизоваться по куки")
            return False


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
                return False
            else:
                print('Вторая попытка открыть твит ')
                self.open_tweet(url=url , second_enter=True)
        try:
            element = WebDriverWait(self.brower, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'article'))
            )
            print('TARGER содержимое твита')
            return True
        except:
            if second_enter:
                print("Неудалось загрусть сам твит дважды")
                return False
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

    def comment(self , text = ''):
        try:
            tweet = self.brower.find_element(By.CSS_SELECTOR, 'article')
            tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="reply"]').click()
            #Ждём загрузки модального окна
            area = WebDriverWait(self.brower, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-labelledby="modal-header"]'))
            )
            #ждём загрузки поля ввода сообщения (определяем по полю со смайликом)
            load_mesage_area = WebDriverWait(self.brower, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR , 'div[aria-autocomplete="list"]'))
            )
            load_mesage_area.send_keys(text)
            # area.find_element(By.CSS_SELECTOR , 'div[data-testid="tweetTextarea_0"]')
            time.sleep(0.2)
            otvet = area.find_element(By.CSS_SELECTOR , 'div[data-testid="tweetButton"]' )
            otvet.click()
            print('Успешный комент')
        except Exception as e:
            print('ошибка во время коментария ' ,e)


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
        # Если есть куки пытаемя войти с их помощью
        if (self.check_cookies(login=tw_login) and flag_used_cookies ):

            if self.enter_for_cookies(login=tw_login):
                print("Вошёл через куки")
                return True
            else:
                print('Заблокирован вход по куки , попытка без них')
                self.login_twiter(tw_login=tw_login, tw_password=tw_password, flag_used_cookies=False)

        else:
            # Если куки в файлах нет авторизуемя и создаём куки

                # Авторизуемся по поролю
            if self.enter_for_password(login=tw_login, password=tw_password):
                    # Создаём куки
                    self.create_cookie(tw_login)
            else:
                if second_enter:
                    print('Дважды не удалось войти, аккаунт добавлен в архив')
                    return False
                else:
                    print('Попытка второго входа')
                    self.login_twiter(tw_login=tw_login, tw_password=tw_password, flag_used_cookies=False , second_enter=True)

    def authorization_verification(self, second_enter=False , refrash = True):
        if refrash:
            self.brower.get('https://twitter.com/home')
        try:
            element = WebDriverWait(self.brower, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="SideNav_AccountSwitcher_Button"]'))
            )
            print('Успешный вход')
            return True
        except:
            if second_enter:
                print('Не успешный вход , нет значка пользователя')
                return False
            else:
                print('Вторая попытка провеоки входа')
                self.authorization_verification(second_enter=True)


def main():
    tw = AccauntTwiter()
    tw.create_browser()
    if tw.login_twiter('akkayntmager@gmail.com', 'passwordtwinkoFarmer'):
        tw.open_tweet('https://twitter.com/elonmusk/status/1531647849599057921')

        tw.like()
        tw.retweet()
        tw.comment( 'very interesting)(' )
    time.sleep(10000)

if __name__ == '__main__':
    main()