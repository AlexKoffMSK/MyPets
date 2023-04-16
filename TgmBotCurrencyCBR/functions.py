import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd


def GetBSSourceDataFromCBRFByDate(day, month, year):
    print("Run", GetBSSourceDataFromCBRFByDate.__name__)
    #https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To=01.07.1992
    main_part_of_page_address_str = 'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To='
    headers_to_send = {"User-Agent": UserAgent().random}
    response = requests.get(main_part_of_page_address_str + day + '.' + month + '.' + year, headers = headers_to_send).text
    soup = BeautifulSoup(response, 'lxml')
    return soup


def MakeDataFrameFromCurLink(soup_source):
    print("Run", MakeDataFrameFromCurLink.__name__)
    tables = soup_source.find_all('table')
    rows = tables[0].find_all('tr')  # теперь все ряды в таблице
    df = pd.DataFrame()
    df['Цифр.код'] = [rows[i].find_all('td')[0].text for i in range(1,len(rows))]
    df['Букв.код'] = [rows[i].find_all('td')[1].text for i in range(1,len(rows))]
    df['Единиц'] = [rows[i].find_all('td')[2].text for i in range(1,len(rows))]
    df['Валюта'] = [rows[i].find_all('td')[3].text for i in range(1,len(rows))]
    df['Курс'] = [rows[i].find_all('td')[4].text for i in range(1,len(rows))]
    return df