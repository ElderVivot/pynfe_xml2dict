import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.functions import returnDataInDictOrArray, treatsFieldAsNumber, treatsFieldAsText
from typing import Dict


class TagEmit():
    def __init__(self, dataTagEmit: dict):
        self._dataTagEmit = dataTagEmit
        self._objEmitente: Dict[str, str] = {}

    def _getCnpjOrCpf(self):
        cnpj = returnDataInDictOrArray(self._dataTagEmit, ['CNPJ'])
        cpf = returnDataInDictOrArray(self._dataTagEmit, ['CPF'])
        self._inscricaoFederal = cnpj if cnpj != '' else cpf
        self._tipoInscricaoFederal = 'CNPJ' if cnpj != '' else 'CPF'

    def _getAddress(self):
        # implement to get this information
        return {}

    def getData(self) -> dict:
        self._getCnpjOrCpf()

        self._objEmitente['inscricao_federal'] = self._inscricaoFederal
        self._objEmitente['tipo_inscricao_federal'] = self._tipoInscricaoFederal
        self._objEmitente['razao_social'] = treatsFieldAsText(returnDataInDictOrArray(self._dataTagEmit, ['xNome']))
        self._objEmitente['nome_fantasia'] = treatsFieldAsText(returnDataInDictOrArray(self._dataTagEmit, ['xFant']))
        self._objEmitente['inscricao_estadual'] = returnDataInDictOrArray(self._dataTagEmit, ['IE'])
        self._objEmitente['regime_empresa'] = treatsFieldAsNumber(returnDataInDictOrArray(self._dataTagEmit, ['CRT']), True)
        self._objEmitente['endereco'] = self._getAddress()

        return self._objEmitente
