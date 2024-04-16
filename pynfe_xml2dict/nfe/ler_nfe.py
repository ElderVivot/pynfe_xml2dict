from typing import Union, Dict, List

from pynfe_xml2dict.utils.functions import returnDataInDictOrArray
from pynfe_xml2dict.utils.read_xml import readXml, readXmlFromStr
from .__tag_ide__ import TagIde
from .__tag_emit__ import TagEmit
from .__tag_dest__ import TagDest
from .__tag_det__ import TagDet
from .__tag_total__ import TagTotal


class LerNfe():
    def __init__(self, caminhoXml: str = None, xmlDados: str = None, tagsPrincipaisPraLer: List[str] = []):
        if caminhoXml is None and xmlDados is not None:
            self.__dataXml = readXmlFromStr(xmlDados)
        elif caminhoXml is not None:
            self.__dataXml = readXml(caminhoXml)
        else:
            raise Exception('Its necessary pass as argument caminhoXml or xmlDados')

        self.__tagsPrincipaisPraLer = tagsPrincipaisPraLer

        self.__objNf: Dict['str', dict] = {}

    def __isNfe(self):
        keyNf = returnDataInDictOrArray(self.__dataXml, ['nfeProc', 'NFe', 'infNFe', '@Id'])
        return True if keyNf != '' else False

    def __tagIde(self):
        if self.__tagsPrincipaisPraLer.count('ide') > 0 or len(self.__tagsPrincipaisPraLer) == 0:
            dataTagIde = returnDataInDictOrArray(self.__dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide'])
            tagIde = TagIde(dataTagIde)
            self.__objNf['identificao_nfe'] = tagIde.getData()
        else:
            self.__objNf['identificao_nfe'] = {}

    def __tagEmit(self):
        if self.__tagsPrincipaisPraLer.count('emit') > 0 or len(self.__tagsPrincipaisPraLer) == 0:
            dataTagEmit = returnDataInDictOrArray(self.__dataXml, ['nfeProc', 'NFe', 'infNFe', 'emit'])
            tagEmit = TagEmit(dataTagEmit)
            self.__objNf['emitente'] = tagEmit.getData()
        else:
            self.__objNf['emitente'] = {}

    def __tagDest(self):
        if self.__tagsPrincipaisPraLer.count('dest') > 0 or len(self.__tagsPrincipaisPraLer) == 0:
            dataTagDest = returnDataInDictOrArray(self.__dataXml, ['nfeProc', 'NFe', 'infNFe', 'dest'])
            tagDest = TagDest(dataTagDest)
            self.__objNf['destinatario'] = tagDest.getData()
        else:
            self.__objNf['destinatario'] = {}

    def __tagDet(self):
        if self.__tagsPrincipaisPraLer.count('det') > 0 or len(self.__tagsPrincipaisPraLer) == 0:
            listTagsDet = []

            dataTagDet = returnDataInDictOrArray(self.__dataXml, ['nfeProc', 'NFe', 'infNFe', 'det'])
            if type(dataTagDet) == list:
                listTagsDet = dataTagDet
            else:
                listTagsDet.append(dataTagDet)

            tagDet = TagDet(listTagsDet)
            self.__objNf['dados_produtos'] = tagDet.getData()
        else:
            self.__objNf['dados_produtos'] = []

    def __tagTotal(self):
        if self.__tagsPrincipaisPraLer.count('total') > 0 or len(self.__tagsPrincipaisPraLer) == 0:
            dataTagTotal = returnDataInDictOrArray(self.__dataXml, ['nfeProc', 'NFe', 'infNFe', 'total'])
            tagTotal = TagTotal(dataTagTotal)
            self.__objNf['total'] = tagTotal.getData()
        else:
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
