from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from generator_interface import MyGenerator
import time
from pynput.keyboard import Controller, Key
from fake_data import get_person
import csv


class JetAcc:
    def __init__(self):
        self.person = get_person()
        self.keyboard = Controller()
        self.gen = MyGenerator()
        self.driver = None
        self.proton_login = None
        self.proton_password = None

    def start_register_jetbrains(self):
        self.driver.get('https://account.jetbrains.com/login')
        time.sleep(3)
        self.driver.find_element(By.NAME, "email").send_keys(self.proton_login)
        elem = WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@class="btn btn-primary btn-lg sign-up-button eml-submit-btn"]')))
        elem.click()

    def protonmail_login(self):
        """
        Підтверджувати обліковий запис
        """

        url = 'https://account.proton.me/login'
        self.driver.get(url)
        elem = WebDriverWait(self.driver, 6).until(
                    EC.presence_of_element_located((By.ID, 'username')))
        elem.send_keys(self.proton_login)

        elem = WebDriverWait(self.driver, 6).until(
                    EC.presence_of_element_located((By.ID, 'password')))
        elem.send_keys(self.proton_password)

        elem = WebDriverWait(self.driver, 6).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@class="button w100 button-large button-solid-norm mt1-5"]')))
        elem.click()

        time.sleep(8)

        try:
            for i in range(3):
                elem = WebDriverWait(self.driver, 6).until(
                            EC.presence_of_element_located((By.XPATH, '//button[@class="button w100 button-large button-solid-norm"]')))
                elem.click()
                time.sleep(1)
        except:
            pass

        self.keyboard.press(Key.tab)
        self.keyboard.press(Key.enter)
        # in message here
        time.sleep(1)
        for i in range(16):
            self.keyboard.press(Key.tab)
            time.sleep(0.5)
        self.keyboard.tap(Key.enter)
        self.keyboard.press(Key.enter)

    def continue_registration(self):
        elem = self.driver.find_element(By.XPATH, '//span[@class="text-bold text-break"]')
        self.driver.get(elem.text)
        # in jetbrains
        time.sleep(2)

        self.driver.find_element(By.NAME, "firstName").send_keys(self.person['first name'])
        self.driver.find_element(By.NAME, "lastName").send_keys(self.person['last name'])
        self.driver.find_element(By.NAME, "userName").send_keys(self.person['nickname'])
        self.driver.find_element(By.NAME, "password").send_keys(self.person['password'])
        self.driver.find_element(By.NAME, "pass2").send_keys(self.person['password'])
        self.driver.find_element(By.NAME, "privacy").click()
        time.sleep(3)
        elem = WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@class="pwd-submit-btn btn btn-primary btn-lg"]')))
        elem.click()
    time.sleep(3)

    def write_jetbrains_data(self):
        with open(self.gen.filename, mode='a', encoding='utf-8', newline='') as f:
            fieldnames = ['login', 'email', 'password']
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writerow({'login': self.person['nickname'], 'email': self.proton_login,
                             'password': self.person['password']})

    def generate_account(self):
        self.gen.run_generator()
        self.gen.write_data()
        self.proton_login, self.proton_password = self.gen.data.values()
        self.driver = webdriver.Chrome(service=Service((ChromeDriverManager().install())), options=Options())
        self.driver.maximize_window()

        time.sleep(5)
        self.start_register_jetbrains()
        time.sleep(15)
        self.protonmail_login()
        self.continue_registration()
        self.write_jetbrains_data()


if __name__ == '__main__':
    jet_acc = JetAcc()
    jet_acc.generate_account()
