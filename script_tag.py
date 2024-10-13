import re

with open('tag.txt', 'r') as file:
    for line in file:
        tag = line[0:3]
        point_position = line.find('.')
        name_eng = line[17:point_position].lower()

        with open('ru.txt', 'r', encoding='UTF-8') as rus_file:
            for rus_line in rus_file:
                pattern = f'^{tag}: '
                if re.match(pattern, rus_line):
                    start_id = rus_line.find(f'"')
                    end_id = rus_line.rfind(f'"')
                    name_rus = rus_line[start_id + 1:end_id].lower()

        with open('tag_dict.txt', 'a', encoding='UTF-8') as end_file:
            tag_countries = f"'{tag}': ['{name_eng}', '{name_rus}'],\n"
            end_file.write(tag_countries)
