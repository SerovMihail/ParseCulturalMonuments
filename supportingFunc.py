import re

def removeAllUseless(text):
    """
    Для удаления лишнего из текста
    :param text:
    :return text:
    """
    result = re.sub("^\s+|\n|\r|\s+$", '', text) # Убирает все отступы, переносы, пробелы

    return result

