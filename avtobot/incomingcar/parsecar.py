import re
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from bs4 import BeautifulSoup as BS

from pycbrf import ExchangeRates

rates = ExchangeRates(locale_en=True)

var = round(rates['USD'].rate)


def get_page_data(arg):
    car_src = ''
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver.get(url=arg)
        time.sleep(5)

        car_src = driver.page_source

    except Exception as ex:
        print(ex)
        print('Похоже по вашему запросу нет автомобилей, или что-то пошло не так')
    finally:
        driver.close()
        driver.quit()
    return car_src


def get_car_data(src):
    soup = BS(src, 'lxml')
    car_params_area = soup.find('ul', class_='params-paramsList-zLpAu')
    params = car_params_area.find_all('li', class_='params-paramsList__item-appQw')

    car_brand_model = soup.find_all('span', itemprop="name")
    car_brand = car_brand_model[-4].text
    car_model = car_brand_model[-3].text

    car_price = soup.find('span',
                          class_='js-item-price style-item-price-text-_w822 '
                                 'text-text-LurtD text-size-xxl-UPhmI').text.replace('\xa0', '')

    car_clear_params = {
        'Марка': car_brand,
        'Модель': car_model,
        'Цена': car_price,
        'Год выпуска': '',
        'Поколение': '',
        'Пробег': '',
        'Состояние': '',
        'Объём двигателя': '',
        'Тип двигателя': '',
        'Коробка передач': '',
        'Привод': '',
        'Тип кузова': '',
        'Руль': ''
    }

    for param in params:
        name, value = tuple(item.replace('\xa0км', '').replace('\xa0л', '').strip() for item in param.text.split(':'))
        if name in car_clear_params:
            car_clear_params[f'{name}'] = value

    car_clear_params['Поколение'] = re.findall(r'\((.+?)\)', car_clear_params['Поколение'])[0].split('—')
    print(car_clear_params)
    return car_clear_params


def get_car_data_avby(src):
    soup = BS(src, 'lxml')

    car_brand_model = soup.find_all('li', class_="breadcrumb-item")

    car_price = int(soup.find('div', class_="card__price-secondary")
                    .text.replace('≈', '').replace('$', '').replace('\u2009', '').strip()) * (var + 4)

    car_params = soup.find('div', class_="card__params").text.replace('\xa0', '').replace('\u2009', '').split(',')

    car_description = soup.find('div', class_="card__description").text.split(',')

    car_drive = re.findall(r'(задний|передний|полный)', car_description[1])[0]

    car_clear_params = {
        'Марка': car_brand_model[1].text,
        'Модель': car_brand_model[2].text,
        'Цена': car_price,
        'Год выпуска': car_params[0].replace('г.', ''),
        'Поколение': '',
        'Пробег': car_params[4].replace('км', '').strip(),
        'Состояние': '',
        'Объём двигателя': car_params[2].replace('л', '').strip(),
        'Тип двигателя': car_params[3].strip().title(),
        'Коробка передач': car_params[1].strip().title(),
        'Привод': car_drive.title(),
        'Тип кузова': car_description[0].split(' ')[0].title(),
        'Руль': 'Левый'
    }
    print(car_clear_params)
    return car_clear_params


def get_car_clear_data(arg):
    car_clear_params = {}
    car_src = get_page_data(arg)
    if 'www.avito.ru' in arg:
        car_clear_params = get_car_data(car_src)
    elif 'cars.av.by' in arg:
        car_clear_params = get_car_data_avby(car_src)
    return car_clear_params
