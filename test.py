import json
# from xml.etree import ElementTree
from pynfe_xml2dict.nfe.ler_nfe import LerNfe

indexNfe = LerNfe('_data/xml_complete.xml')
print(json.dumps(indexNfe.process(), indent=4))


# TESTING WITH NAMESPACE - DONT WORK YET
# tree = ElementTree.parse('_data/xml_complete.xml')
# root = tree.getroot()

# namespaces = {"ns": "http://www.portalfiscal.inf.br/nfe"}

# print(root.find('ns:nfeProc', namespaces=namespaces))
