import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.functions import returnDataInDictOrArray, treatsFieldAsNumber
from typing import Dict


class TagIde():
    def __init__(self, dataTagIde: dict):
        self.__dataTagIde = dataTagIde
        self.__objIde: Dict[str, str] = {}

    def getData(self):
        self.__objIde['numero_nf'] = treatsFieldAsNumber(returnDataInDictOrArray(self.__dataTagIde, ['nNF']))
        self.__objIde['modelo_nf'] = treatsFieldAsNumber(returnDataInDictOrArray(self.__dataTagIde, ['mod']))
        self.__objIde['serie_nf'] = returnDataInDictOrArray(self.__dataTagIde, ['serie'])
        self.__objIde['data_emissao'] = returnDataInDictOrArray(self.__dataTagIde, ['dhEmi'])
        self.__objIde['data_saida_entrada'] = returnDataInDictOrArray(self.__dataTagIde, ['dhSaiEnt'])
        self.__objIde['tipo_documento'] = treatsFieldAsNumber(returnDataInDictOrArray(self.__dataTagIde, 'tpNF'))
        self.__objIde['identificador_local_destino_operacao'] = treatsFieldAsNumber(
            returnDataInDictOrArray(self.__dataTagIde, ['idDest']))
        self.__objIde['municipio_ocorrencia_fato'] = treatsFieldAsNumber(
            returnDataInDictOrArray(self.__dataTagIde, ['cMunFG']))
        self.__objIde['finalidade_nf'] = treatsFieldAsNumber(returnDataInDictOrArray(self.__dataTagIde, ['finNFe']))

        return self.__objIde
