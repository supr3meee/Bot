import datetime
import time

from bs4 import BeautifulSoup as BS

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.firefox.options import Options

from incomingcar.parsecar import get_car_clear_data


current_year = datetime.datetime.now().year


def get_data_with_selenium(arg, car):
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        # in "--headless" mode only works like this -> set_window_size
        driver.set_window_size(1920, 1080)

        driver.get(url=arg)
        time.sleep(3)

        # Clicking on the localization button
        local_priority = driver.find_element(By.NAME, "localPriority")
        ActionChains(driver) \
            .click(local_priority) \
            .perform()
        time.sleep(2)

        print(1)

        # brand

        brand = car['Марка']

        place_brand = driver.find_element(By.XPATH, "//input[@data-marker='params[110000]/suggest-input']")
        ActionChains(driver) \
            .click(place_brand) \
            .send_keys(brand) \
            .perform()
        time.sleep(1)

        place_brand_after = driver.find_element(By.XPATH, "//li[@data-marker='params[110000]/suggest-dropdown(0)']")
        ActionChains(driver) \
            .click(place_brand_after) \
            .perform()
        time.sleep(1)

        print(2)

        # model

        model = car['Модель']

        place_model = driver.find_element(By.XPATH, "//input[@data-marker='params[110001]/suggest-input']")
        ActionChains(driver) \
            .click(place_model) \
            .send_keys(model) \
            .perform()
        time.sleep(1)

        place_model_after = driver.find_element(By.XPATH, "//li[@data-marker='params[110001]/suggest-dropdown(0)']")
        ActionChains(driver) \
            .click(place_model_after) \
            .perform()
        time.sleep(1)

        print(3)

        driver.execute_script('window.scrollTo(0, 600)')    # Перемещаемся по странице
        time.sleep(2)

        # price

        # start_price = int(car['Цена'])
        # price_from = str(int(start_price - ((start_price / 100) * 25)))
        # price_to = str(int(start_price + ((start_price / 100) * 25)))
        #
        # place_price_from = driver.find_element(By.XPATH, "//input[@data-marker='price/from']")
        # ActionChains(driver) \
        #     .click(place_price_from) \
        #     .send_keys(price_from) \
        #     .perform()
        # time.sleep(1)
        #
        # place_price_to = driver.find_element(By.XPATH, "//input[@data-marker='price/to']")
        # ActionChains(driver) \
        #     .click(place_price_to) \
        #     .send_keys(price_to) \
        #     .perform()
        # time.sleep(1)

        print(4)

        # production year

        start_year = car['Год выпуска']

        if not car['Поколение']:
            year_from = int(start_year) - 2
            year_to = int(start_year) + 2
            if year_to > current_year:
                year_to = current_year
        else:

            min_year = int(car['Поколение'][0])

            if car['Поколение'][1] != 'н. в.':
                max_year = int(car['Поколение'][1])
            else:
                max_year = current_year

            year_from = int(start_year) - 2
            if year_from < min_year:
                year_from = str(min_year)

            year_to = int(start_year) + 2

            if year_to > max_year:
                year_to = str(max_year)
            else:
                str(year_to)

        place_year_from = driver.find_element(By.XPATH, "//input[@data-marker='params[188]/from/input']")
        ActionChains(driver) \
            .click(place_year_from) \
            .send_keys(year_from) \
            .perform()
        time.sleep(1)

        place_year_from_after = driver.find_element(By.XPATH, "//li[@data-marker='suggest(0)']")
        ActionChains(driver) \
            .click(place_year_from_after) \
            .perform()
        time.sleep(1)

        place_year_to = driver.find_element(By.XPATH, "//input[@data-marker='params[188]/to/input']")
        ActionChains(driver) \
            .click(place_year_to) \
            .send_keys(year_to) \
            .perform()
        time.sleep(1)

        place_year_to_after = driver.find_element(By.XPATH, "//li[@data-marker='suggest(0)']")
        ActionChains(driver) \
            .click(place_year_to_after) \
            .perform()
        time.sleep(1)

        print(5)

        # transmission

        # (Автомат общий id="331255-331257-331256") Механика(id="331254331254")
        # (Автомат id="331255") (Вариатор id="331257") (Робот id="331256")

        transmission_list = ['Автомат', 'Вариатор', 'Робот']

        transmission = car['Коробка передач']
        if transmission in transmission_list:
            transmission = "331255-331257-331256"
        else:
            transmission = "331254331254"

        place_transmission = driver.find_element(By.XPATH, "//input[@placeholder='Коробка передач']")
        ActionChains(driver) \
            .click(place_transmission) \
            .perform()
        time.sleep(1)

        place_transmission_after = driver.find_element(By.XPATH, f"//input[@id='{transmission}']")
        ActionChains(driver) \
            .click(place_transmission_after) \
            .perform()
        time.sleep(1)

        # Body type is not touched yet

        # scrolling

        driver.execute_script('window.scrollTo(0, 1400)')    # Перемещаемся по странице
        time.sleep(2)

        print(6)

        # engine type

        engine_type_dict = {
            'бензин': '331247',
            'дизель': '331248',
            'газ': '408671',
            'электро': '331250',
            'гибрид': '331249'
        }

        engine_type = engine_type_dict[car['Тип двигателя'].lower()]

        open_place_engine_type = driver.find_element(By.XPATH, "//button[@data-marker='multiselect-expand-button']")
        ActionChains(driver) \
            .click(open_place_engine_type) \
            .perform()
        time.sleep(1)

        place_engine_type = driver.find_element(By.XPATH,
                                                f"//input[@data-marker='params[110006]({engine_type})/input']")
        ActionChains(driver) \
            .click(place_engine_type) \
            .perform()
        time.sleep(1)

        print(7)

        # mileage

        start_mileage = round((int(car['Пробег'])) / 10000) * 10000

        if start_mileage > 100000:
            mileage_from = round((start_mileage - start_mileage / 100 * 33) / 10000) * 10000
            mileage_to = round((start_mileage + start_mileage / 100 * 33) / 10000) * 10000
        else:
            mileage = {
                10000: ['0', '20000'],
                20000: ['5000', '40000'],
                30000: ['10000', '50000'],
                40000: ['20000', '60000'],
                50000: ['25000', '75000'],
                60000: ['30000', '85000'],
                70000: ['40000', '95000'],
                80000: ['50000', '100000'],
                90000: ['60000', '120000'],
                100000: ['70000', '130000']
            }
            mileage_from = mileage[start_mileage][0]
            mileage_to = mileage[start_mileage][1]

        place_mileage_to = driver.find_element(By.XPATH, "//input[@data-marker='params[1375]/to/input']")
        ActionChains(driver) \
            .click(place_mileage_to) \
            .send_keys(mileage_to) \
            .perform()
        time.sleep(1)

        # calculate the index to select the desired value
        index_place_mileage_to_after = \
            str(len(driver.find_elements(By.XPATH, "//li[@class='suggest-suggest-uk_Ib text-text-LurtD "
                                                   "text-size-s-BxGpL']")) - 1)

        place_mileage_to_after = driver.find_element(By.XPATH,
                                                     f"//li[@data-marker='suggest({index_place_mileage_to_after})']")
        ActionChains(driver) \
            .click(place_mileage_to_after) \
            .perform()
        time.sleep(1)

        place_mileage_from = driver.find_element(By.XPATH, "//input[@data-marker='params[1375]/from/input']")
        ActionChains(driver) \
            .click(place_mileage_from) \
            .send_keys(mileage_from) \
            .perform()
        time.sleep(1)

        place_mileage_from_after = driver.find_element(By.XPATH, "//li[@data-marker='suggest(0)']")
        ActionChains(driver) \
            .click(place_mileage_from_after) \
            .perform()
        time.sleep(1)

        print(8)

        # engine value

        engine_value = float(car['Объём двигателя'])

        if engine_value == 2.0:
            index_engine_value = '10'
        elif engine_value == 3.0:
            index_engine_value = '5'
        elif engine_value == 4.0:
            index_engine_value = '1'
        elif engine_value == 5.0:
            index_engine_value = '1'
        elif engine_value == 6.0:
            index_engine_value = '1'
        else:
            index_engine_value = '0'

        place_engine_value_to = driver.find_element(By.XPATH, "//input[@data-marker='params[1374]/to/input']")
        ActionChains(driver) \
            .click(place_engine_value_to) \
            .send_keys(engine_value) \
            .key_down(Keys.UP) \
            .perform()
        time.sleep(1)

        place_engine_value_to_after = driver.find_element(By.XPATH,
                                                          f"//li[@data-marker='suggest({index_engine_value})']")
        ActionChains(driver) \
            .click(place_engine_value_to_after) \
            .perform()
        time.sleep(1)

        place_engine_value_from = driver.find_element(By.XPATH, "//input[@data-marker='params[1374]/from/input']")
        ActionChains(driver) \
            .click(place_engine_value_from) \
            .send_keys(engine_value) \
            .perform()
        time.sleep(1)

        if engine_value == 2.0:
            index_engine_value = '1'
        elif engine_value == 3.0:
            index_engine_value = '2'
        elif engine_value == 4.0:
            index_engine_value = '3'
        elif engine_value == 5.0:
            index_engine_value = '4'
        elif engine_value == 6.0:
            index_engine_value = '3'
        else:
            index_engine_value = '0'

        place_engine_value_to_after = driver.find_element(By.XPATH,
                                                          f"//li[@data-marker='suggest({index_engine_value})']")
        ActionChains(driver) \
            .click(place_engine_value_to_after) \
            .perform()
        time.sleep(1)

        print(9)

        # drive

        drive_dict = {
            'задний': '331252',
            'передний': '331251',
            'полный': '331253'
        }

        drive = drive_dict[car['Привод'].lower()]

        place_drive = driver.find_element(By.XPATH, f"//input[@data-marker='params[110007]({drive})/input']")
        ActionChains(driver) \
            .click(place_drive) \
            .perform()
        time.sleep(1)

        print(10)

        # wheel

        # По умолчанию стоит НЕВАЖНО

        wheel_dict = {
            'Левый': '8854',
            'Правый': '8855',
        }

        wheel = wheel_dict[car['Руль']]

        place_wheel = driver.find_element(By.XPATH, f"//input[@data-marker='params[696]({wheel}-radio)/input']")
        ActionChains(driver) \
            .click(place_wheel) \
            .perform()
        time.sleep(1)

        print(11)

        # Registration of a car in the traffic police

        # По умолчанию стоит НЕВАЖНО
        # Есть 478239
        # Нет 478240

        register = '478239'

        place_wheel = driver.find_element(By.XPATH, f"//input[@data-marker='params[110907]({register}-radio)/input']")
        ActionChains(driver) \
            .click(place_wheel) \
            .perform()
        time.sleep(1)

        print(12)

        # condition

        # По умолчанию стоит НЕВАЖНО
        # Кроме битых 8856
        # Битые 8857

        condition = '8856'

        place_wheel = driver.find_element(By.XPATH, f"//input[@data-marker='params[697]({condition})/input']")
        ActionChains(driver) \
            .click(place_wheel) \
            .perform()
        time.sleep(1)

        print(13)

        # Clicking on the search button

        button_search = driver.find_element(By.CLASS_NAME, 'form-part-button-qO9Yf')
        button_search.click()
        time.sleep(2)

        cars_src = driver.page_source

    except Exception as ex:
        print(ex)
        print('Похоже по вашему запросу нет автомобилей, или что-то пошло не так')
    finally:
        driver.close()
        driver.quit()
    return cars_src


def get_data_with_bs4(src):
    cars_list = []

    soup = BS(src, 'lxml')

    cars_area = soup.find('div', {'data-marker': 'catalog-serp'})
    cars = cars_area.find_all('div', class_='iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH '
                                            'iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih '
                                            'items-listItem-Gd1jN js-catalog-item-enum')
    for car in cars:
        car_name = car.find('h3', class_='title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR '
                                         'title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL '
                                         'text-bold-SinUO').text

        car_price = car.find('span', class_='price-text-_YGDY text-text-LurtD text-size-s-BxGpL').text

        car_params = car.find('div', class_='iva-item-text-Ge6dR text-text-LurtD text-size-s-BxGpL').text

        car_geo = car.find('div', class_='geo-root-zPwRk iva-item-geo-_Owyg').text
        car_link = 'https://www.avito.ru' + car.find('a', class_='iva-item-sliderLink-uLz1v').get('href')
        cars_list.append(f'{car_name},\n{car_price},\n{car_params},\n{car_geo}\n{car_link}\n{"_" * 30}')
        print(f'{car_name},\n{car_price},\n{car_params},\n{car_geo}\n{car_link}\n{"_" * 30}')
    return cars_list


def get_car_list(arg):
    url1 = 'https://www.avito.ru/krasnodar/avtomobili?radius=300'
    car_clear_params = get_car_clear_data(arg)
    cars_src = get_data_with_selenium(url1, car_clear_params)
    cars_list = get_data_with_bs4(cars_src)
    if 'cars.av.by' in arg:
        by_car_price = car_clear_params['Цена']
        return cars_list, by_car_price
    return cars_list
