from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from pynput.keyboard import Controller
from selenium.webdriver.support import expected_conditions as EC

from fake_data import get_person
from guerrilla import get_guerrilla_mail


def new_protonmail(use_capcha=False, sleeping_time=5):
    driver = webdriver.Chrome(service=Service((ChromeDriverManager().install())), options=Options())
    keyboard = Controller()

    domain = '@guerrillamail.com'
    url = 'https://account.proton.me/signup?plan=free&billing=12&ref=prctbl&minimumCycle=12&currency=EUR&product=mail&language=en'

    person = get_person()
    user = person['nickname']
    password = person['password']
    email = person['email nickname']
    full_email = person['email nickname'] + domain

    driver.get(url)
    time.sleep(sleeping_time)
    keyboard.type(user)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'repeat-password').send_keys(password)
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        "body > div.app-root > div.flex-no-min-children.flex-nowrap.flex-column.h100.sign-layout-bg.scroll-if-needed.relative > div.sign-layout-container.flex-item-fluid-auto.flex.flex-nowrap.flex-column.flex-justify-space-between > div > main > div.sign-layout-main-content > form > button")))
    elem.click()

    try:
        elem = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-testid="tab-header-Email-button"]')))
        elem.click()

        driver.find_element(By.ID, 'email').send_keys(full_email)
    except Exception as Exc:
        try:
            if use_capcha:
                print("Finding capcha...")
                elem = WebDriverWait(driver, 6).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@data-testid="tab-header-CAPTCHA-button"]')))
                elem.click()
                input("\nPress enter when you complete the capcha and setup!")
                driver.close()
                return {'login': user + "@proton.me", 'password': password}
            else:
                driver.close()
                return
        except Exception as Exc:
            driver.close()
            return

    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//button[@class="button w100 button-large button-solid-norm mt1-5"]')))
    elem.click()

    content = get_guerrilla_mail(email)
    verification_code = content.split('<br>')[1].strip('</p>')
    driver.find_element(By.ID, 'verification').send_keys(verification_code)

    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//button[@class="button w100 button-large button-solid-norm mt1-5"]')))
    elem.click()

    time.sleep(sleeping_time*3)

    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//button[@class="button w100 button-large button-solid-norm mt1-5"]')))
    elem.click()

    # maybe later???
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text() = "Maybe later"]')))
    elem.click()

    # other ...
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text() = "Confirm"]')))
    elem.click()

    time.sleep(sleeping_time)
    driver.close()

    return {'login': user+"@proton.me", 'password': password}
