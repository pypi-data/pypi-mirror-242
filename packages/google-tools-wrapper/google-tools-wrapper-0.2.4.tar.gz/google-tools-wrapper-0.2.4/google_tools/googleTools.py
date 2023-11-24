import os
import platform
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs
import requests

def cls():
    os_name = platform.system().lower()
    if os_name == 'windows':
        os.system('cls')
    else:
        os.system('clear')

def wrapper(url: str, translater_selenium_method=False):
    if translater_selenium_method is True:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
            cls()
            driver.get(url)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'ryNqvb')))
            page_code = driver.page_source
            driver.quit()
            soup = bs(page_code, 'html.parser')
        except (Exception or TimeoutException) as err:
            return f"Something went wrong! Error: {str(err)}"
    else:
        try:
            resp = requests.get(url)
            soup = bs(resp.content, 'html.parser')
        except Exception as err:
            return f"Something went wrong! Error: {str(err)}"
    return soup

class GoogleTools:
    ## FINE
    def currency_conversion(base_currency: str, target_currency: str, only_float=True):
        url_ = f"https://www.google.com/finance/quote/{base_currency.upper()}-{target_currency.upper()}"
            
        soup = wrapper(url=url_)
        
        currency_value = float(f"{float(soup.find('div', attrs={'class': 'YMlKec fxKbKc'}).text):.2f}")
        last_update_ = soup.find('div', attrs={'class': 'ygUjEc', 'jsname': 'Vebqub'}).text.replace('\u202f', ' ').replace(' · Disclaimer', '')

        conversion_dict = {
            'conversion': [
                f'1 {base_currency}',
                f'{currency_value} {target_currency}'
            ],
            'float': (1, currency_value),
            'last_update': last_update_
        }

        if only_float is not True:
            return conversion_dict
        else:
            return conversion_dict['float']

    def translater(source_language: str, target_language: str, text: str):
        text = text.replace(' ', '%20') # deixando apropriado para o url
        
        url_ = f'https://translate.google.com/?sl={source_language}&tl={target_language}&text={text}&op=translate'

        soup = wrapper(url_, True)

        translated_text = soup.find('span', class_='ryNqvb').text
        if translated_text is not None:
            return translated_text
        else:
            return f"Something went wrong! The translated text is NoneType, may you requesting too much!"
        
    ## TODO
    def bard_api(question: str):
        print('under development')
    
class GoogleToolsTests:
    def test_currency_conversion():
        print("\nTESTING CURRENCY CONVERSION:\n")
        result1 = GoogleTools.currency_conversion('USD', 'BRL', False)
        result2 = GoogleTools.currency_conversion('USD', 'BRL', True)
        print(f"first result:\n{result1}\n")
        print(f"sec result:\n{result2}")
    
    def test_translater():
        print("\nTESTING TRANSLATER:\n")
        result = GoogleTools.translater('pt', 'en', 'Olá, eu me chamo João!')
        print(result)

if __name__ == '__main__':
    tests = GoogleToolsTests

    #tests.test_currency_conversion()
    tests.test_translater()
