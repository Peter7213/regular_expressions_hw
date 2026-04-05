from pprint import pprint
import re
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

def check_names(c_list, contact):
    for index, sub_list in enumerate(c_list):
        if contact[0] and contact[1] in sub_list:
            return index, 'exists'
    return None, 'not_exists'


    
new_contacts_list = []
new_contacts_list.append(contacts_list[0])
contacts_list.pop(0)

for sublist in contacts_list:                               #Извлечение ФИО
    line = ' '.join(sublist)
    pattern = r'\b[А-ЯЁ][а-яёa-z]*\b'
    matches_n = re.findall(pattern, line)
    contact = matches_n[:3]
    index, in_list = check_names(new_contacts_list, contact)         #Доп. переменная для проверки наличия контакта в базе
    if in_list == 'not_exists':
        new_contacts_list.append(contact)
        index = len(new_contacts_list) - 1


    try:
        match_org = re.search(fr"{contact[2]}\s+(\w+)", line)
        organization = match_org.group(1).strip()
        if organization not in new_contacts_list[index]:
            new_contacts_list[index].insert(3, organization)
    except: pass

    try:
        match_position = re.search(rf"{organization}(.+?)(?=\+|[0-9]|\s*$)", line)
        position = match_position.group(1).strip()
        new_contacts_list[index].insert(4, position)
        del new_contacts_list[index][5]                                         #Хардкод, знаю. Не могу сообразить как решить иначе
    except: pass

    try:
        correctional_pattern = r'(\+?7|8)[-\s]?\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})(\s+\(?)?'
        replacement_pattern = r"+7(\2)\3-\4-\5 "
        line_corrected = re.sub(correctional_pattern, replacement_pattern, line)
        search_pattern = r'(\+?7|8)[-\s]?\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})(\s+\(?\доб.?\s*\d{4})?'
        phone_match = re.search(search_pattern, line_corrected)
        phone = phone_match.group()
        new_contacts_list[index].insert(5, phone.strip())

    except: pass

    try:
        search_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
        match_email = re.search(search_pattern, line)
        new_contacts_list[index].insert(6, match_email[0])

    except: pass


with open("phonebook.csv", "w", newline='', encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(new_contacts_list)

if __name__ == '__main__':
    pass