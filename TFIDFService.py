from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk
import jieba


from NLPService import NLPService


class TFIDFService(NLPService):
    def __init__(self):
        super().__init__(0, 50, 10, True)

    def _Words(self, text):
        try:
            sw = stopwords.words('chinese')
        except Exception as e:
            nltk.download('stopwords')
            sw = stopwords.words('chinese')
        ws = list(jieba.cut(text, cut_all=False))
        return [w for w in ws if w not in sw]

    def ComputeCosineSimilarity(self, text1, text2):
        # 去除停用词
        seg1_filtered = ' '.join(self._Words(text1))
        seg2_filtered = ' '.join(self._Words(text2))

        # 使用TF-IDF向量化文本
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([seg1_filtered, seg2_filtered])

        # 计算余弦相似度
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
        return similarity

    def Configed(self):
        return True

    def Description(self):
        return "使用TF-IDF算法计算文本余弦相似度"

