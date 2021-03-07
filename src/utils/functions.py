import unicodedata
import re
import datetime


def getOnlyNameFile(nameFileOriginal):
    nameFileSplit = nameFileOriginal.split('.')
    nameFile = '.'.join(nameFileSplit[:-1])
    return nameFile


def getDateTimeNowInFormatStr():
    dateTimeObj = datetime.datetime.now()
    return dateTimeObj.strftime("%Y_%m_%d_%H_%M")


def removeCharsSpecial(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra).encode('ASCII', 'ignore').decode('ASCII')
    palavraTratada = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com valores corretos
    return re.sub('[^a-zA-Z0-9.!+:><=)?$(/*,\-_ \\\]', '', palavraTratada)


def minimalizeSpaces(text):
    _result = text
    while ("  " in _result):
        _result = _result.replace("  ", " ")
    _result = _result.strip()
    return _result


def searchPositionFieldForName(header, nameField=''):
    nameField = treatTextField(nameField)
    try:
        return header[nameField]
    except Exception:
        return None


def analyzeIfFieldIsValid(data, name, returnDefault=""):
    try:
        return data[name]
    except Exception:
        return returnDefault


def analyzeIfFieldHasPositionInFileEnd(data, positionInFile, positionInFileEnd):
    positionInFile = positionInFile - 1

    try:
        if positionInFileEnd <= 0:
            return data[positionInFile]
        else:
            return ''.join(data[positionInFile:positionInFileEnd])
    except Exception:
        return ""


def analyzeIfFieldIsValidMatrix(data, position, returnDefault="", positionOriginal=False):
    """
    # :data é o vetor com as informações
    # :position a posição que a informação que quero retornar se encontra no vetor
    # :returnDefault caso não encontre a posição qual valor deve retornar
    # :positionOriginal é pra não subtrair por menos 1 o retorno, por padrão eu passo o número normal e ele subtrai um
    # visto que o vetor
    # começa com zero. Quando True ele não faz esta substração.
    """
    try:
        if positionOriginal is False:
            return data[position - 1]
        else:
            return data[position]
    except Exception:
        return returnDefault


def treatTextField(value):
    try:
        value = str(value)
        return minimalizeSpaces(removeCharsSpecial(value.strip().upper()))
    except Exception:
        return ""


def treatTextFieldInVector(data, numberOfField=0, fieldsHeader=[], nameFieldHeader='', positionInFileEnd=0,
                           keepTextOriginal=True):
    """
    :param data: Informar o array de dados que quer ler
    :param numberOfField: numero do campo na planilha (opcional)
    :param fieldsHeader: linha do cabeçalho armazenado num vetor (opcional)
    :param nameFieldHeader: nome do cabeçalho que é pra buscar (opcional)
    :return: retorna um campo como texto, retirando acentos, espaços excessivos, etc
    """
    if len(fieldsHeader) > 0 and nameFieldHeader is not None and nameFieldHeader != "":
        try:
            value = data[searchPositionFieldForName(fieldsHeader, nameFieldHeader)]
            return treatTextField(value) if keepTextOriginal is True else value
        except Exception:
            try:
                value = analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd)
                return treatTextField(value) if keepTextOriginal is True else value
            except Exception:
                return ""
    else:
        try:
            value = analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd)
            return treatTextField(value) if keepTextOriginal is True else value
        except Exception:
            return ""


def treatDecimalField(value, numberOfDecimalPlaces=2):
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


def treatDecimalFieldInVector(data, numberOfField=0, fieldsHeader=[], nameFieldHeader='', row='main',
                              positionInFileEnd=0):
    """
    :param data: Informar o array de dados que quer ler
    :param numberOfField: numero do campo na planilha (opcional)
    :param fieldsHeader: linha do cabeçalho armazenado num vetor (opcional)
    :param nameFieldHeader: nome do cabeçalho que é pra buscar (opcional)
    :param row: este serve pra caso não seja um pagamento que esteja na linha principal (que não tem cabeçalho, então
    pegar apenas pelo número do campo). O valor 'main' quer dizer que tá numa linha que pode ter cabeçalho
    :return: retorna um campo como decimal
    """
    if len(fieldsHeader) > 0 and nameFieldHeader is not None and nameFieldHeader != "":
        try:
            if row == 'main':
                return treatDecimalField(data[searchPositionFieldForName(fieldsHeader, nameFieldHeader)])
            else:
                return treatDecimalField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd))
        except Exception:
            try:
                return treatDecimalField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd))
            except Exception:
                return float(0)
    else:
        try:
            return treatDecimalField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd))
        except Exception:
            return float(0)


def treatDateField(valorCampo, formatoData=1):
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


def treatDateFieldInVector(data, numberOfField=0, fieldsHeader=[], nameFieldHeader='', formatoData=1, row='main',
                           positionInFileEnd=0):
    """
    :param data: Informar o array de dados que quer ler
    :param numberOfField: numero do campo na planilha (opcional)
    :param fieldsHeader: linha do cabeçalho armazenado num vetor (opcional)
    :param nameFieldHeader: nome do cabeçalho que é pra buscar (opcional)
    :param formatoData: 1 = 'DD/MM/YYYY' ; 2 = 'YYYY-MM-DD (opcional)
    :param row: este serve pra caso não seja um pagamento que esteja na linha principal (que não tem cabeçalho, então 
    pegar apenas pelo número do campo). O valor 'main' quer dizer que tá numa linha que pode ter cabeçalho
    :return: retorna um campo como decimal
    """
    if len(fieldsHeader) > 0 and nameFieldHeader is not None and nameFieldHeader != "":
        try:
            if row == 'main':
                return treatDateField(data[searchPositionFieldForName(fieldsHeader, nameFieldHeader)], formatoData)
            else:
                return treatDateField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd),
                                      formatoData)
        except Exception:
            try:
                return treatDateField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd),
                                      formatoData)
            except Exception:
                return None
    else:
        try:
            return treatDateField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd),
                                  formatoData)
        except Exception:
            return None


def treatNumberField(value, isInt=False):
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


def treatNumberFieldInVector(data, numberOfField=-1, fieldsHeader=[], nameFieldHeader='', isInt=False, positionInFileEnd=0):
    """
    :param data: Informar o array de dados que quer ler
    :param numberOfField: numero do campo na planilha (opcional)
    :param fieldsHeader: linha do cabeçalho armazenado num vetor (opcional)
    :param nameFieldHeader: nome do cabeçalho que é pra buscar (opcional)
    :return: retorna um campo apenas como número
    """
    if len(fieldsHeader) > 0 and nameFieldHeader is not None and nameFieldHeader != "":
        try:
            return treatNumberField(data[searchPositionFieldForName(fieldsHeader, nameFieldHeader)], isInt)
        except Exception:
            try:
                return treatNumberField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd), isInt)
            except Exception:
                return 0
    else:
        try:
            return treatNumberField(analyzeIfFieldHasPositionInFileEnd(data, numberOfField, positionInFileEnd), isInt)
        except Exception:
            return 0
