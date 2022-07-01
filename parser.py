from bs4 import BeautifulSoup
import requests
from config import SELECT_CITY_LINK, CITY_ID


class Parser:

    def __init__(self, filename='vacancies.txt'):
        self.__city = CITY_ID
        self.__select_link = SELECT_CITY_LINK
        self.session = requests.Session()
        self.soup = None
        self.__vacancy_url = 'https://{}/sveden/employees/jobs/'
        self.__filename = filename

    def get_filename(self):
        return self.__filename

    def get_schools_dict(self):
        data = dict(id=self.__city)
        response = self.session.post(self.__select_link, data)
        self.soup = BeautifulSoup(response.text, 'lxml')
        options = self.soup.find_all('option')
        schools = dict()
        for option in options[1:]:
            schools[option.text] = option['value']
        return schools

    def __get_school_data(self, url):
        req = self.session.post('https://' + url)
        self.soup = BeautifulSoup(req.text, 'lxml')
        school_name = self.soup.find('div', class_='name_school')
        data = list()
        school_name_pretty = school_name.text.strip().replace('\n', ''). \
            replace('                        		', ' ')
        data.append(school_name_pretty)
        school_adr_and_phone = self.soup.find('div', class_='address_block')
        school_adr_pretty = school_adr_and_phone.text.strip().split('Телефон')[0]. \
            replace('            			                                        ', '').replace('Адрес:', '')
        data.append(school_adr_pretty)
        school_phone = school_adr_and_phone.text.split('Телефон:')[1].split('Контакты')[0].strip()
        data.append(school_phone)
        return data

    def __get_school_vacancies(self, url):
        req = self.session.post(self.__vacancy_url.format(url))
        self.soup = BeautifulSoup(req.text, 'lxml')
        block = self.soup.find('div', id='center_block')
        vacancies = list()
        try:
            vac_list = block.find_all('td', class_='first_td')
            for vac in vac_list:
                vacancies.append(vac.text)
        except:
            pass
        return vacancies

    def parse_vacancies(self):
        with open(self.__filename, 'w') as file:
            schools = self.get_schools_dict()
            schools_list = schools.keys()
            for s in schools_list:
                row_data = self.__get_school_data(schools[s])
                file.write('Школа: {}\nАдрес: {}\nТелефоны: {}\n'.format(row_data[0], row_data[1], row_data[2]))
                file.write('Вакансии: ')
                vac_data = self.__get_school_vacancies(schools[s])
                file.write(','.join(vac_data)) if vac_data else file.write('нет вакансий')
                file.write('\n\n\n')
