from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
from NLPService import NLPService


class BERTService(NLPService):
    def __init__(self):
        super().__init__(0, 5, 10, False)

    def ComputeCosineSimilarity(self, text1, text2):
        tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        model = BertModel.from_pretrained('bert-base-chinese')

        inputs = tokenizer([text1, text2], padding=True,
                           truncation=True, return_tensors='pt')
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']

        # 获取文本的表示
        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            # 提取CLS标记的表示
            embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()

        # 计算余弦相似度
        similarity = cosine_similarity(embeddings)[0, 1]
        return similarity

    def Configed(self):
        return True

    def Description(self):
        return "使用BERT算法计算文本余弦相似度"
