import unicodedata
import re
import datetime
from typing import List, Any


def removeCharsSpecialTwo(text: str):
    charSpecials = '!+:>;<=)?$(/*@#$?|'
    for char in charSpecials:
        text = text.replace(char, '')
    return text


def removeCharsSpecial(text: str):
    try:
        text = text.replace('[', '')
        text = text.replace(']', '')
        # Unicode normalize transforma um caracter em seu equivalente em latin.
        nfkd = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        text = u"".join([c for c in nfkd if not unicodedata.combining(c)])

        # Usa expressão regular para retornar a palavra apenas com valores corretos
        text = re.sub('[^a-zA-Z0-9.!+:>;<=)?$(/*,-_ \\]', '', text)
        return text
    except Exception:
        text = removeCharsSpecialTwo(text)
        return text


def minimalizeSpaces(text):
    _result = text
    while ("  " in _result):
        _result = _result.replace("  ", " ")
    _result = _result.strip()
    return _result


def treatsFieldAsText(value):
    try:
        value = str(value)
        return minimalizeSpaces(removeCharsSpecial(value.strip().upper()))
    except Exception:
        return ""


def treatsFieldAsDecimal(value, numberOfDecimalPlaces=2):
    if type(value) == float:
        return value
    try:
        value = str(value)
        value = re.sub('[^0-9.,-]', '', value)
        if value.find(',') >= 0 and value.find('.') >= 0:
            value = value.replace('.', '')

        if value.find(',') >= 0:
            value = value.replace(',', '.')

        if value.find('.') < 0:
            value = int(value)

        return float(value)
    except Exception:
        return float(0)


def treatsFieldAsDate(valorCampo, formatoData=1):
    """
    :param valorCampo: Informar o campo string que será transformado para DATA
    :param formatoData: 1 = 'DD/MM/YYYY' ; 2 = 'YYYY-MM-DD' ; 3 = 'YYYY/MM/DD' ; 4 = 'DDMMYYYY'
    :return: retorna como uma data. Caso não seja uma data válida irá retornar None
    """
    if type(valorCampo) == 'datetime.date':
        return valorCampo

    valorCampo = str(valorCampo).strip()

    lengthField = 10  # tamanho padrão da data são 10 caracteres, só muda se não tiver os separados de dia, mês e ano

    if formatoData == 1:
        formatoDataStr = "%d/%m/%Y"
    elif formatoData == 2:
        formatoDataStr = "%Y-%m-%d"
    elif formatoData == 3:
        formatoDataStr = "%Y/%m/%d"
    elif formatoData == 4:
        formatoDataStr = "%d%m%Y"
        lengthField = 8
    elif formatoData == 5:
        formatoDataStr = "%d/%m/%Y"
        valorCampo = valorCampo[0:6] + '/20' + valorCampo[6:]
    elif formatoData == 6:
        formatoDataStr = "%d%m%Y"

    try:
        return datetime.datetime.strptime(valorCampo[:lengthField], formatoDataStr).date()
    except ValueError:
        return None


def treatsFieldAsNumber(value, isInt=True):
    if type(value) == int:
        return value
    try:
        value = re.sub("[^0-9]", '', value)
        if value == "":
            return 0
        else:
            if isInt is True:
                try:
                    return int(value)
                except Exception:
                    return 0
            return value
    except Exception:
        return 0


def returnDataInDictOrArray(data: Any, arrayStructureDataReturn: List[Any], valueDefault='') -> Any:
    """
    :data: vector, matrix ou dict with data -> example: {"name": "Obama", "adress": {"zipCode": "1234567"}}
    :arrayStructureDataReturn: array in order with position of vector/matriz or name property of dict to \
    return -> example: ['adress', 'zipCode'] -> return is '1234567'
    """
    try:
        dataAccumulated = ''
        for i in range(len(arrayStructureDataReturn)):
            if i == 0:
                dataAccumulated = data[arrayStructureDataReturn[i]]
            else:
                dataAccumulated = dataAccumulated[arrayStructureDataReturn[i]]
        return dataAccumulated
    except Exception:
        return valueDefault
