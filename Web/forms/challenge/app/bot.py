from secrets import token_hex
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from uuid import UUID

BASE_URL = 'http://localhost:5000'


def visit(id, questions_to_fill):
    print(f'Visiting {id}')
    options = FirefoxOptions()
    options.add_argument('--headless')
    browser = Firefox(options=options)
    browser.set_page_load_timeout(10)
    try:
        browser.get(BASE_URL)
        browser.add_cookie({'name': 'flag', 'value': 'ictf{jp_2022_such_4_c00l_3nc0d1ng}'})
        browser.get(f'{BASE_URL}/form/fill/{id}')

        for q in questions_to_fill:
            question = browser.find_element(By.NAME, q)
            question.send_keys(token_hex(8))

        button = browser.find_element(By.NAME, 'submit')
        button.click()
        time.sleep(10)
    finally:
        browser.quit()
