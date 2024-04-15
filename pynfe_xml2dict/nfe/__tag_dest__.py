from utils.functions import returnDataInDictOrArray, treatsFieldAsNumber, treatsFieldAsText
from typing import Dict


class TagDest():
    def __init__(self, dataTagDest: dict):
        self.__dataTagDest = dataTagDest
        self.__objDestinatario: Dict[str, str] = {}

    def __getCnpjOrCpf(self):
        cnpj = returnDataInDictOrArray(self.__dataTagDest, ['CNPJ'])
        cpf = returnDataInDictOrArray(self.__dataTagDest, ['CPF'])
        self.__idEstrangeiro = returnDataInDictOrArray(self.__dataTagDest, ['idEstrangeiro'], '')
        if self.__idEstrangeiro == '' or self.__idEstrangeiro is None:
            self.__inscricaoFederal = cnpj if cnpj != '' else cpf
            self.__tipoInscricaoFederal = 'CNPJ' if cnpj != '' else 'CPF'
        else:
            self.__inscricaoFederal = ''
            self.__tipoInscricaoFederal = ''

    def __getAddress(self):
        # implement to get this information
        return {}

    def getData(self) -> dict:
        self.__getCnpjOrCpf()

        self.__objDestinatario['inscricao_federal'] = self.__inscricaoFederal
        self.__objDestinatario['tipo_inscricao_federal'] = self.__tipoInscricaoFederal
        self.__objDestinatario['id_estrangeiro'] = self.__idEstrangeiro
        self.__objDestinatario['razao_social'] = treatsFieldAsText(returnDataInDictOrArray(self.__dataTagDest, ['xNome']))
        self.__objDestinatario['indicador_inscricao_estadual'] = treatsFieldAsNumber(
            returnDataInDictOrArray(self.__dataTagDest, ['indIEDest']), True)
        self.__objDestinatario['inscricao_estadual'] = returnDataInDictOrArray(self.__dataTagDest, ['IE'])
        self.__objDestinatario['inscricao_municipal'] = returnDataInDictOrArray(self.__dataTagDest, ['IM'])
        self.__objDestinatario['endereco'] = self.__getAddress()

        return self.__objDestinatario
