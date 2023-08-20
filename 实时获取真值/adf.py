from hanlp_restful import HanLPClient
HanLP = HanLPClient('https://www.hanlp.com/api', auth=None, language='zh')
doc = HanLP.parse('晓美焰来到北京立方庭参观自然语义科技公司。', tasks='dep')
print(doc)
doc.pretty_print()
print(doc.to_conll())