import csv
import toml
from datetime import datetime
from itertools import chain
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


def setup():
    option = Options()
    option.headless = False
    driver = webdriver.Chrome(options=option)
    config = toml.load('config.toml')
    return driver, config


def openBrowser(driver, config):
    url = config['login']['url']
    driver.get(url)
    driver.maximize_window()


def go_to_credencials_modal(driver, config):
    login_button_xpath = config['login']['landing_page']['login_button']['xpath']
    login_button = driver.find_element_by_xpath(
        login_button_xpath)
    login_button.click()


def set_credencials(driver, config):
    base_config = config['login']['landing_page']['modal']

    username_value = base_config['username']['value']
    password_value = base_config['password']['value']

    username_xpath = base_config['username']['xpath']
    password_xpath = base_config['password']['xpath']
    submit_button_xpath = base_config['submit_button']['xpath']

    username_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, username_xpath))
    )
    password_field = driver.find_element_by_xpath(password_xpath)
    submit_button = driver.find_element_by_xpath(submit_button_xpath)

    username_field.send_keys(username_value)
    password_field.send_keys(password_value)
    submit_button.click()


def access_unavailable(driver, config):
    base_config = config['login']['landing_page']['modal']
    end_session_xpath = base_config['end_session']['xpath']
    end_session = WebDriverWait(driver, 10). until(
        EC.element_to_be_clickable((By.XPATH, end_session_xpath))
    )
    end_session.click()


def login(driver, config):
    try:
        go_to_credencials_modal(driver, config)
        set_credencials(driver, config)
    except:
        print('access unavailable')
    else:
        access_unavailable(driver, config)


def choose_my_products_issqn(driver, config):
    base_config = config['main']['header']['my_products']
    my_products_xpath = base_config['xpath']
    issqn_option_xpath = base_config['issqn_option']['xpath']
    main_header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'main-header'))
    )
    my_products = driver.find_element_by_xpath(my_products_xpath)
    my_products.click()
    issqn_option = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, issqn_option_xpath))
    )
    issqn_option.click()
    sleep(5)


def getCities():
    with open('cidades.csv', encoding='utf-8', newline='') as cities:
        reader = csv.reader(cities)
        next(reader, None)
        params = list(reader)
        return params


def set_state(driver, config, state):
    sleep(2)
    select_state_xpath = config['issqn']['select_state']['xpath']
    select_state = driver.find_element_by_xpath(select_state_xpath)
    uf = Select(select_state)
    uf.select_by_value(state)


def set_city(driver, config, city):
    sleep(4)
    city_select_xpath = f'//*[@id="formCombosISS:OLRMUNICIPIOISS"]/option[text() = "{city}"]'
    city_select = driver.find_element_by_xpath(city_select_xpath)
    city_select.click()


def perform_search(driver, config):
    sleep(3)
    search_submit_button_xpath = config['issqn']['submit_button']['xpath']
    search_submit_button = driver.find_element_by_xpath(
        search_submit_button_xpath)
    search_submit_button.click()


def access_results(driver, config):
    sleep(1)
    law_link_xpath = config['issqn']['law_link']['xpath']
    law_link = driver.find_element_by_xpath(law_link_xpath)
    law_link.click()


def get_data(driver, config, state, city):
    base_config = config['results']
    xpath_items = base_config['items']['xpath']
    elementos_items = driver.find_elements_by_xpath(xpath_items)
    lista_valores = []
    cod_serv_atual, desc_serv_atual = ('', '')
    for index, linha in enumerate(elementos_items):
        print(f'{index + 1}/{len(elementos_items)}')
        tds = linha.find_elements_by_xpath('./td')
        texto_tds = [td.text.strip() for td in tds]
        if len(texto_tds) == 9 or len(texto_tds) == 6:
            cod_serv_atual, desc_serv_atual = texto_tds[:2]
            if len(texto_tds) == 6:
                texto_tds.insert(2, '')
                texto_tds.insert(3, '')
                texto_tds.insert(4, '')
        else:
            texto_tds.insert(0, cod_serv_atual)
            texto_tds.insert(1, desc_serv_atual)

        texto_tds.insert(0, state)
        texto_tds.insert(1, city)
        lista_valores.append(texto_tds)

    return lista_valores


def create_dataframe(table):
    df = pd.DataFrame(table)
    df.columns = ["UF", "MUNICIPIO", "ITEM MUNICIPAL", "DESCRIÇÃO DO SERVIÇO MUNICIPAL", "CODIGO DE SERVIÇO DO PRESTADOR",
                  "CODIGO DE SERVIÇO DO TOMADOR", "CODIGO DE SERVIÇO DESCRIÇÃO", "ALÍQUOTA", "BENEFÍCIO FISCAL", "SOCIEDADE", "COMENTÁRIO"]
    return df


if __name__ == "__main__":
    driver, config = setup()
    openBrowser(driver, config)
    login(driver, config)
    sleep(5)
    choose_my_products_issqn(driver, config)
    driver.switch_to.window(driver.window_handles[1])
    params = getCities()
    repository = []
    for i in params:
        state = str(i[0])
        city = str(i[1])
        set_state(driver, config, state)
        set_city(driver, config, city)
        perform_search(driver, config)
        access_results(driver, config)
        data = get_data(driver, config, state, city)
        repository.append(data)
    df = create_dataframe(list(chain(*repository)))
    file_creation_date = datetime.now().strftime('%d-%m-%Y')
    df.to_csv('importar.csv', index=False)
    driver.quit()
