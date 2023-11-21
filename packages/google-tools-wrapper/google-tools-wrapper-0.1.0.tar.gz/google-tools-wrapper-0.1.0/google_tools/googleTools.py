import requests
from bs4 import BeautifulSoup as bs

class GoogleTools:
    class Finances:
        def currency_conversion(base_currency: str, target_currency: str, only_float=True):
            url = f"https://www.google.com/finance/quote/{base_currency}-{target_currency}"
            
            # requesting
            try:
                resp = requests.get(url)
                soup = bs(resp.text, 'html.parser')
            except Exception as err:
                return f"Something went wrong! Error: {str(err)}"
            finally:
                currency_value = round(float(str(soup.find('div', class_='YMlKec fxKbKc')).replace('<div class="YMlKec fxKbKc">', '').replace('</div>', '')), 2)
                last_update_ = str(soup.find('div', class_='ygUjEc')).replace('<div class="ygUjEc" jsname="Vebqub">', '').replace(' · <a href="https://www.google.com/intl/en-US_BR/googlefinance/disclaimer/"><span class="koPoYd">Disclaimer</span></a></div>', '').replace('\u202f', ' ')
            
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

if __name__ == '__main__':
    result = GoogleTools.Finances.currency_conversion('USD', 'BRL', False)
    print(result)
