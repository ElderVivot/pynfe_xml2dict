import xmltodict as xmldict
import platform
from codecs import open


def readXml(filePath: str) -> dict:
    """
    # :filePath is xml file
    """
    try:
        if platform.system() == 'Windows':
            with open(filePath, 'rb', encoding='latin1') as file:
                return xmldict.parse(file.read())
        else:
            with open(filePath, 'rb') as file:
                return xmldict.parse(file.read())
    except Exception as e:
        print(e)
        return {}
