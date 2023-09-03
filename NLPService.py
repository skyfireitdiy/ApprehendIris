import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk
import snownlp

from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

class NLPService(object):

    def __init__(self, up_segment=0, down_segment=10, top=5, model='TF-IDF', need_group=True):
        self._up_segment = up_segment
        self._down_segment = down_segment
        self._top = top
        self._need_group = need_group
        if model == 'TF-IDF':
            self._ComputeCosineSimilarity = self._ComputeCosineSimilarityByTFIDF
        elif model == 'BERT':
            self._ComputeCosineSimilarity = self._ComputeCosineSimilarityByBERT
        else:
            raise ValueError('Invalid model')

    @staticmethod
    def _GroupOverlappingSegments(segments:list):
        groups = []
        current_group = []
        segments.sort(key=lambda x: x[2][0])

        # 对每个线段进行遍历
        for segment in segments:
            if not current_group:
                current_group.append(segment)
            else:
                # 判断当前线段是否与当前分组中的线段重叠
                if segment[2][0] < current_group[-1][2][1]:
                    current_group.append(segment)
                else:
                    groups.append(current_group)
                    current_group = [segment]

        if current_group:
            groups.append(current_group)
        
        return groups

    @staticmethod
    def _Sentences(text:str):
        #  nlp = snownlp.SnowNLP(text)
        #  return nlp.sentences
        return [y for y in [x.strip() for x in text.splitlines()] if len(y)>0]

    def _Words(self, text):
        try:
            sw = stopwords.words('chinese')
        except Exception as e:
            nltk.download('stopwords')
            sw = stopwords.words('chinese')
        ws = list(jieba.cut(text, cut_all=False))
        return [w for w in ws if w not in sw]


    def _ComputeCosineSimilarityByTFIDF(self, text1, text2):
        # 去除停用词
        seg1_filtered = ' '.join(self._Words(text1))
        seg2_filtered = ' '.join(self._Words(text2))

        # 使用TF-IDF向量化文本
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([seg1_filtered, seg2_filtered])

        # 计算余弦相似度
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
        return similarity

    def _ComputeCosineSimilarityByBERT(self, text1, text2):
        tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        model = BertModel.from_pretrained('bert-base-chinese')

        inputs = tokenizer([text1, text2], padding=True, truncation=True, return_tensors='pt')
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']

        # 获取文本的表示
        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()  # 提取CLS标记的表示

        # 计算余弦相似度
        similarity = cosine_similarity(embeddings)[0, 1]
        return similarity

    def GetKeySentences(self, text, question:str):
        sts = NLPService._Sentences(text)
        ret = []
        for i,s in enumerate(sts):
            left = i-self._up_segment if i-self._up_segment>0 else 0
            right = i+self._down_segment+1 if i+self._down_segment+1<len(sts) else len(sts)
            t = '\n'.join(sts[left : right])
            rate = self._ComputeCosineSimilarity(t, question)
            print(f"{rate} {t}")
            if rate == 0:
                continue
            ret.append((rate, t , (left, right)))

        if self._need_group:
            ret = self._GroupOverlappingSegments(ret)
            ret = [sorted(x, key=lambda t:t[0], reverse=True)[0] for x in ret]

        ret.sort(key=lambda x: x[0], reverse=True)
        if len(ret) > self._top:
            return ret[:self._top]
        return ret

