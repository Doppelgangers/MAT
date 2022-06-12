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

    def __init__(self , off_image = True , bacground_mode=False):
        self.worked = True
        # Отключаем отображение изображений для оптимизации и так медленых прокси
        self.chrome_options = webdriver.ChromeOptions()

        if off_image:
            prefs = {"profile.managed_default_content_settings.images": 2}
            self.chrome_options.add_experimental_option("prefs", prefs)

        self.chrome_options.add_argument("--ignore-certificate-errors")
        self.chrome_options.add_argument("--disable-popup-blocking")
        # self.chrome_options.add_argument("--incognito")



        # Прячем вебдрайвер
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # отключаем уведомления
        self.chrome_options.add_argument('--disable-notifications')

        if bacground_mode:
            # В фоновый режим
            self.chrome_options.headless = True


        self.caps = DesiredCapabilities().CHROME
        # caps["pageLoadStrategy"] = "normal"  # complete (полная загрузка страницы)
        # caps["pageLoadStrategy"] = "eager"  #  interactive
        self.caps["pageLoadStrategy"] = "none"

    def create_browser(self ):
        # Создаём браузер
        self.brower = webdriver.Chrome(executable_path=PATCH_DRIVER, chrome_options=self.chrome_options, desired_capabilities=self.caps)


    def create_proxy_browser(self, proxy_username, proxy_password, proxy_ip, proxy_port):
        # Настраиваем прокси
        seleniumwire_options = {
            "proxy": {"http": f"http://{proxy_username}:{proxy_password}@{proxy_ip}:{proxy_port}", "verify_ssl": False}}
        # Создаём браузер
        self.brower = webdriver.Chrome(executable_path=PATCH_DRIVER, seleniumwire_options=seleniumwire_options,
                                       chrome_options=self.chrome_options, desired_capabilities=self.caps)

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

        #Проверка успешности входа
        if self.authorization_verification(refrash=False):
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
        print('проверка входа')
        if self.authorization_verification():
            return True
        else:
            print("Не удалось авторизоваться по куки")
            return False

    def open_tweet(self, url , second_enter = False):
        self.brower.get(url)
        try:
            WebDriverWait(self.brower, 20).until(
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
            WebDriverWait(self.brower, 20).until(
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
        #Удаляем старые куки
        self.delete_cookie(login=login)
        #Создаём куки
        print('куки записываюстя')
        try:
            pickle.dump(self.brower.get_cookies(), open(f'{PATCH_COOKIES}{login}__cookies', 'wb'))
            print('куки записаны')
            return True
        #Если возникла ошибка при записи повторить попытку
        except:

            if refresh:
                print("Куки не удалось  уже дважды!")
                return False
            else:
                print('Во время созранения куки возникла ,ошибка вторая попытка')
                self.create_cookie(login=login , refresh=True)

    def check_cookies(self, login):
        if os.path.isfile(PATCH_COOKIES + login + '__cookies'):
            return True
        else:
            return False

    def subscribe(self ,link):
        try:
            self.brower.get(link)
            btn = WebDriverWait(self.brower, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="placementTracking"] div[role="button"]'))
            )
            trash , status = btn.get_attribute('data-testid').split('-')
            match status:
                case 'follow':
                    btn.click()
                    time.sleep(0.05)
                    print('Подписался')
                    return True
                case 'unfollow':
                    print('Был подписан')
                    return True
                case _:
                    print('ошибка в данных')
                    return False
        except Exception as e:
            print('Возникла ошибка')
            return False


    def retweet(self):
        try:
            tweet = self.brower.find_element(By.CSS_SELECTOR, 'article')
            tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="retweet"]').click()
            confirm_retweet  = WebDriverWait(self.brower, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="retweetConfirm"]'))
            )
            confirm_retweet.click()
            print('Успешный ретвит')
            return True
        except:

            try:
                tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="unretweet"]')
                print("Ретвит уже был сделан")
                return True
            except Exception as e:
                print('Ретвит неудался' , e)
                return False

    def comment(self , text , file = ''):
        try:
            tweet = self.brower.find_element(By.CSS_SELECTOR, 'article')
            tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="reply"]').click()

            # Ждём загрузки поля сообщения
            text_area = WebDriverWait(self.brower, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-labelledby="modal-header"] div[role="textbox"]'))
            )

            #ввод текста
            text_area.send_keys(text)

            #ЕСЛИ НУЖНО ЗАГРУЗИТЬ ФАЙЛ
            if file:
                self.brower.find_element(By.CSS_SELECTOR, 'input[data-testid="fileInput"]').send_keys(file)

                try:
                    WebDriverWait(self.brower, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="attachments"]'))
                    )
                    print('Файл загружен')
                except:
                    print('Файл НЕ загружен')


            commit = WebDriverWait(self.brower, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="tweetButton"]:not(div[aria-disabled="true"])'))
            )
            commit.click()

            WebDriverWait(self.brower, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="alert"]'))
            )

            print('Успешный комент')
            return True
        except Exception as e:
            print('ошибка во время коментария ' ,e)
            return False

    def like(self):
        try:
            tweet = self.brower.find_element(By.CSS_SELECTOR, 'article')
            tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="like"]').click()
            print("Лайкнул")
            return True

        except:

            try:
                tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="unlike"]')
                print("лайк уже стоит")
                return True
            except Exception as e:
                print("Лайк не удался " , e)
                return False

    def accept_cookies(self):
        """
        Бывает появляется окно с просьбой подтвердить использование куки , что мешаст ставить работать с постами
        """
        try:
            self.brower.find_element(By.XPATH , '//*[@id="layers"]/div/div/div/div/div/div[2]/div[1]' ).click()
            return True
        except:
            return False




    def login_twiter(self, tw_login='', tw_password='', flag_used_cookies=True):
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
                return True
            else:
                print('Не удалось войти')
                return False

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

    tw = AccauntTwiter(off_image=False , bacground_mode=False)
    tw.create_browser()
    # tw.brower.get('https://bot.sannysoft.com')
    # time.sleep(10000)
    if tw.login_twiter('akkayntmager@gmail.com', 'passwordtwinkoFarmer'):
        tw.subscribe('https://twitter.com/elonmusk')
        # tw.open_tweet('https://twitter.com/elonmusk/status/1531647849599057921')
        # tw.open_tweet('https://twitter.com/binance/status/1535895825246785536')
        tw.accept_cookies()

        res  = []

        # res.append(tw.like())
        # res.append(tw.retweet())
        # res.append(tw.comment(text='i like this post)' ,file=os.getcwd()+'/tes.png'))
        # tw.brower.find_element(By.TAG_NAME , 'body').screenshot('tester.png')
        print( res )
        # tw.cls_broser()
        time.sleep(1000000)
if __name__ == '__main__':
    main()