import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.append(dirNameSrc)

from utils.functions import returnDataInDictOrArray, treatsFieldAsNumber, treatsFieldAsDecimal, treatsFieldAsText
from typing import Dict, List, OrderedDict


class TagDet():
    def __init__(self, listDataTagDet: List[OrderedDict]):
        self.__listDataTagDet = listDataTagDet
        self.__objListTagDet: List[Dict[str, str]] = []
        self.__objDet: Dict[str, str] = {}

    def __amountValorContabil(self):
        return self.__objDet['valor_produto'] + self.__objDet['valor_frete'] + self.__objDet['vseg'] \
            + self.__objDet['valor_outros'] - self.__objDet['valor_desconto']

    def getData(self):
        for key, dataTagDet in enumerate(self.__listDataTagDet):

            self.__objDet['numero_item'] = key + 1
            self.__objDet['codigo_produto'] = returnDataInDictOrArray(dataTagDet, ['prod', 'cProd'])
            self.__objDet['nome_produto'] = treatsFieldAsText(returnDataInDictOrArray(dataTagDet, ['prod', 'xProd']))
            self.__objDet['global_trade_item_number'] = returnDataInDictOrArray(dataTagDet, ['prod', 'cEAN'])
            self.__objDet['ncm'] = returnDataInDictOrArray(dataTagDet, ['prod', 'NCM'])
            self.__objDet['cfop'] = treatsFieldAsNumber(returnDataInDictOrArray(dataTagDet, ['prod', 'CFOP']), isInt=True)
            self.__objDet['unidade'] = returnDataInDictOrArray(dataTagDet, ['prod', 'uCom'])
            self.__objDet['quantidade'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'qCom']), 4)
            self.__objDet['valor_unitario'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'vUnCom']), 10)
            self.__objDet['valor_produto'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'vProd']), 10)
            self.__objDet['valor_frete'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'vFrete']), 10)
            self.__objDet['vseg'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'vSeg']), 10)
            self.__objDet['valor_outros'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'vOutro']), 10)
            self.__objDet['valor_desconto'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'vDesc']), 10)
            self.__objDet['valor_total'] = self.__amountValorContabil()
            self.__objDet['informacao_adicionais'] = treatsFieldAsText(returnDataInDictOrArray(dataTagDet, ['infAdProd']))

            self.__objListTagDet.append(self.__objDet.copy())
            self.__objDet.clear()

        return self.__objListTagDet
