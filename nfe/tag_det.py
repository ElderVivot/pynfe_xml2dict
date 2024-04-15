import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.append(dirNameSrc)

from utils.functions import returnDataInDictOrArray, treatsFieldAsNumber, treatsFieldAsDecimal, treatsFieldAsText
from typing import Dict, List, OrderedDict


class TagDet():
    def __init__(self, listDataTagDet: List[OrderedDict]):
        self._listDataTagDet = listDataTagDet
        self._objListTagDet: List[Dict[str, str]] = []
        self._objDet: Dict[str, str] = {}

    def __amountValorContabil(self):
        return self._objDet['valor_produto'] + self._objDet['valor_frete'] + self._objDet['vseg'] \
            + self._objDet['valor_outros'] - self._objDet['valor_desconto']

    def getData(self):
        for key, dataTagDet in enumerate(self._listDataTagDet):

            self._objDet['numero_item'] = key + 1
            self._objDet['codigo_produto'] = returnDataInDictOrArray(dataTagDet, ['prod', 'cProd'])
            self._objDet['nome_produto'] = treatsFieldAsText(returnDataInDictOrArray(dataTagDet, ['prod', 'xProd']))
            self._objDet['global_trade_item_number'] = returnDataInDictOrArray(dataTagDet, ['prod', 'cEAN'])
            self._objDet['ncm'] = returnDataInDictOrArray(dataTagDet, ['prod', 'NCM'])
            self._objDet['cfop'] = treatsFieldAsNumber(returnDataInDictOrArray(dataTagDet, ['prod', 'CFOP']), isInt=True)
            self._objDet['unidade'] = returnDataInDictOrArray(dataTagDet, ['prod', 'uCom'])
            self._objDet['quantidade'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'qCom']), 4)
            self._objDet['valor_unitario'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'vUnCom']), 10)
            self._objDet['valor_produto'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'vProd']), 10)
            self._objDet['valor_frete'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'vFrete']), 10)
            self._objDet['vseg'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'vSeg']), 10)
            self._objDet['valor_outros'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'vOutro']), 10)
            self._objDet['valor_desconto'] = treatsFieldAsDecimal(returnDataInDictOrArray(dataTagDet, ['prod', 'vDesc']), 10)
            self._objDet['valor_total'] = self.__amountValorContabil()
            self._objDet['informacao_adicionais'] = treatsFieldAsText(returnDataInDictOrArray(dataTagDet, ['infAdProd']))

            self._objListTagDet.append(self._objDet.copy())
            self._objDet.clear()

        return self._objListTagDet
