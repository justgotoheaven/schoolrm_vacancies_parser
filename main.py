from parser import Parser
import datetime

if __name__ == '__main__':
    print('\n\n\tПарсер вакансий школ. Время: ' + str(datetime.datetime.now()))
    print('\tНачата работа парсера...')
    init_time = datetime.datetime.now()
    parser = Parser(filename='vacancies.txt')
    parser.parse_vacancies()
    end_time = datetime.datetime.now()
    print('\tРабота парсера окончена. Данные доступны в файле ' +
          parser.get_filename() + '\n\tВремя работы парсера: ' + str(end_time - init_time))
