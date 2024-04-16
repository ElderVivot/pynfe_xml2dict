from typing import Dict
from pynfe_xml2dict.utils.functions import returnDataInDictOrArray, treatsFieldAsDecimal


class TagTotal():
    def __init__(self, dataTagTotal: dict):
        self.__dataTagTotal = dataTagTotal
        self.__objTotal: Dict[str, str] = {}

    def getData(self):
        tagIcmsTot = returnDataInDictOrArray(self.__dataTagTotal, ['ICMSTot'])
        self.__objTotal['total_base_calculo'] = treatsFieldAsDecimal(returnDataInDictOrArray(tagIcmsTot, ['vBC']))
        self.__objTotal['total_icms'] = treatsFieldAsDecimal(returnDataInDictOrArray(tagIcmsTot, ['vICMS']))
        self.__objTotal['total_produtos'] = treatsFieldAsDecimal(returnDataInDictOrArray(tagIcmsTot, ['vProd']))
        self.__objTotal['total_frete'] = treatsFieldAsDecimal(returnDataInDictOrArray(tagIcmsTot, ['vFrete']))
        self.__objTotal['total_seguro'] = treatsFieldAsDecimal(returnDataInDictOrArray(tagIcmsTot, ['vSeg']))
        self.__objTotal['total_desconto'] = treatsFieldAsDecimal(returnDataInDictOrArray(tagIcmsTot, ['vDesc']))
        self.__objTotal['total_outros'] = treatsFieldAsDecimal(returnDataInDictOrArray(tagIcmsTot, ['vOutro']))
        self.__objTotal['total_nf'] = treatsFieldAsDecimal(returnDataInDictOrArray(tagIcmsTot, ['vNF']))

        return self.__objTotal
