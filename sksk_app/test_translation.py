import MeCab
from konlpy.tag import Mecab
from konlpy.utils import pprint
from konlpy.tag import Okt

sample = '父は医者です。'
mecab = MeCab.Tagger()
# result = mecab.parse(sample)
words = []
i = 0
node = mecab.parseToNode(sample)
while node:
    p = node.feature.split(',')[0]
    if p == '名詞' or p == '動詞' or p== '形容詞' or p =='副詞':
        words.append(node.feature.split(",")[6])
    node = node.next

print(words)

sample = '어머니는 공무원입니다.'
mecab = Mecab()
pprint(mecab.pos(sample))

okt = Okt()
pprint(okt.morphs(sample, norm=False, stem=True))
