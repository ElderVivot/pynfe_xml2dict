import xmltodict as xmldict
from codecs import open


def readXml(filePath: str) -> dict:
    """
    # :filePath is xml file
    """
    try:
        with open(filePath, 'r') as file:
            return xmldict.parse(file.read())
    except Exception as e:
        print(e)
        return {}
