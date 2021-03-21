import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.functions import returnDataInDictOrArray, treatsFieldAsNumber
from typing import Dict


class TagDest():
    def __init__(self, dataTagDest: dict):
        self._dataTagDest = dataTagDest
        self._objDestinatario: Dict[str, str] = {}

    def _getCnpjOrCpf(self):
        cnpj = returnDataInDictOrArray(self._dataTagDest, ['CNPJ'])
        cpf = returnDataInDictOrArray(self._dataTagDest, ['CPF'])
        self._idEstrangeiro = returnDataInDictOrArray(self._dataTagDest, ['idEstrangeiro'], '')
        if self._idEstrangeiro == '' or self._idEstrangeiro is None:
            self._inscricaoFederal = cnpj if cnpj != '' else cpf
            self._tipoInscricaoFederal = 'CNPJ' if cnpj != '' else 'CPF'
        else:
            self._inscricaoFederal = ''
            self._tipoInscricaoFederal = ''

    def _getAddress(self):
        # implement to get this information
        return {}

    def getData(self) -> dict:
        self._getCnpjOrCpf()

        self._objDestinatario['inscricao_federal'] = self._inscricaoFederal
        self._objDestinatario['tipo_inscricao_federal'] = self._tipoInscricaoFederal
        self._objDestinatario['id_estrangeiro'] = self._idEstrangeiro
        self._objDestinatario['razao_social'] = returnDataInDictOrArray(self._dataTagDest, ['xNome'])
        self._objDestinatario['indicador_inscricao_estadual'] = treatsFieldAsNumber(
            returnDataInDictOrArray(self._dataTagDest, ['indIEDest']), True)
        self._objDestinatario['inscricao_estadual'] = returnDataInDictOrArray(self._dataTagDest, ['IE'])
        self._objDestinatario['inscricao_municipal'] = returnDataInDictOrArray(self._dataTagDest, ['IM'])
        self._objDestinatario['endereco'] = self._getAddress()

        return self._objDestinatario
