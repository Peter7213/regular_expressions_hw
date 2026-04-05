from pprint import pprint
import re
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


new_contacts_list = [{} for _ in range(len(contacts_list))]
for rubric in contacts_list[0]:
    for subdict in new_contacts_list:
        subdict.setdefault(rubric, None)
contacts_list.pop(0)
dict_index = 0

def find_person(new_contacts_list, names_data):
    for index, subdict in enumerate(new_contacts_list):
        if (subdict['lastname'], subdict['firstname']) == names_data:
            return index
    return None

for sublist in contacts_list:                               #Извлечение ФИО
    line = ' '.join(sublist)
    pattern = r'\b[А-ЯЁ][а-яёa-z]*\b'
    matches_n = re.findall(pattern, line)
    contact = matches_n[:3]
    names_data = (contact[0], contact[1])
    index = find_person(new_contacts_list, names_data)              #Проверка есть ли запись в словаре
    if not index:
        new_contacts_list[dict_index].update({'lastname':contact[0], 'firstname':contact[1], 'surname':contact[2]})

    index = find_person(new_contacts_list, names_data)              #Повторный запрос уже определенного индекса

    try:
        match_org = re.search(fr"{contact[2]}\s+(\w+)", line)
        organization = match_org.group(1).strip()
        new_contacts_list[index].update({'organization':organization})
    except:
        pass

    try:
        match_position = re.search(rf"{organization}(.+?)(?=\+|[0-9]|\s*$)", line)
        position = match_position.group(1).strip()
        new_contacts_list[index].update({'position': position})
    except:
        pass

    try:
        correctional_pattern = r'(\+?7|8)[-\s]?\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})(\s+\(?)?'
        replacement_pattern = r"+7(\2)\3-\4-\5 "
        line_corrected = re.sub(correctional_pattern, replacement_pattern, line)
        correctional_pattern_2 = r'\(?\доб.?\s*(\d{4})'
        replacement_pattern_2 = r'доб.\1'
        line_corrected_again = re.sub(correctional_pattern_2, replacement_pattern_2, line_corrected)
        search_pattern = r'(\+?7|8)[-\s]?\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})(\s+\(?\доб.?\s*\d{4})?'
        phone_match = re.search(search_pattern, line_corrected_again)
        phone = phone_match.group()
        new_contacts_list[index].update({'phone': phone})
    except:
        pass

    try:
        search_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
        match_email = re.search(search_pattern, line)
        new_contacts_list[index].update({'email': match_email[0]})
    except:
        pass
    dict_index += 1

for ind, subdict in enumerate(new_contacts_list):
    if not subdict['lastname']:
        new_contacts_list.pop(ind)

titles = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
with open('new_phonebook.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=titles)
    writer.writeheader()
    writer.writerows(new_contacts_list)