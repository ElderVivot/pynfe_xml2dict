import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.functions import returnDataInDictOrArray, treatsFieldAsNumber, treatsFieldAsText
from typing import Dict


class TagEmit():
    def __init__(self, dataTagEmit: dict):
        self.__dataTagEmit = dataTagEmit
        self.__objEmitente: Dict[str, str] = {}

    def __getCnpjOrCpf(self):
        cnpj = returnDataInDictOrArray(self.__dataTagEmit, ['CNPJ'])
        cpf = returnDataInDictOrArray(self.__dataTagEmit, ['CPF'])
        self.__inscricaoFederal = cnpj if cnpj != '' else cpf
        self.__tipoInscricaoFederal = 'CNPJ' if cnpj != '' else 'CPF'

    def __getAddress(self):
        # implement to get this information
        return {}

    def getData(self) -> dict:
        self.__getCnpjOrCpf()

        self.__objEmitente['inscricao_federal'] = self.__inscricaoFederal
        self.__objEmitente['tipo_inscricao_federal'] = self.__tipoInscricaoFederal
        self.__objEmitente['razao_social'] = treatsFieldAsText(returnDataInDictOrArray(self.__dataTagEmit, ['xNome']))
        self.__objEmitente['nome_fantasia'] = treatsFieldAsText(returnDataInDictOrArray(self.__dataTagEmit, ['xFant']))
        self.__objEmitente['inscricao_estadual'] = returnDataInDictOrArray(self.__dataTagEmit, ['IE'])
        self.__objEmitente['regime_empresa'] = treatsFieldAsNumber(returnDataInDictOrArray(self.__dataTagEmit, ['CRT']), True)
        self.__objEmitente['endereco'] = self.__getAddress()

        return self.__objEmitente
