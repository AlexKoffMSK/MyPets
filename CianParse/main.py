from bs4 import BeautifulSoup
from time import sleep
# import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

#working_directory_str = getcwd()

#usag = UserAgent()
#driver = webdriver.Chrome()

#блок кода где в драйвер загружается конкретная страница и перегоняется в BS
def FeedBSWithPageLink(page_link, driver):
    print(FeedBSWithPageLink.__name__, 'run')
    try:
        driver.get(page_link)
    except:
        print('Couldnt driver.get(page_link)')
    try:
        page_soup = BeautifulSoup(driver.page_source, 'lxml')
        #driver.close()
        return page_soup
    except:
        print('Couldnt parse')
    print(FeedBSWithPageLink.__name__, 'finish')

#блок кода чтобы нажать кнопку Принять куки
def AcceptCookies(driver):
    print(AcceptCookies.__name__, 'run')
    try:
        #cookie_button = '/html/body/header/div[1]/div[2]/button/span'
        cookie_button = '/html/body/header/div[1]/div[2]/button'
        fld = driver.find_element(By.XPATH, cookie_button)
        fld.click()
    except:
        print('Couldnt find element by XPATH or click on it')
    print(AcceptCookies.__name__, 'finish')

#блок кода, чтобы закрыть боковое окно с опросом
def CloseQuizBlock(driver):
    print(CloseQuizBlock.__name__, 'run')
    quiz_button_first_part_of_path = '/html/body/div['
    quiz_button_last_part_of_path = ']/div[2]/form/div/div[1]/button'

    for i in range(0,6):
        try:
            #print("Trying to guess the right number from 0 to 5")
            quiz_button = quiz_button_first_part_of_path+str(i)+quiz_button_last_part_of_path
            fld = driver.find_element(By.XPATH, quiz_button)
            fld.click()
        except:
            print('Couldnt close Quiz')
    print(CloseQuizBlock.__name__, 'finish')

# более простой способ найти текст в тэге используя поиск через attrs.get('***') по атрибутам тэга
def GetTitleOfAd(page_source):
    print(GetTitleOfAd.__name__, 'run')
    title_of_ad = ''
    for item in page_source.find_all('div'):
        if item.attrs.get('data-name') == 'OfferTitle' or item.attrs.get('data-name') == 'OfferTitleNew':
            title_of_ad = item.text
    print(GetTitleOfAd.__name__, 'finish')
    return title_of_ad

# более простой способ найти текст в тэге используя поиск через attrs.get('***') по атрибутам тэга
def GetGeoPosition(page_source):
    print(GetGeoPosition.__name__, 'run')
    geo_position=''
    for item in page_source.find_all('div'): #итерируемся по тэгам div, которые ВСЕ найдены методом find_all
        if item.attrs.get('data-name') == 'Geo':
            assert(len(item.find_all('span')) > 0)
            assert(item.find_all('span')[0].attrs.get('content') != None)
            geo_position=item.find_all('span')[0].attrs.get('content')
    print(GetGeoPosition.__name__, 'finish')
    return geo_position

#более простой блок кода для добычи цены квартиры
def GetPrice(page_source):
    print(GetPrice.__name__, 'run')
    #assert(len(page_source.find_all('span', itemprop='price')) == 1)
    item = page_source.find_all('span', itemprop='price')[0]
    #price = int(''.join(item.attrs.get('content')[:-2].split(' '))))
    price = int(item.attrs.get('content')[:-1].replace(' ',''))
    print(GetPrice.__name__, 'finish')
    return price

def GetPrice2(page_source):
    print(GetPrice2.__name__, 'run')
    tmp_price = page_source.find('div', class_ = re.findall('a10a3f92e9--price--PcAEt a10a3f92e9--price--residential--.[^\"]*', str(page_source))).text.split('₽')
    pattern_for_excluding_unicode_in_price = re.compile(r'\s+', re.UNICODE)
    tmp = [pattern_for_excluding_unicode_in_price.sub('', p) for p in tmp_price[0]]
    tmp_price[0]=''.join(tmp)
    price=tmp_price[0]
    print(GetPrice2.__name__, 'finish')
    return price

#более простой блок кода для добычи общей информации о квартире
def GetSpaceAndFloor(page_source):
    print(GetSpaceAndFloor.__name__, 'run')
    dict_title_and_number={}
    for item in page_source.find_all('div'):
        if item.attrs.get('data-testid') == 'object-summary-description-info':
            dict_title_and_number[item.find_all()[1].text] = item.find_all()[0].text
    print(GetSpaceAndFloor.__name__, 'finish')
    return dict_title_and_number

#более простой блок поиска текста объявления
def GetDescriptionOfAd(page_source):
    print(GetDescriptionOfAd.__name__, 'run')
    description_of_ad=''
    for item in page_source.find_all('div'):
        if item.attrs.get('data-name') == 'Description':
            description_of_ad=item.text
    print(GetDescriptionOfAd.__name__, 'finish')
    return description_of_ad

#блок кода, чтобы нажать кнопку Показать телефон и скопировать телефон
# def PressButtonOpenPhone():
#     #open_phone_number = '/html/body/div[2]/main/div[3]/div/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/button'
#     open_phone_number = '/html/body/div[2]/main/div[3]/div/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/button/span'
#     fld = driver.find_element(By.XPATH, open_phone_number)
#     fld.click()

#более простой блок кода чтобы достать телефон продавца
# def GetSellersPhone(page_source):
#     phone_seller=''
#     for item in page_source.find_all('div'):
#         if item.attrs.get('data-name') == 'OfferContactsAside':
#             for it_in in item.find_all('a'):
#                 phone_seller='-'.join(it_in.text.split(' '))
#     return phone_seller

#блок кода чтобы достать телефон по объявлению
# def GetSellersPhone2(page_source):
#     phone_seller = page_source.find('a', class_ = re.findall('a10a3f92e9--phone--.[^\"]*', str(page_source))).text.split(' ')
#     phone_seller ='-'.join(phone_seller)
#     return phone_seller

def PressButtonOpenPhoneAndGetPhone(page_source, driver):
    print(PressButtonOpenPhoneAndGetPhone.__name__, 'run')
    sleep(2)
    print('Trying to open phone number button')
    try:
        open_phone_number = '/html/body/div[2]/main/div[3]/div/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/button'
        #open_phone_number = '/html/body/div[2]/main/div[3]/div/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/button/span'
        #open_phone_number = '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[4]/button'
        fld = driver.find_element(By.XPATH, open_phone_number)
        sleep(0.5)
        fld.click()
        print('Phone number button opened')
    except:
        print('Couldnt open phone button')

    sleep(1.5)
    print('Trying to close message with working hours')
    try:
        window_close = '/html/body/div[6]/div/div/div[1]/div[1]' #всплывающее окно с графиком работы специалистов. Всплывает вечером.
        fld = driver.find_element(By.XPATH, window_close)
        fld.click()
        print('Message with working hours closed')
    except:
        print('Couldnt close window with working hours')
    #sleep(0.5)

    phone_seller = ''
    print('Trying to grab a phone number')
    try: #если открылась кнопка и я достучался до телефона - пытаюсь его забрать
        for item in page_source.find_all('div'):
            if item.attrs.get('data-name') == 'OfferContactsAside':
                for it_in in item.find_all('a'):
                    phone_seller='-'.join(it_in.text.split(' '))
        print('Phone number grabbed')
    except:
        print('Couldnt grab phone number')
        phone_seller+= 'Телефон не достали'
    print(PressButtonOpenPhoneAndGetPhone.__name__, 'finish')
    return phone_seller

#блок кода, чтобы закрыть окно с графиком работы специалистов
# def HideWorkingHoursOfManagers():
#     try:
#         window_close = '/html/body/div[6]/div/div/div[1]/div[1]'
#         fld = driver.find_element(By.XPATH, window_close)
#         fld.click()
#     except:
#         print('')
#     finally:
#         print("The 'try except' is finished")

#блок кода для сбора сета из веб-адресов страниц на ЦИАНе с продажей квартир на вторичке
#https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p=54&region=1&room1=1
#https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p=54&region=1&room2=1
#https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p=54&region=1&room3=1

first_part_of_link_before_page_number = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p='
last_part_of_link_after_page_number_for_1_bedroom = '&region=1&room1=1'
last_part_of_link_after_page_number_for_2_bedroom = '&region=1&room2=1'
last_part_of_link_after_page_number_for_3_bedroom = '&region=1&room3=1'

set_of_sale_pages_1_room = set()
def GetSetOfSalePagesUrls_1Bed(cur_final_num_page_for_test):
    print(GetSetOfSalePagesUrls_1Bed.__name__, 'run')
    for i in range(1, cur_final_num_page_for_test+1):
        driver = webdriver.Chrome()
        i_page_with_ads = first_part_of_link_before_page_number + str(i) + last_part_of_link_after_page_number_for_1_bedroom
        driver.get(i_page_with_ads)
        sleep(0.5)
        page_soup = BeautifulSoup(driver.page_source, 'lxml')

        for item in page_soup.find_all('div'):
            if item.attrs.get('data-name') == 'LinkArea':
                for in_it in item.find_all('a'):
                    if 'https://www.cian.ru/sale/flat/' in in_it.get('href'):
                        set_of_sale_pages_1_room.add(in_it.attrs.get('href'))
        driver.quit()
        #sleep(1)
    print(GetSetOfSalePagesUrls_1Bed.__name__, 'finish')

set_of_sale_pages_2_room = set()
def GetSetOfSalePagesUrls_2Bed(cur_final_num_page_for_test):
    print(GetSetOfSalePagesUrls_2Bed.__name__, 'run')
    for i in range(1, cur_final_num_page_for_test+1):
        driver = webdriver.Chrome()
        i_page_with_ads = first_part_of_link_before_page_number + str(i) + last_part_of_link_after_page_number_for_2_bedroom
        driver.get(i_page_with_ads)
        sleep(0.5)
        page_soup = BeautifulSoup(driver.page_source, 'lxml')

        for item in page_soup.find_all('div'):
            if item.attrs.get('data-name') == 'LinkArea':
                for in_it in item.find_all('a'):
                    if 'https://www.cian.ru/sale/flat/' in in_it.get('href'):
                        set_of_sale_pages_2_room.add(in_it.attrs.get('href'))
        driver.quit()
        #sleep(1)
    print(GetSetOfSalePagesUrls_2Bed.__name__, 'finish')

set_of_sale_pages_3_room = set()
def GetSetOfSalePagesUrls_3Bed(cur_final_num_page_for_test):
    print(GetSetOfSalePagesUrls_3Bed.__name__, 'run')
    for i in range(1, cur_final_num_page_for_test+1):
        driver = webdriver.Chrome()
        i_page_with_ads = first_part_of_link_before_page_number + str(i) + last_part_of_link_after_page_number_for_3_bedroom
        driver.get(i_page_with_ads)
        sleep(0.5)
        page_soup = BeautifulSoup(driver.page_source, 'lxml')

        for item in page_soup.find_all('div'):
            if item.attrs.get('data-name') == 'LinkArea':
                for in_it in item.find_all('a'):
                    if 'https://www.cian.ru/sale/flat/' in in_it.get('href'):
                        set_of_sale_pages_3_room.add(in_it.attrs.get('href'))
        driver.quit()
        #sleep(1)
    print(GetSetOfSalePagesUrls_3Bed.__name__, 'finish')

def GetDataForCurFlat(set_of_sale_pages_X_room):
    print(GetDataForCurFlat.__name__, 'run')
    tmp_set_of_sale_pages_X_room = set(list(set_of_sale_pages_X_room)[:3]) #просто для примера того, что оно работает - возьмем по 3 квартиры
    for link in tmp_set_of_sale_pages_X_room:
    #for link in set_of_sale_pages_X_room:
        list_with_flat_data = []
        sleep(1)
        print('add link to flat in list_with_flat_data')
        list_with_flat_data.append(link)
        print(list_with_flat_data)
        driver = webdriver.Chrome()
        try:
            print('trying to parse flat page')
            page_source = FeedBSWithPageLink(link, driver)
        except:
            print('fail to parse flat page')
        sleep(1)
        try:
            print('trying to click on page on Cookie button')
            AcceptCookies(driver)
        except:
            print('fail to click on page on Cookie button')
        sleep(1)
        try:
            print('trying to close quiz window')
            CloseQuizBlock(driver)
        except:
            print('fail to close quiz window')
        sleep(1)
        # PressButtonOpenPhone()
        # sleep(2)
        # HideWorkingHoursOfManagers()
        try:
            print('trying to get title')
            list_with_flat_data.append(GetTitleOfAd(page_source))
        except:
            print('fail to get title')
        sleep(0.2)
        try:
            print('trying to get GeoPosition')
            list_with_flat_data.append(GetGeoPosition(page_source))
            print(list_with_flat_data)
        except:
            print('fail to get GeoPosition')
        sleep(0.2)
        try:
            print('trying to get Price2')
            #list_with_flat_data.append(GetPrice(page_source))
            list_with_flat_data.append(GetPrice2(page_source))
            print(list_with_flat_data)
        except:
            print('fail to get Price2')
        sleep(0.2)
        try:
            print('trying to get Description')
            list_with_flat_data.append(GetDescriptionOfAd(page_source))
            print(list_with_flat_data)
        except:
            print('fail to get Description')
        sleep(0.2)
        try:
            print('trying to run function for Press Button Open Phone And Get Phone')
            list_with_flat_data.append(PressButtonOpenPhoneAndGetPhone(page_source, driver))
            print(list_with_flat_data)
        except:
            print('fail to run function for Press Button Open Phone And Get Phone')
        driver.close()
        print('Добавляем информацию по квартире в список списков с информацией по квартирам')
        list_with_all_flats_data.append(list_with_flat_data)
    print('Агрегированный список с информацией по квартирам')
    print(list_with_all_flats_data)

    print(GetDataForCurFlat.__name__, 'finish')

def DataToCSVFile(list_with_all_flats_data):
    #через библиотеку pandas перегоняем в файл
    df = pd.DataFrame(list_with_all_flats_data)
    df.columns = ['url_link', 'title', 'geo_position', 'price_str', 'description', 'seller_phone'] #именуем заголовки столбцов
    df.to_csv('data.csv', index=False, sep=';', encoding='utf-8-sig')

list_with_all_flats_data=[]
cur_final_page_for_test = 2 #для примера спарсим по 2 страницы с каждого поиска, чтобы проверить пагинацию

def RunParseCian():
    GetSetOfSalePagesUrls_1Bed(cur_final_page_for_test)
    print(set_of_sale_pages_1_room)
    sleep(3)
    GetDataForCurFlat(set_of_sale_pages_1_room)
    sleep(2)

    GetSetOfSalePagesUrls_2Bed(cur_final_page_for_test)
    print(set_of_sale_pages_2_room)
    sleep(3)
    GetDataForCurFlat(set_of_sale_pages_2_room)
    sleep(2)

    GetSetOfSalePagesUrls_3Bed(cur_final_page_for_test)
    print(set_of_sale_pages_3_room)
    sleep(3)
    GetDataForCurFlat(set_of_sale_pages_3_room)

    DataToCSVFile(list_with_all_flats_data)

RunParseCian() #запуск с одной функции