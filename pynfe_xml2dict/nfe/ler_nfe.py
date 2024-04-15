from typing import Union, Dict

from pynfe_xml2dict.utils.functions import returnDataInDictOrArray
from pynfe_xml2dict.utils.read_xml import readXml, readXmlFromStr
from .__tag_ide__ import TagIde
from .__tag_emit__ import TagEmit
from .__tag_dest__ import TagDest
from .__tag_det__ import TagDet


class LerNfe():
    def __init__(self, pathXml: str = None, xmlData: str = None):
        if pathXml is None and xmlData is not None:
            self.__dataXml = readXmlFromStr(xmlData)
        elif pathXml is not None:
            self.__dataXml = readXml(pathXml)
        else:
            raise Exception('Its necessary pass as argument pathXml or xmlData')

        self.__objNf: Dict['str', dict] = {}

    def __isNfe(self):
        keyNf = returnDataInDictOrArray(self.__dataXml, ['nfeProc', 'NFe', 'infNFe', '@Id'])
        return True if keyNf != '' else False

    def __tagIde(self):
        dataTagIde = returnDataInDictOrArray(self.__dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide'])
        tagIde = TagIde(dataTagIde)
        self.__objNf['identificao_nfe'] = tagIde.getData()

    def __tagEmit(self):
        dataTagEmit = returnDataInDictOrArray(self.__dataXml, ['nfeProc', 'NFe', 'infNFe', 'emit'])
        tagEmit = TagEmit(dataTagEmit)
        self.__objNf['emitente'] = tagEmit.getData()

    def __tagDest(self):
        dataTagDest = returnDataInDictOrArray(self.__dataXml, ['nfeProc', 'NFe', 'infNFe', 'dest'])
        tagDest = TagDest(dataTagDest)
        self.__objNf['destinatario'] = tagDest.getData()

    def __tagDet(self):
        listTagsDet = []

        dataTagDet = returnDataInDictOrArray(self.__dataXml, ['nfeProc', 'NFe', 'infNFe', 'det'])
        if type(dataTagDet) == list:
            listTagsDet = dataTagDet
        else:
            listTagsDet.append(dataTagDet)

        tagDet = TagDet(listTagsDet)
        self.__objNf['dados_produtos'] = tagDet.getData()

    def __tagTotal(self):
        # implement to get this information
        self.__objNf['total'] = {}

    def process(self) -> Union[dict, None]:
        isNfe = self.__isNfe()
        if isNfe is False:
            return None

        self.__objNf['chave_nota'] = returnDataInDictOrArray(self.__dataXml, ['nfeProc', 'NFe', 'infNFe', '@Id'])[3:]
        self.__tagIde()
        self.__tagEmit()
        self.__tagDest()
        self.__tagDet()
        self.__tagTotal()

        return self.__objNf
