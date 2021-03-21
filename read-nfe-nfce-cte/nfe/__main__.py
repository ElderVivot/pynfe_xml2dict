import os
import sys
from typing import Union, Dict

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.functions import returnDataInDictOrArray
from utils.read_xml import readXml
from nfe.tag_ide import TagIde
from nfe.tag_emit import TagEmit
from nfe.tag_det import TagDet


class IndexNfe():
    def __init__(self, pathXml: str):
        self._dataXml = readXml(pathXml)
        self._objNf: Dict['str', dict] = {}

    def _isNfe(self):
        keyNf = returnDataInDictOrArray(self._dataXml, ['nfeProc', 'NFe', 'infNFe', '@Id'])
        return True if keyNf != '' else False

    def _tagIde(self):
        dataTagIde = returnDataInDictOrArray(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'ide'])
        tagIde = TagIde(dataTagIde)
        self._objNf['identificao_nfe'] = tagIde.getData()

    def _tagEmit(self):
        dataTagEmit = returnDataInDictOrArray(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'emit'])
        tagEmit = TagEmit(dataTagEmit)
        self._objNf['emitente'] = tagEmit.getData()

    def _tagDet(self):
        listTagsDet = []

        dataTagDet = returnDataInDictOrArray(self._dataXml, ['nfeProc', 'NFe', 'infNFe', 'det'])
        if type(dataTagDet) == list:
            listTagsDet = dataTagDet
        else:
            listTagsDet.append(dataTagDet)

        tagDet = TagDet(listTagsDet)
        self._objNf['dados_produtos'] = tagDet.getData()

    def _tagTotal(self):
        # implement to get this information
        self._objNf['total'] = {}

    def process(self) -> Union[dict, None]:
        isNfe = self._isNfe()
        if isNfe is False:
            return None

        self._objNf['chave_nota'] = returnDataInDictOrArray(self._dataXml, ['nfeProc', 'NFe', 'infNFe', '@Id'])[3:]
        self._tagIde()
        self._tagEmit()
        self._tagDet()
        self._tagTotal()

        return self._objNf


if __name__ == '__main__':
    indexNfe = IndexNfe('/home/eldervivot/Programming/microservices/read-xml-nfe-nfce-cte/data/nfe2.xml')
    print(indexNfe.process())
