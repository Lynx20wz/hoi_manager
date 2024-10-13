import json
from loguru import logger

logger.remove()
logger.add(
        sink='logs/get_name.log',
        level='INFO',
        mode='w',
        format='{time:H:mm:ss} | <level>{level}</level> | {message}',
)


def bootstrap_id():
    global tag_countries
    try:
        with open('tag_countries.json', 'r', encoding='UTF_8') as file_json:
            tag_countries = json.loads(file_json.read())
            logger.info(f'Подгружены id стран')
    except:
        logger.critical('не удалось загрузить id стран')


def get_name_with_help_id(name: str) -> str:
    if len(name) == 3:  # название из тега
        try:
            logger.info(f'{name} - {tag_countries.get(name)[0]}')
            return tag_countries.get(name)[0]
        except TypeError:
            pass
    for k, s in tag_countries.items():  # тег по названию
        for s in s:
            if s == name:
                logger.info(f'{name} - {k}')
                return k
    return 'None'


bootstrap_id()
