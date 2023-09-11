from NLPService import NLPService
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

# 加载BERT分词器
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

# 加载预训练的BERT模型
model = BertModel.from_pretrained('bert-base-chinese')

class BERTBaseChineseService(NLPService):
    def __init__(self):
        super().__init__(70, 3)

    def ComputeSimilarity(self, text1, text2):
        # 对文本进行分词和编码
        tokens1 = tokenizer(text1, padding=True, truncation=True, return_tensors='pt')
        tokens2 = tokenizer(text2, padding=True, truncation=True, return_tensors='pt')

        # 获取BERT模型的输出
        with torch.no_grad():
            output1 = model(**tokens1)
            output2 = model(**tokens2)

        # 获取文本的嵌入向量
        embeddings1 = output1.last_hidden_state.mean(dim=1)  # 使用均值池化
        embeddings2 = output2.last_hidden_state.mean(dim=1)

        # 计算余弦相似度
        similarity = cosine_similarity(embeddings1, embeddings2)

        return similarity[0][0]

    def Configed(self)->bool:
        return True

    def Description(self):
        return "使用BERT计算文本余弦相似度"
