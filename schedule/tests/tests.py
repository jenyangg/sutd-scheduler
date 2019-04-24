from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from django.test import TestCase
import threading
import time
import random
import logging
import datetime

LEGAL_PASSWORD = 'SomeStrongPW09!'


def generate_user():
    ran_num = random.randint(1001, 5000)
    ran_num_str = str(ran_num)
    ran_name = "100" + ran_num_str
    email = ran_name + '@mymail.sutd.edu.sg'
    return ran_name, email


def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


chrome_options = Options()
chrome_options.add_argument("headless")
chrome_options.add_argument("allow-insecure-localhost")
driver = webdriver.Chrome(r"C:\Users\Tea\Desktop\chromedriver_win32 (1)\chromedriver.exe", options=chrome_options)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
logger = setup_logger('info_level_logger', 'formsINFO.log')


def register():
    ran_name, email = generate_user()
    driver.find_element_by_xpath("//a[text()='Register']").click()
    username = driver.find_element_by_xpath('//input[@name="username"]')
    username.send_keys(ran_name)

    driver.find_element_by_xpath('//input[@name="email"]').send_keys(email)

    pw1 = driver.find_element_by_xpath('//input[@name="password1"]')
    pw1.send_keys(LEGAL_PASSWORD)
    pw2 = driver.find_element_by_xpath('//input[@name="password2"]')
    pw2.send_keys(LEGAL_PASSWORD)
    pw2.send_keys(Keys.RETURN)

    success_msg = driver.find_element_by_class_name('.alert.alert-success')
    assert f"Account created for {username}" in success_msg


def basic():
    register()
    driver.find_element_by_xpath('//a[text()="Login"]').click()
    driver.find_element_by_xpath('//input[@name="username"]').send_keys()
    driver.find_element_by_xpath('//input[@name = "password"]').send_keys(LEGAL_PASSWORD)
    driver.find_element_by_xpath('//button[text()="Login"]').click()


def worker(methodToRun=basic):
    start = time.time()
    now = datetime.datetime.now()
    s = now.strftime("%H:%M:%S")
    logger.info(f"Thread {threading.currentThread().getName()} started: {s}")

    methodToRun()

    end = time.time()
    total = end - start
    logger.info(f"Thread {threading.currentThread().getName()} took: {total:3f}s\n")


def run(runs=10, methodToRun=basic):
    threads = []
    for i in range(runs):
        thread = threading.Thread(target=worker, args=(methodToRun,))
        threads.append(thread)
        thread.start()


run(runs=1, methodToRun=basic)
