import csv
import re


def parcing_file(file_name):
    try:
        with open(file_name, encoding='utf-8') as f:
            rows = csv.reader(f, delimiter=",")
            contacts_list = list(rows)
            contacts_head = contacts_list[0]
            contacts_list = contacts_list[1:]
            return contacts_head,contacts_list
    except Exception as e:
        print(f'Не удалось извлечь данные из файла {file_name} по причине: {e}')


def struct_contacts_list(contacts_list):
    for contact in contacts_list:
        if len(contact) >= 7:
            #Структурируем ФИО
            reg_name = re.compile(r'^(\w*)\W+(\w*)\W+(\w*)\W*')
            result_name = reg_name.match(f'{contact[0]} {contact[1]} {contact[2]}')
            contact[0] = result_name.group(1) if result_name.group(1) else ''
            contact[1] = result_name.group(2) if result_name.group(2) else ''
            contact[2] = result_name.group(3) if result_name.group(3) else ''
            #Структурируем телефон при наличии
            reg_phone = re.compile(r"([\\+7|8])*[\D]*(\d+)[\D]*(\d*)[\D]*(\d*)[\D]*(\d*)[\D]*(\d*)")
            result_phone = reg_phone.match(f'{contact[5]}')
            if result_phone:
                main_phone = f'{result_phone.group(2)}{result_phone.group(3)}{result_phone.group(4)}{result_phone.group(5)}'
                contact[5] = f'+7({main_phone[0:3]}){main_phone[3:6]}-{main_phone[6:8]}-{main_phone[8:]}'
                if result_phone.group(6):
                    contact[5] += f' доб.{result_phone.group(6)}'
        else:

            print(f'Некорретные данные в строке {contact}')
    return contacts_list


def find_double(contacts_list):
    contacts_list_no_double = []
    while len(contacts_list):
        if len(contacts_list[0]) >= 7:
            current_fname = contacts_list[0][0]
            current_lname = contacts_list[0][1]
            current_all_index = []
            # Ищем совпадения по имени
            for index, contact in enumerate(contacts_list):
                if (contact[0] == current_fname) and (contact[1] == current_lname):
                    current_all_index.append(index)
            # Если контакт уникальный берем его и записываем
            if len(current_all_index) == 1:
                contacts_list_no_double.append(contacts_list[current_all_index[0]])
            else:
            # Если контакт не уникальный то берем "склеиваем" по совпадающим Фамилии и Имени данные
                surname, organization, position, phone, email = '', '', '', '', ''
                for index in current_all_index:
                    surname = contacts_list[index][2] if contacts_list[index][2] > surname else surname
                    organization = contacts_list[index][3] if contacts_list[index][3] > organization else organization
                    position = contacts_list[index][4] if contacts_list[index][4] > position else position
                    phone = contacts_list[index][5] if contacts_list[index][5] > phone else phone
                    email = contacts_list[index][6] if contacts_list[index][6] > email else email
                contacts_list_no_double.append([current_fname, current_lname, surname,
                                                organization, position, phone, email])
            current_all_index.reverse()
            for index in current_all_index:
                contacts_list.pop(index)
        else:
            contacts_list.pop(0)

    return contacts_list_no_double


def write_csv_file(file_name, contacts_head, contacts_list):
    try:
        with open(file_name, 'w', encoding='utf-8', newline='') as f:
            datawriter = csv.writer(f, delimiter=',')
            # Вместо contacts_list подставьте свой список
            contacts_list.insert(0, contacts_head)
            datawriter.writerows(contacts_list)
            return True
    except Exception as e:
        print(f'Не удалось сохранить записную книгу в файл {file_name} по причине: {e}')


if __name__ == '__main__':
    while True:
        file_name_in = input('Попробуем считать данные контактов из файла.\n'
                             'Введите имя файла или нажмите Enter для чтения файла phonebook_raw.csv: ')
        if not file_name_in:
            file_name_in = "phonebook_raw.csv"

        contacts_in = parcing_file(file_name_in)
        if contacts_in:
            contacts_head, contacts_list_in = contacts_in
            contacts_list_out = find_double(struct_contacts_list(contacts_list_in))
            print('Стурктурированные данные контактов:')
            print(contacts_head)

            for contact in contacts_list_out:
                print(contact)
            file_name_out = input('Попробуем записать данные контактов в файл.\n'
                                  'Введите имя файла для сохранения данных')
            if not file_name_out:
                file_name_out = "phonebook.csv"
                print(f'Хорошо запишу в {file_name_out}')
            if write_csv_file(file_name_out, contacts_head, contacts_list_out):
                print('Файл успешно записан')
        else:
            print('Не удалось получить данные')
        if input('Попробуем еще раз?(y)').upper() != 'Y':
            break
