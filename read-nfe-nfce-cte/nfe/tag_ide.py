import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.functions import returnDataInDictOrArray, treatsFieldAsNumber
from typing import Dict


class TagIde():
    def __init__(self, dataTagIde: dict):
        self._dataTagIde = dataTagIde
        self._objIde: Dict[str, str] = {}

    def getData(self):
        self._objIde['numero_nf']: int = treatsFieldAsNumber(returnDataInDictOrArray(self._dataTagIde, ['nNF']))
        self._objIde['modelo_nf'] = treatsFieldAsNumber(returnDataInDictOrArray(self._dataTagIde, ['mod']))
        self._objIde['serie_nf'] = returnDataInDictOrArray(self._dataTagIde, ['serie'])
        self._objIde['data_emissao'] = returnDataInDictOrArray(self._dataTagIde, ['dhEmi'])
        self._objIde['data_saida_entrada'] = returnDataInDictOrArray(self._dataTagIde, ['dhSaiEnt'])
        self._objIde['tipo_documento'] = treatsFieldAsNumber(returnDataInDictOrArray(self._dataTagIde, 'tpNF'))
        self._objIde['identificador_local_destino_operacao'] = treatsFieldAsNumber(
            returnDataInDictOrArray(self._dataTagIde, ['idDest']))
        self._objIde['municipio_ocorrencia_fato'] = treatsFieldAsNumber(
            returnDataInDictOrArray(self._dataTagIde, ['cMunFG']))
        self._objIde['finalidade_nf'] = treatsFieldAsNumber(returnDataInDictOrArray(self._dataTagIde, ['finNFe']))

        return self._objIde
