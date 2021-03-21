import xmltodict as xmldict


def readXml(filePath: str) -> dict:
    """
    # :filePath is xml file
    """
    try:
        with open(filePath) as file:
            return xmldict.parse(file.read())
    except Exception as e:
        print(e)
        return {}
